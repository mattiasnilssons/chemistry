from fastapi import FastAPI, APIRouter, HTTPException
from chemistry_calculator.mould_temperature import get_mould_data
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
app = FastAPI()
load_dotenv()  # This loads the .env file

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("VITE_WEBSITE_HOST"),
                   "https://chemistry-chemistry-calculator-portal-xopabutmga-ez.a.run.app",
                   "https://chemistry-xopabutmga-ez.a.run.app"
                   "https://chemistry-chemistry-calculator-portal-xopabutmga-ez.a.run.app/mold_risk",
                    "https://chemistry-chemistry-calculator-portal-xopabutmga-ez.a.run.app/overview",
                    "https://chemistry-chemistry-calculator-portal-xopabutmga-ez.a.run.app/water_content",
                   "ALLOW_ORIGINS", ""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

# Set up the API router
router = APIRouter()
@app.exception_handler(Exception)
async def universal_exception_handler(request, exc):
    # Log the exception details here, e.g., to a file or a logging service
    print(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )
@router.post("/calculate-mould")
async def calculate_mould():
    try:
        results = get_mould_data()
        return results
    except Exception as e:
        # Log specific exception details and raise a HTTPException
        print(f"Error during mould_risk processing: {e}")
        raise HTTPException(status_code=500, detail="Error processing the request")

app.include_router(router)
if __name__ == "__main__":
    portname = int(os.getenv("APP_PORT"))
    hostname = "0.0.0.0" #os.getenv("APP_HOST"),
    import uvicorn
    uvicorn.run("main:app", host=hostname, port=portname, reload=True)
