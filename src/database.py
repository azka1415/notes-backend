from fastapi import HTTPException
from pymongo import MongoClient
from src.models import NoteResult
from datetime import datetime
from pymongo.cursor import Cursor
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

mongo = MongoClient(
    host=os.getenv('DATABASE_URL'), username=os.getenv('DATABASE_USERNAME'), password=os.getenv('DATABASE_PASSWORD'))

database = mongo['newnotes']

notes_collection = database['notes']
users_collection = database['users']
users_collection.create_index('email', unique=True)


async def db_parser(cursor: Cursor):
    ''' parse data from database into lists '''
    notes = []
    for doc in cursor:
        notes.append(
            NoteResult(**doc))
    return notes


async def fetch_all(limit: int, skip: int, title: str):
    ''' fetch every note from owner '''

    cursor = notes_collection.find(
        {'title': {"$regex": title}}).limit(limit).skip(skip)
    result = await db_parser(cursor)
    return result


async def update_note(title: str, description: str):
    ''' update note '''
    notes_collection.update_one({'title': title}, {
                                "$set": {"description": description}})
    return notes_collection.find_one({"title": title})


async def remove_note(title: str):
    ''' remove note '''
    find = notes_collection.delete_one(
        {"title": title})
    if find:
        return True
    raise HTTPException(404, "Item not found")


async def create_note(note: dict):
    ''' create note '''
    note['created_at'] = datetime.now()
    print(note)
    notes_collection.insert_one(note)
    return note
