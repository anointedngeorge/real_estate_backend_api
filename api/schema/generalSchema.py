from datetime import date, datetime
from typing import Any, List, Optional
import uuid
from ninja import Schema, Field
from pydantic import BaseModel
import re




class SettingsSerializer(Schema):
    data: str