from sqlalchemy.orm import Mapped, mapped_column,relationship
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    # Convert Goal instance to dictionary
    def to_dict(self) :
        goal_dict = {
            "id": self.id,
            "title": self.title
        }

        if hasattr(self, 'tasks') and self.tasks:
            goal_dict["task_ids"] = [task.id for task in self.tasks]

        return goal_dict


    # Convert dictionary to Goal instance
    @classmethod    
    def from_dict(cls, data):
        if 'title' not in data:
            raise KeyError('title') 
        return cls(
            title=data['title'],
        )
