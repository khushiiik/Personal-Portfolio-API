from fastapi import FastAPI
from app.database import Base, engine
from app import routers
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Linkup API",
    description="Users portfolio.",
)

app.include_router(routers.auth.router)
app.include_router(routers.user.router)
app.include_router(routers.skills.router)
app.include_router(routers.project.router)


@app.get("/")
def root():
    return {"message": "Linkup API is running!"}
