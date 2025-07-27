import uuid
from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, max_length=50)
    email: EmailStr = Field(index=True, unique=True, max_length=255)


# class Tweet(SQLModel):
#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     content: str = Field(max_length=280)
#     user_id: uuid.UUID = Field(foreign_key="user.id")


# class Follow(SQLModel):
#     follower_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)
#     followed_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)

#     user: User = Field(sa_relationship_kwargs={"lazy": "joined"})
#     followed_user: User = Field(sa_relationship_kwargs={"lazy": "joined"})
