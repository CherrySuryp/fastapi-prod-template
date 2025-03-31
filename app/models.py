from sqlalchemy import orm

from app.database import Base


class TestModel(Base):
    __tablename__ = "test"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
