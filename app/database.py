import datetime

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.schema import MetaData

from app.config import config

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",  # Index naming convention
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # Unique constraint naming convention
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # Check constraint naming convention
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # Foreign key naming convention
    "pk": "pk_%(table_name)s",  # Primary key naming convention
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)

engine = create_async_engine(
    config.database_dsn,
    pool_size=config.DATABASE_POOL_SIZE,
    pool_recycle=config.DATABASE_POOL_TTL,
    pool_pre_ping=config.DATABASE_POOL_PRE_PING,
)
if config.ENV.is_testing:
    engine = create_async_engine(config.database_dsn, poolclass=sa.NullPool)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    metadata = metadata
    type_annotation_map = {
        int: sa.Integer,
        str: sa.String,
        float: sa.Float,
        bool: sa.Boolean,
        bytes: sa.LargeBinary,
        dict: sa.JSON,
        list: sa.ARRAY,
        datetime.datetime: sa.types.DateTime,
    }
