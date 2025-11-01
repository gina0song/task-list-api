from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str] = mapped_column(nullable=False)
    description:Mapped[str] = mapped_column(nullable=False)
    completed_at:Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)


    # Method to convert Task instance to dictionary
    def to_dict(self) :
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
        return task_dict

    # Class method to create Task instance from dictionary
    @classmethod
    def from_dict(cls, data: dict):

        # Validation for 'title' and 'description': Raises KeyError if missing.
        
        if 'title' not in data:
            raise KeyError('title is required') 
        if 'description' not in data:
            raise KeyError('description is required')

        return cls(
            title=data.get("title"),
            description=data.get("description"),
            completed_at=data.get("completed_at")
        )