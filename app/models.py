import uuid
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, max_length=50)
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    username: str = Field(max_length=50)
    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)


# Database model for User
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    tweets: list["Tweet"] = Relationship(back_populates="owner", cascade_delete=True)


class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    users: list[UserPublic]
    count: int


class TweetBase(SQLModel):
    title: str = Field(min_length=1, max_length=50)
    content: str = Field(max_length=255)


class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    owner: User = Relationship(back_populates="tweets")


class TweetPublic(TweetBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class TweetsPublic(SQLModel):
    tweets: list[TweetPublic]
    count: int


class TokenPayload(SQLModel):
    sub: str | None = None


class Token(SQLModel):
    access_token: str
