import asyncpg
from config import DATABASE_URL


async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            full_name TEXT,
            status TEXT
        );
    """)
    await conn.close()


async def get_user(user_id):
    conn = await asyncpg.connect(DATABASE_URL)
    user = await conn.fetchrow(
        "SELECT * FROM users WHERE id=$1",
        user_id
    )
    await conn.close()
    return user


async def add_user(user_id, full_name):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(
        "INSERT INTO users(id, full_name, status) VALUES($1,$2,$3)",
        user_id, full_name, "pending"
    )
    await conn.close()


async def update_status(user_id, status):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(
        "UPDATE users SET status=$1 WHERE id=$2",
        status, user_id
    )
    await conn.close()