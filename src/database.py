from settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from models.orm import Base

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.PG_USER}:{settings.PG_PASSWORD}"
    f"@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_NAME}"
)

# Create async SQL DB
engine = create_async_engine(DATABASE_URL, echo=False)

SessionLocal = async_sessionmaker[AsyncSession](
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(f"Database '{settings.PG_NAME}' initialized")

async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print(f"All tables from '{settings.PG_NAME}' database removed")

# Hard
async def recreate_db():
    await drop_all_tables()
    await init_db()
