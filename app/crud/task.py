from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.task import Task, Tag
from app.schemas.task import TaskCreate, TaskUpdate

async def get_tag_by_name(db: AsyncSession, name: str) -> Tag:
    result = await db.execute(select(Tag).where(Tag.name == name))
    return result.scalars().first()

async def create_tag_if_not_exists(db: AsyncSession, name: str) -> Tag:
    tag = await get_tag_by_name(db, name)
    if not tag:
        tag = Tag(name=name)
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
    return tag

async def get(db: AsyncSession, id: int) -> Task:
    result = await db.execute(select(Task).options(selectinload(Task.tags)).where(Task.id == id))
    return result.scalars().first()

async def get_multi(db: AsyncSession, project_id: Optional[int] = None, status: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Task]:
    query = select(Task).options(selectinload(Task.tags))
    if project_id:
        query = query.where(Task.project_id == project_id)
    if status:
        query = query.where(Task.status == status)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

async def create(db: AsyncSession, obj_in: TaskCreate) -> Task:
    tags = []
    for tag_name in obj_in.tags:
        tag = await create_tag_if_not_exists(db, tag_name)
        tags.append(tag)
    
    db_obj = Task(
        title=obj_in.title,
        description=obj_in.description,
        status=obj_in.status,
        project_id=obj_in.project_id,
        assignee_id=obj_in.assignee_id,
        tags=tags
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
