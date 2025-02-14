from redis.asyncio import Redis
from typing import List
from ..models.User import User
import json

redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)


async def set_users(users: List[User]):
    await redis_client.setex("users", 3600, json.dumps([
        {"id": user.id, "name": user.name, "email": user.email} for user in users
    ]))


async def get_users() -> List[User]:
    users_slz = await redis_client.get("users")
    if users_slz:
        users_data = json.loads(users_slz)  # Deserialize JSON
        return [User(id=user["id"], name=user["name"], email=user["email"]) for user in users_data]
    return []


async def update_cache(id: int=None, user:User=None):
    users = await get_users()
    updated_users: List[User] = None
    if user:  # If a new user is provided, update the existing user in the list
        updated_users = [
            u if u.id != id else user for u in users
        ]
    if id is None and user is not None:
        users.append(user)
        updated_users = users
    elif id is not None and user is None:  # If no user is provided, remove the user from the cache
        updated_users = [u for u in users if u.id != id]
    await set_users(updated_users)
