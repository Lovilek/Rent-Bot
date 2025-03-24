import aiosqlite

async def search_apartments(city: str, max_price: int, min_rooms: int):
    from database.db import DB_PATH

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute('''
            SELECT * FROM apartments
            WHERE city = ?
            AND price <= ?
            AND rooms >= ?
            ORDER BY created_at DESC
        ''', (city, max_price, min_rooms))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
