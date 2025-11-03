from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column,relationship
from ..db import db
from datetime import datetime
from sqlalchemy import ForeignKey




class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str] = mapped_column(nullable=False)
    description:Mapped[str] = mapped_column(nullable=False)
    completed_at:Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")


    # Method to convert Task instance to dictionary
    def to_dict(self) :
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
            # "goal_id": self.goal_id
        }
        if hasattr(self, 'goal_id') and self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    # Class method to create Task instance from dictionary
    @classmethod
    def from_dict(cls, data):

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