from sqlalchemy.orm import DeclarativeBase


class OrmBase(DeclarativeBase):
    def __repr__(self) -> str:
        column_values = ", ".join(
            f"{column.name}={getattr(self, column.name)!r}"
            for column in self.__table__.columns
        )
        return f"<{self.__class__.__name__}({column_values})>"
