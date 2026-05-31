from datetime import date, datetime
from typing import Any, List, Optional, Union
import uuid
from ninja import Schema, Field
from pydantic import BaseModel
import re




class SettingsSerializer(Schema):
    data: str
    
    

class ResultSerializer(BaseModel):
    data: Any
    status: bool
    status_code: int
    message: str
    