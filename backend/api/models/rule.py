from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any
from sqlalchemy import JSON
from typing import List, Union, Dict, Any, Literal


class NewRule(BaseModel):
    rule: str


class EvaluateRule(BaseModel):
    rule: str 
    data: str
    
class CombineRulesInput(BaseModel):
    rules: List[str] = Field(..., min_items=1, description="A list of rule strings to combine")
    combine_operator: Literal["AND", "OR"] = Field(default="AND", description="Operator to use for combining rules")

    @field_validator('rules')
    def validate_rules(cls, v):
        if not v:
            raise ValueError("At least one rule must be provided")
        return v