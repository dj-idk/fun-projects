from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, or_
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated

from model import Post
from schema import PostCreate, PostInDB, PostUpdate
from exceptions import InternalServerError, NotFound


class PostManager:

    @staticmethod
    async def create_post(session: AsyncSession, post: PostCreate):
        try:
            new_post = Post(
                title=post.title,
                content=post.content,
                category=post.category,
                tags=post.tags,
            )
            session.add(new_post)
            await session.commit()
            await session.refresh(new_post)
            return PostInDB.model_validate(new_post)
        except Exception as e:
            await session.rollback()
            raise InternalServerError(f"Internal Server Error: {e}")

    @staticmethod
    async def update_post(session: AsyncSession, update_form: PostUpdate, post_id: int):
        try:
            post = await session.get(Post, post_id)
            if not post:
                raise NotFound()

            update_data = update_form.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(post, key, value)
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return PostInDB.model_validate(post)
        except NotFound as e:
            raise e
        except Exception as e:
            await session.rollback()
            raise InternalServerError(f"Internal Server Error: {e}")

    @staticmethod
    async def delete_post(session: AsyncSession, post_id: int):
        try:
            post = await session.get(Post, post_id)
            if not post:
                raise NotFound()

            await session.delete(post)
            await session.commit()
            return {"message": f"Post {post_id} was deleted successfully."}
        except NotFound as e:
            raise e
        except Exception as e:
            await session.rollback()
            raise InternalServerError(f"Internal Server Error: {e}")

    @staticmethod
    async def get_post(session: AsyncSession, post_id: int):
        try:
            post = await session.get(Post, post_id)
            if not post:
                raise NotFound()
            return PostInDB.model_validate(post)
        except NotFound as e:
            raise e
        except Exception as e:
            raise InternalServerError(f"Internal Server Error: {e}")

    @staticmethod
    async def get_all_posts_or_none(session: AsyncSession, skip: int, limit: int):
        try:
            if limit > 100:
                limit = 100

            total = await session.scalar(func.count(Post.id))

            total_pages = (total // limit) + (1 if total % limit != 0 else 0)
            current_page = (skip // limit) + 1

            posts_query = await session.execute(select(Post).offset(skip).limit(limit))
            posts = posts_query.scalars().all()

            post_responses = [PostInDB.model_validate(post) for post in posts]

            pagination = {
                "total": total,
                "limit": limit,
                "skip": skip,
                "current_page": current_page,
                "total_pages": total_pages,
                "has_previous": current_page > 1,
                "has_next": current_page < total_pages,
            }

            return {"posts": post_responses, "pagination": pagination}

        except Exception as e:
            raise InternalServerError(f"Internal Server Error: {e}")

    @staticmethod
    async def search_posts(session: AsyncSession, search_term: str):
        try:
            search_query = select(Post).where(
                or_(
                    Post.title.ilike(f"%{search_term}%"),
                    Post.content.ilike(f"%{search_term}%"),
                    Post.category.ilike(f"%{search_term}%"),
                )
            )

            result = await session.execute(search_query)
            posts = result.scalars().all()

            post_responses = [PostInDB.model_validate(post) for post in posts]

            return post_responses

        except Exception as e:
            raise InternalServerError(f"Internal Server Error: {e}")
