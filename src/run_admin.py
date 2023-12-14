import uvicorn

from core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "admin:app",
        host="0.0.0.0",
        port=settings.admin_port,
        reload=True,
        reload_dirs=["/app"],
    )
