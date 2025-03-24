import aiosqlite

DB_PATH = "rent.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS apartments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            city TEXT,
            price INTEGER,
            rooms INTEGER,
            address TEXT,
            phone TEXT,
            description TEXT,
            photo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        await db.commit()

async def insert_apartment(apartment):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT INTO apartments (user_id, city, price, rooms, address, phone, description, photo)
            VALUES (?, ?, ?, ?, ?, ?,?,?)
        ''', (
            apartment.user_id,
            apartment.city,
            apartment.price,
            apartment.rooms,
            apartment.address,
            apartment.phone,
            apartment.description,
            apartment.photo
        ))
        await db.commit()

async def get_user_apartments(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute('''
            SELECT * FROM apartments WHERE user_id = ? ORDER BY created_at DESC
        ''', (user_id,))
        return [dict(row) for row in await cursor.fetchall()]

async def delete_apartment_by_id(apartment_id: int, user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM apartments WHERE id = ? AND user_id = ?",
            (apartment_id, user_id)
        )
        await db.commit()
        return cursor.rowcount > 0
