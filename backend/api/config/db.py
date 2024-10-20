from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Field, create_engine, Session, select
import os
from fastapi import Depends
from api.schemas.schema import Rule
from api.models.rule import NewRule
from api.config.session import get_session

# Store a rule in the database
def store_rule(rule_string: NewRule, db: Session = Depends(get_session)):
    if not rule_string:
        raise HTTPException(status_code=400, detail="No rule string provided")
    new_rule_record=Rule(
        rule=rule_string.rule
    )
    db.add(new_rule_record)
    db.commit()
    db.refresh(new_rule_record)
    return JSONResponse(
        status_code=200,
        content={"message": "Rule added successfully"}
    )