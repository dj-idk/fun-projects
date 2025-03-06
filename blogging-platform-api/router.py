from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from service import PostManager
from schema import PostCreate, PostInDB, PostUpdate
from database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Post Mangement"],
)

db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.post("/", response_model=PostInDB)
async def create_post(
    session: db_dependency,
    post: PostCreate,
):
    try:
        return await PostManager.create_post(post, session)
    except Exception as e:
        raise e


@router.put("/{post_id}", response_model=PostInDB)
async def update_post(
    session: db_dependency,
    post_id: int,
    update_form: PostUpdate,
):
    try:
        return await PostManager.update_post(session, update_form, post_id)
    except Exception as e:
        raise e


@router.delete("/{post_id}", response_model=dict)
async def delete_post(
    session: db_dependency,
    post_id: int,
):
    try:
        return await PostManager.delete_post(session, post_id)
    except Exception as e:
        raise e


@router.get("/all", response_model=dict)
async def get_all_posts_or_none(
    session: db_dependency,
    skip: int = 0,
    limit: int = 10,
):
    try:
        return await PostManager.get_all_posts_or_none(session, skip, limit)
    except Exception as e:
        raise e


@router.get("/search", response_model=List[PostInDB])
async def search_posts(session: db_dependency, search_term: str):
    try:
        return await PostManager.search_posts(session, search_term)
    except Exception as e:
        raise e


@router.get("/{post_id}", response_model=PostInDB)
async def get_post(
    session: db_dependency,
    post_id: int,
):
    try:
        return await PostManager.get_post(session, post_id)
    except Exception as e:
        raise e
