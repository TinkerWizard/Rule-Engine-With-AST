from fastapi import APIRouter, Depends, HTTPException, FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from sqlmodel import Session, select
from api.utilities.rule import create_rule, evaluate_rule, combine_rules, is_valid_rule
from api.utilities.node import node_to_dict
from api.config.db import store_rule, get_session
from api.models.rule import NewRule, EvaluateRule, CombineRulesInput
from pydantic import BaseModel
import os
import json
import logging
from typing import List


from api.schemas.schema import Rule
router = APIRouter()

class RuleResponse(BaseModel):
    id: int
    name: str
    description: str  # Include fields you want to return

    class Config:
        orm_mode = True  # This tells Pydantic to serialize ORM objects

@router.get('/get-rules')
async def get_rules(db: Session = Depends(get_session)):
    rules = db.exec(select(Rule.rule)).all()
    print(len(rules))
    
    # print("rules:", rules)
    a = {"rules": rules}
    print("here:", a)
    return a

@router.post("/save")
async def rules(new_rule: NewRule, db: Session = Depends(get_session)):    
    if not new_rule:
        raise HTTPException(status_code=400, detail="No rule string provided")
    if not is_valid_rule(new_rule.rule):
        raise HTTPException(status_code=400, detail="Invalid rule")
    try:
        new_rule_record=Rule(
            rule=new_rule.rule
        )
        db.add(new_rule_record)
        db.commit()
        db.refresh(new_rule_record)
        rule_ast = create_rule(new_rule.rule)
        json_text = json.dumps(node_to_dict(rule_ast), indent=4)
        return JSONResponse(
            status_code=200,
            content={"message": "Rule added successfully", 'ast': json_text}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate")
async def evaluate(evaluateRule: EvaluateRule):
    if not evaluate_rule:
        raise HTTPException(status_code=400, detail="Missing rule string or evaluation data")
    try:
        rule_ast = create_rule(evaluateRule.rule)
        data = evaluateRule.data
        json_data = json.loads(data)
        print(json_data)
        logging.debug(f'Rule AST: {rule_ast}')
        result = evaluate_rule(rule_ast, json_data)
        print(result)
        return JSONResponse(content={'result': result})
    
    except Exception as e:
        logging.error(f'Error: {e}')
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.post('/combine')
def combine_multiple_rules(rules: CombineRulesInput):
    result = combine_rules(rules.rules, rules.combine_operator)
    json_text = json.dumps(node_to_dict(result), indent=4)
    return JSONResponse(
        status_code=200,
        content={"message": "Rule combined successfully", 'ast': json_text}
    )
