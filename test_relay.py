import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


# This is the CORS accepted address
origins = [
    "localhost:3000",
    "127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def index():
    return "Hello World"


uvicorn.run(app,
            host='127.0.0.1',
            port=4000,
            log_level='info',  # set logger warning here if you want less
            )