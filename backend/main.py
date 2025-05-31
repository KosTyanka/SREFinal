from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Concert Ticketing API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/concerts")
async def get_concerts():
    concerts = [
        {
            "id": 1,
            "name": "Jennifer Lopez",
            "venue": "Astana Arena",
            "location": "Astana Kazakhstan",
            "available_tickets": 100
        },
        {
            "id": 2,
            "name": "Imagine Dragons",
            "venue": "Central Stadium",
            "location": "Almaty Kazakhstan",
            "available_tickets": 150
        },
        {
            "id": 3,
            "name": "Coldplay",
            "venue": "Almaty Arena",
            "location": "Kazakhstan",
            "available_tickets": 200
        }
    ]
    return concerts 