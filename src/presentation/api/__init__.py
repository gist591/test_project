from .operators import router as operators_router
from .leads import router as leads_router
from .contacts import router as contacts_router
from .sources import router as sources_router


__all__ = [
    "operators_router",
    "leads_router",
    "contacts_router",
    "sources_router",
]
