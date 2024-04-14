from fastapi import FastAPI, APIRouter
from chemistry_calculator.mould_temperature import get_mould_data
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()  # This loads the .env file

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("VITE_WEBSITE_HOST"),
                   "https://chemistry-chemistry-calculator-portal-xopabutmga-ez.a.run.app",
                   "https://chemistry-xopabutmga-ez.a.run.app",
                   "ALLOW_ORIGINS", ""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up the API router
router = APIRouter()

@router.post("/calculate-mould")
async def calculate_mould():
    try:
        results = get_mould_data()
        return results
    except Exception as e:
        return {"error": str(e)}

app.include_router(router)
if __name__ == "__main__":
    portname = int(os.getenv("APP_PORT"))
    hostname = "0.0.0.0" #os.getenv("APP_HOST"),
    import uvicorn
    uvicorn.run("main:app", host=hostname, port=portname, reload=True)
