import os
import uuid
from typing import List, Optional

from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

__package__ = "DB.engine"

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    uploads: Mapped[List["Upload"]] = relationship("Upload", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Upload(Base):
    __tablename__ = 'uploads'

    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    upload_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    finish_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")

    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))
    user: Mapped[Optional["User"]] = relationship("User", back_populates="uploads")

    def __repr__(self):
        return f"<Upload(id={self.id}, uid={self.uid},\
         filename={self.filename}, upload_time={self.upload_time},\
          finish_time={self.finish_time}, status={self.status},\
           user_id={self.user_id})>"


DIR = os.path.dirname(__file__)
engine = create_engine(f'sqlite:///{DIR}/db.sqlite3', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

