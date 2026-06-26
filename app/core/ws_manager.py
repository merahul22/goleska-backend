import json
import asyncio
from typing import Dict
from fastapi import WebSocket
from app.services.auth_service import redis_client

class ConnectionManager:
    def __init__(self):
        # Maps worker_id to their active WebSocket connection
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, worker_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[worker_id] = websocket

    def disconnect(self, worker_id: str):
        if worker_id in self.active_connections:
            del self.active_connections[worker_id]

    async def send_personal_message(self, message: dict, worker_id: str):
        if worker_id in self.active_connections:
            websocket = self.active_connections[worker_id]
            try:
                await websocket.send_json(message)
            except Exception:
                self.disconnect(worker_id)

manager = ConnectionManager()

async def listen_to_redis_channel():
    """Background task to listen for job dispatches via Redis Pub/Sub."""
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("job_dispatch")
    
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                worker_id = data.get("worker_id")
                if worker_id:
                    await manager.send_personal_message(data, worker_id)
    except Exception as e:
        print(f"Redis PubSub Listener Error: {e}")
        # In a real app, add retry/backoff logic here.
