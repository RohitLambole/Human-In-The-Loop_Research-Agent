from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.thread import Thread


async def get_owned_thread(
    thread_id: UUID,
    user: dict[str, str] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Thread:
    thread = await db.get(Thread, thread_id)
    if thread is None or thread.user_id != user["user_id"]:
        # Deliberately use 404 so callers cannot enumerate other users' thread IDs.
        raise HTTPException(status_code=404, detail="Session not found")
    return thread
