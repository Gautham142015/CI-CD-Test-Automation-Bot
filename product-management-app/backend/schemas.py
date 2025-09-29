from pydantic import BaseModel

class TaskBase(BaseModel):
    description: str
    type: str
    priority: str
    user_story: str
    acceptance_criteria: str

class TaskCreate(TaskBase):
    pass

class TextInput(BaseModel):
    text: str

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
