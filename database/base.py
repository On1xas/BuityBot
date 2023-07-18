from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker,  AsyncSession
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


async def async_create_engine(
    driver: str,
    host: str,
    port: str,
    username: str,
    password: str,
    database: str
) -> AsyncSession:
    engine = create_async_engine(
        url=f"{driver}://{username}:{password}@{host}:{port}/{database}",
        echo=False
    )
    session = async_sessionmaker(engine, expire_on_commit=False)
    return session

class BaseModel:
    pass