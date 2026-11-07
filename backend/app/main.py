from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine
from app.models import Base
from app.routers import auth,workspaces,drafts,insights
import os

Base.metadata.create_all(bind=engine)
os.makedirs("uploads",exist_ok=True)

app=FastAPI(title="CodeNexus Brand Governance",version="2.0.0",description="Pre-Publication Brand Governance Platform by Social Bugs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(workspaces.router)
app.include_router(drafts.router)
app.include_router(insights.router)

@app.get("/")
def root():
    return {"message":"CodeNexus Brand Governance API","version":"2.0.0","team":"Social Bugs"}

@app.get("/health")
def health():
    return {"status":"ok"}

