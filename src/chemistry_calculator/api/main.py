from fastapi import FastAPI, APIRouter
from chemistry_calculator.mould_temperature import get_mould_data
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust the port if your Svelte app runs on a different one
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
