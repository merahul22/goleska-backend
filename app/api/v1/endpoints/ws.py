from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.ws_manager import manager
from app.core.security import decode_access_token
from app.core.database import get_db_session
from app.models.job_match import JobMatch
from app.models.worker import Worker
from sqlalchemy import update

router = APIRouter()

@router.websocket("/worker")
async def websocket_worker_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
    try:
        # 1. Authenticate via token query param
        payload = decode_access_token(token)
        if not payload or not payload.get("sub"):
            await websocket.close(code=1008) # Policy Violation
            return
            
        worker_id = payload.get("sub")
        
        # 2. Connect
        await manager.connect(worker_id, websocket)
        
        # 3. Listen for responses (Accept/Reject)
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            job_id = data.get("job_id")
            
            if action == "ACCEPT" and job_id:
                # We need a new session context here because we don't have Depends(get_db_session) injected into the loop
                async for session in get_db_session():
                    # Update JobMatch to ACCEPTED
                    await session.execute(
                        update(JobMatch)
                        .where(JobMatch.job_id == job_id, JobMatch.worker_id == worker_id)
                        .values(status="ACCEPTED")
                    )
                    # Update Worker availability
                    await session.execute(
                        update(Worker)
                        .where(Worker.id == worker_id)
                        .values(is_available=False)
                    )
                    await session.commit()
                    await manager.send_personal_message({"status": "SUCCESS", "message": "Job Accepted"}, worker_id)
                    break # Break out of async generator

    except WebSocketDisconnect:
        manager.disconnect(worker_id)
    except Exception:
        if worker_id:
            manager.disconnect(worker_id)
        await websocket.close(code=1011) # Internal Error
