from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project
from app.schemas.project import ProjectCreate

async def get(db: AsyncSession, id: int) -> Project:
    result = await db.execute(select(Project).where(Project.id == id))
    return result.scalars().first()

async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Project]:
    result = await db.execute(select(Project).offset(skip).limit(limit))
    return result.scalars().all()

async def create(db: AsyncSession, obj_in: ProjectCreate, owner_id: int) -> Project:
    db_obj = Project(title=obj_in.title, description=obj_in.description, owner_id=owner_id)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
