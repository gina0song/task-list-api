from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)

    def to_dict(self) -> dict:       
        return {
            "id": self.id,
            "title": self.title
        }                                   
    @classmethod    
    def from_dict(cls, data):
        if 'title' not in data:
            raise KeyError('title') 
        return cls(
            title=data['title'],
        )
