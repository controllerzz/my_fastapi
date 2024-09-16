from sqlalchemy import select, func

from src.models.hotels import HotelsModel
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsModel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
        query = select(HotelsModel)

        if location:
            query = query.filter(func.lower(HotelsModel.location).contains(location.lower()))

        if title:
            query = query.filter(func.lower(HotelsModel.title).contains(title.lower()))

        query = (
            query
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)
        return result.scalars().all()
