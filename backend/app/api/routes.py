from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_owned_thread
from app.core.auth import get_current_user
from app.core.database import get_db
from app.models.thread import Thread

router = APIRouter()


@router.post("/sessions", status_code=status.HTTP_201_CREATED)
async def create_session(
    user: dict[str, str] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    thread = Thread(user_id=user["user_id"], status="running")
    db.add(thread)
    await db.commit()
    await db.refresh(thread)
    return {"thread_id": str(thread.thread_id), "status": thread.status}


@router.get("/sessions")
async def list_sessions(
    user: dict[str, str] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Thread).where(Thread.user_id == user["user_id"]).order_by(Thread.created_at.desc())
    )
    return [
        {
            "thread_id": str(thread.thread_id),
            "status": thread.status,
            "created_at": thread.created_at,
        }
        for thread in result.scalars().all()
    ]


@router.get("/sessions/{thread_id}/state")
async def get_session_state(thread: Thread = Depends(get_owned_thread)):
    return {"thread_id": str(thread.thread_id), "status": thread.status, "pending_interrupt": None}


@router.get("/sessions/{thread_id}/stream")
async def stream_session(thread: Thread = Depends(get_owned_thread)):
    raise HTTPException(status_code=501, detail="Streaming is introduced with the graph in Phase 1")


@router.post("/sessions/{thread_id}/resume")
async def resume_session(thread: Thread = Depends(get_owned_thread)):
    raise HTTPException(status_code=501, detail="Resume is introduced with HITL in Phase 2")
