from fastapi import FastAPI, APIRouter
from chemistry_calculator.mould_temperature import get_mould_data
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
from dotenv import load_dotenv
load_dotenv()  # This loads the .env file
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("VITE_WEBSITE_HOST"),  # Adjust the port if your Svelte app runs on a different one
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter()

@router.post("/calculate-mould")
async def calculate_mould():
    results = get_mould_data()
    return results

app.include_router(router)
portname = int(os.getenv("APP_PORT"))
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=portname, reload=True)
