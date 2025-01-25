from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.app.routes import employee, report, squad
import uvicorn

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

api.include_router(employee.router, prefix="/employee", tags=["employee"])
api.include_router(report.router, prefix="/report", tags=["report"])
api.include_router(squad.router, prefix="/squad", tags=["squad"])

if __name__ == "__main__":
    uvicorn.run("main:api", host="0.0.0.0", port=8000, reload=True)