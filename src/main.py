from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from src.routers import notes
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_route(notes.router)


@app.get('/')
async def get_root():
    ''' redirect to /docs '''
    return RedirectResponse('/docs')
