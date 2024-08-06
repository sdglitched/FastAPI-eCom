from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from fastapi_ecom import db_creds as dbc

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{dbc.user}:{dbc.password}@localhost:5432/{dbc.name}"

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()
