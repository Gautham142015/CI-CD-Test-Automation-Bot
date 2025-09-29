from sqlalchemy import Column, Integer, String
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    type = Column(String)
    priority = Column(String)
    user_story = Column(String)
    acceptance_criteria = Column(String)
