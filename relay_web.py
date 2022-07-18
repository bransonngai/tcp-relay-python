import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


# This is the CORS accepted address
origins = [
    "127.0.0.1:4000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def index():
    return "Hello World"


uvicorn.run(app,
            host='0.0.0.0',
            port=4000,
            log_level='info',  # set logger warning here if you want less
            )