from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
import os
from api.utilities.rule import create_rule, evaluate_rule
from api.config.db import store_rule
import logging


from fastapi import APIRouter
from api.routes import rules
api_router = APIRouter()


api_router.include_router(rules.router, prefix="/rules",tags=["Rules"])



# Setup basic logging
logging.basicConfig(level=logging.DEBUG)
