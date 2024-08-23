import logging
from typing import List, Optional
import requests
from pydantic import BaseModel, EmailStr, Field, ValidationError

# Define Pydantic pydantic_models
class ContactPoint(BaseModel):
    type: str = Field(..., alias='@type')
    fn: str
    hasEmail: Optional[str] = EmailStr


class Publisher(BaseModel):
    type: str = Field(..., alias='@type')
    name: str


class DistributionItem(BaseModel):
    type: str = Field(..., alias='@type')
    downloadURL: str
    mediaType: str


class Dataset(BaseModel):
    accessLevel: str
    landingPage: str
    bureauCode: List[str]
    issued: str
    type: str = Field(..., alias='@type')
    modified: str
    released: str
    keyword: List[str]
    contactPoint: ContactPoint
    publisher: Publisher
    identifier: str
    description: str
    title: str
    programCode: List[str]
    distribution: List[DistributionItem]
    theme: List[str]