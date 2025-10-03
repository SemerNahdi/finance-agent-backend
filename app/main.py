from fastapi import FastAPI
from app.routes import agent

app = FastAPI(title="Finance Agent Backend")

# Include the agent router
app.include_router(agent.router, prefix="/agent")

@app.get("/")
def root():
    return {"message": "Finance Agent backend is running"}
