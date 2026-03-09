from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Task])
async def read_tasks(
    db: AsyncSession = Depends(deps.get_db),
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    tasks = await crud.get_multi(db, project_id=project_id, status=status, skip=skip, limit=limit)
    return tasks

@router.post("/", response_model=schemas.Task)
async def create_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    task_in: schemas.TaskCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    project = await crud.get(db=db, id=task_in.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    task = await crud.create(db=db, obj_in=task_in)
    return task

@router.get("/{id}", response_model=schemas.Task)
async def read_task(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    task = await crud.get(db=db, id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
