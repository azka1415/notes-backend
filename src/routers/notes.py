from typing import List
from fastapi import APIRouter, HTTPException
import src.database as database
from src.models import Note, NoteResult

router = APIRouter(
    prefix='/notes',
    tags=['Notes']
)


@router.get('', response_model=List[NoteResult])
async def get_all_notes(title: str = '', limit: int = 0, skip: int = 0):
    ''' fetch all notes '''
    response = await database.fetch_all(limit, skip, title)
    return response


@router.post('', response_model=NoteResult)
async def post_note(note: Note):
    ''' post new note '''
    response = await database.create_note(note.dict())
    if response:
        return response
    raise HTTPException(404, 'Bad payload')


@router.put('/{title}', response_model=Note)
async def update_note(note_title: str, data: str):
    ''' update note '''
    response = await database.update_note(note_title, data, )
    if response:
        return response
    raise HTTPException(404, 'Item not found')


@router.delete('/{title}')
async def delete_note(title: str):
    ''' delete note '''
    response = await database.remove_note(title, )
    if response:
        return 'item deleted'
    raise HTTPException(404, 'Item not found')
