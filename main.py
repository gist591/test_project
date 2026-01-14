from fastapi import FastAPI

from src.infra.db import init_db
from src.presentation.api import (
    operators_router,
    sources_router,
    contacts_router,
    leads_router,
)

app = FastAPI(
    title="Lead Distribution CRM",
    version="1.0.0",
)

app.include_router(operators_router)
app.include_router(sources_router)
app.include_router(contacts_router)
app.include_router(leads_router)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}
