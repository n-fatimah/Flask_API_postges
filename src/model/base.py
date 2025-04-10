from __future__ import annotations

import hashlib
from datetime import datetime, timedelta
from typing import Union

import jwt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from config import settings

db = SQLAlchemy(session_options={"autoflush": False})


@as_declarative()
class Base(object):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True
    )

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate __tablename__ automatically

        Returns:
            Table name
        """
        return cls.__name__.lower()

    def insert(self) -> Base:
        """
        Insert

        Returns:
            Base
        """
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self) -> Base:
        """
        Delete

        Returns:
            Base
        """
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def update(cls, id: int, to_update: dict) -> None:
        """
        Update row by id

        Args:
            id: id to update data
            to_update: dictionary to update data
            session: Defaults to None.
        """
        db.session.query(cls).filter(cls.id == id).update(to_update)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id: int) -> Union[Base, None]:
        """
        Get by id

        Args:
            id: fetch row by id
            session: Defaults to None.

        Returns:
            Row from database
        """
        row = db.session.query(cls).filter_by(id=id).first()
        return row

    @classmethod
    def list(cls, page: int, per_page: int) -> Union[Base, None]:
        """
        List all rows

        Args:
            session: Defaults to None.

        Returns:
            All rows
        """
        return db.session.query(cls).offset((page - 1) * per_page).limit(per_page).all()
