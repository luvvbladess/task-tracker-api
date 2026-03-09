import os

files_to_fix = {
    "app/api/deps.py": lambda text: text.replace("from app import crud\n", ""),
    "app/api/endpoints/auth.py": lambda text: text.replace("from fastapi import APIRouter, Depends, HTTPException, status", "from fastapi import APIRouter, Depends, HTTPException").replace("from app import crud, models, schemas", "from app import crud, schemas").replace("from app.core.config import settings\n", "").replace("crud.get_by_email", "crud.user.get_by_email").replace("crud.create", "crud.user.create"),
    "app/api/endpoints/projects.py": lambda text: text.replace("crud.get_multi", "crud.project.get_multi").replace("crud.create", "crud.project.create").replace("crud.get(", "crud.project.get(").replace("crud.get(db=db", "crud.project.get(db=db"),
    "app/api/endpoints/tasks.py": lambda text: text.replace("crud.get_multi", "crud.task.get_multi").replace("project = await crud.get(", "project = await crud.project.get(").replace("crud.create", "crud.task.create").replace("task = await crud.get(", "task = await crud.task.get("),
    "app/crud/task.py": lambda text: text.replace("from app.schemas.task import TaskCreate, TaskUpdate", "from app.schemas.task import TaskCreate"),
    "app/crud/user.py": lambda text: text.replace("from app.schemas.user import UserCreate, UserUpdate", "from app.schemas.user import UserCreate"),
    "app/schemas/user.py": lambda text: text.replace("from typing import Optional, List", "from typing import Optional"),
    "app/main.py": lambda text: "import logging\nfrom fastapi import FastAPI, Request, status\nfrom fastapi.responses import JSONResponse\nfrom app.api.api import api_router\nfrom app.core.config import settings\n\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)\n\napp = FastAPI(\n    title=settings.PROJECT_NAME,\n    version=settings.VERSION,\n    openapi_url=f\"{settings.API_V1_STR}/openapi.json\"\n)\n\napp.include_router(api_router, prefix=settings.API_V1_STR)\n\n\n@app.middleware(\"http\")\nasync def log_requests(request: Request, call_next):\n    logger.info(f\"Incoming request: {request.method} {request.url}\")\n    response = await call_next(request)\n    logger.info(f\"Response status: {response.status_code}\")\n    return response\n\n\n@app.exception_handler(Exception)\nasync def global_exception_handler(request: Request, exc: Exception):\n    logger.error(f\"Global Error: {exc}\")\n    return JSONResponse(\n        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,\n        content={\"message\": \"Internal server error\"},\n    )\n\n\n@app.get(\"/\")\nasync def root():\n    return {\"message\": \"Welcome to Task Tracker API\"}\n",
    "app/crud/__init__.py": lambda text: "from . import user  # noqa: F401\nfrom . import project  # noqa: F401\nfrom . import task  # noqa: F401\n",
    "app/models/__init__.py": lambda text: "\n".join([(line + "  # noqa: F401") if line.strip() and not "# noqa" in line else line for line in text.split("\n")]),
    "app/schemas/__init__.py": lambda text: "\n".join([(line + "  # noqa: F401") if line.strip() and not "# noqa" in line else line for line in text.split("\n")])
}

for filepath, fixer in files_to_fix.items():
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = fixer(content)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
