from routes.chat_route import router as chat_router
from routes.sessions_route import router as sessions_router
from routes.pdf_route import router as pdf_router


routers = [
    chat_router,
    sessions_router,
    pdf_router,
]