from sqlmodel import Session, create_engine

from app.core.config import settings


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    """
    Initialize the database by creating all tables.
    This function should be called at the start of the application.
    """
    # SQLModel.metadata.create_all(engine)
