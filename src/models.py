from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class Note(BaseModel):
    ''' note creation model '''
    title: str
    description: str


class NoteResult(Note):
    ''' note result for the user '''
    created_at: datetime
    owner: str
