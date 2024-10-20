from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer
from typing import Optional, List
from datetime import date



class Rule(SQLModel, table=True):
    __tablename__ = 'rule'  # Specify the table name
    id: int = Field(default=None, sa_column=Column(Integer, autoincrement=True, primary_key=True))
    rule: str  # Rule string

class Condition(SQLModel, table=True):
    __tablename__ = "condition"  # Define the table name for SQLModel

    id: Optional[int] = Field(default=None, primary_key=True)
    rule_id: int = Field(foreign_key="rule.id")
    expression: str
    operator: str
    created_at: date
    updated_at: date


class Action(SQLModel, table=True):
    __tablename__ = "action"  # Define the table name for SQLModel

    id: Optional[int] = Field(default=None, primary_key=True)
    rule_id: int = Field(foreign_key="rule.id")
    action_type: str
    action_value: str
    created_at: date
    updated_at: date


class RuleExecutionHistory(SQLModel, table=True):
    __tablename__ = "rule_execution_history"  # Define the table name for SQLModel

    id: Optional[int] = Field(default=None, primary_key=True)
    rule_id: int = Field(foreign_key="rule.id")
    executed_at: date
    status: str
    result: Optional[str] = None
    execution_time_ms: Optional[int] = None


class User(SQLModel, table=True):
    __tablename__ = "users"  # Define the table name for SQLModel

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    username: str = Field(unique=True)
    password: str
    role: str
    created_at: date
    updated_at: date


class ASTNode(SQLModel, table=True):
    __tablename__ = "ast_node"  # Define the table name for SQLModel

    id: Optional[int] = Field(default=None, primary_key=True)
    rule_id: int = Field(foreign_key="rule.id")
    node_type: str
    node_value: str
    parent_node_id: Optional[int] = None  # Self-referencing
    left_child_id: Optional[int] = None
    right_child_id: Optional[int] = None
    created_at: date
    updated_at: date
