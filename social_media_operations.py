from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from social_media import SocialMedia, SocialMediaCreate, SocialMediaUpdate


class SocialMediaOperations:

    @staticmethod
    async def read_all(session: AsyncSession) -> List[SocialMedia]:
        result = await session.exec(select(SocialMedia))
        return result.all()

    @staticmethod
    async def read_one(session: AsyncSession, entry_id: int) -> Optional[SocialMedia]:
        return await session.get(SocialMedia, entry_id)

    @staticmethod
    async def create(session: AsyncSession, entry: SocialMediaCreate) -> SocialMedia:
        new_entry = SocialMedia(**entry.dict())
        session.add(new_entry)
        await session.commit()
        await session.refresh(new_entry)
        return new_entry

    @staticmethod
    async def update(session: AsyncSession, entry_id: int, update_data: SocialMediaUpdate) -> Optional[SocialMedia]:
        existing_entry = await session.get(SocialMedia, entry_id)
        if not existing_entry:
            return None

        update_data_dict = update_data.dict(exclude_unset=True)
        for key, value in update_data_dict.items():
            setattr(existing_entry, key, value)

        session.add(existing_entry)
        await session.commit()
        await session.refresh(existing_entry)
        return existing_entry

    @staticmethod
    async def delete(session: AsyncSession, entry_id: int) -> Optional[SocialMedia]:
        existing_entry = await session.get(SocialMedia, entry_id)
        if not existing_entry:
            return None

        await session.delete(existing_entry)
        await session.commit()
        return existing_entry

    @staticmethod
    async def search_by_gender(session: AsyncSession, gender: str) -> List[SocialMedia]:
        result = await session.exec(
            select(SocialMedia).where(SocialMedia.gender.ilike(gender))
        )
        return result.all()

    @staticmethod
    async def filter_by_age(session: AsyncSession) -> List[SocialMedia]:
        result = await session.exec(select(SocialMedia).order_by(SocialMedia.age))
        return result.all()
