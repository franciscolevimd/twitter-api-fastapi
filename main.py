# Python
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional
from typing import List

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from fastapi import Path
from fastapi import HTTPException


app = FastAPI()


# Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(
        ...,
        example="arisaurio@gmail.com"
    )


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )


class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Arisaurus"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Rex"
    )
    birth_date: Optional[date] = Field(
        default=None,
        example="2005-03-12"
    )


class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        example="Hu729uqp"
    )


class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        max_length=256,
        min_length=1
    )
    created_at: datetime = Field(deafult=datetime.now())
    updated_at: Optional[datetime] = Field(deafult=None)
    by: User = Field(...)


# Path Operations


# ## Users


# ### Register an user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register an user",
    tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
    Signup a User

    This path operation register a user in the app.

    Parameters:
    - Request body parameter
        - user: UserRegister

    Returns a json with the basic user information:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user


# ### Login an user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login an user",
    tags=["Users"]
)
def login():
    pass


# ### Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    Show all Users

    This path operation shows all users in the app

    Parameters:

    Returns a json list with all users in the app, with the following keys:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results


# ### Show an user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show an user",
    tags=["Users"]
)
def show_user(
    user_id: UUID = Path(
        ...,
        title="User ID",
        description="This is the user ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
):
    """
    Show an User

    This path operation show a specific user data.

    Parameters:
    - Path parameter
        - user_id: UUID

    Returns a json with the user information:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    with open("users.json", "r", encoding="utf-8") as f:
        user_id_str = str(user_id)
        users = json.loads(f.read())
        for user in users:
            if user["user_id"] == user_id_str:
                return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user doesn't exist!"
        )


# ### Delete an user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete an user",
    tags=["Users"]
)
def delete_user(
    user_id: UUID = Path(
        ...,
        title="User ID",
        description="This is the user ID",
        example="3fa85f64-5717-4562-b3fc-4c963f88afb0"
    )
):
    """
    Delete an User

    This path operation delete a user of the app.

    Parameters:
    - Path parameter
        - user_id: UUID

    Returns a json with the deleted user information:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        user_id_str = str(user_id)
        users = json.loads(f.read())
        for index in range(len(users)):
            if users[index]["user_id"] == user_id_str:
                result = users.pop(index)
                f.seek(0)
                f.write(json.dumps(users))
                f.truncate()
                return result
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user doesn't exist!"
        )


# ### Update an user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update an user",
    tags=["Users"]
)
def update_user(
    user_id: UUID = Path(
        ...,
        title="User ID",
        description="This is the user ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    ),
    user: User = Body(...)
):
    """
    Update and User

    This path operation update an user information.

    Parameters:
    - Path parameter
        - user_id: UUID
    - Request body parameter
        - user: User

    Returns a json with the updated user information:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        user_id_str = str(user_id)
        users = json.loads(f.read())
        user_dict = user.dict()
        for index in range(len(users)):
            if users[index]["user_id"] == user_id_str:
                users[index]["user_id"] = user_id_str
                users[index]["email"] = user_dict["email"]
                users[index]["first_name"] = user_dict["first_name"]
                users[index]["last_name"] = user_dict["last_name"]
                users[index]["birth_date"] = str(user_dict["birth_date"])
                f.seek(0)
                f.write(json.dumps(users))
                f.truncate()
                return users[index]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This user doesn't exist!"
        )


# ## Tweets


# ### Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
def show_all_tweets():
    """
    Show all Tweets

    This path operation shows all tweets in the app

    Parameters:

    Returns a json list with all tweets in the app, with the following keys:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results


# ### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    Post a Tweet

    This path operation post a tweet in the app.

    Parameters:
    - Request body parameter
        - tweet: Tweet

    Returns a json with the basic tweet information:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        if tweet_dict["updated_at"]:
            tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        if tweet_dict["by"]:
            tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
            tweet_dict["by"]["birth_date"] = str(
                tweet_dict["by"]["birth_date"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet


# ### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_tweet(
    tweet_id: UUID = Path(
        ...,
        title="Tweet ID",
        description="This is the tweet ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
):
    """
    Show a Tweet

    This path operation show a specific tweet.

    Parameters:
    - Path parameter
        - tweet_id: UUID

    Returns a json with the tweet information:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        tweet_id_str = str(tweet_id)
        tweets = json.loads(f.read())
        for tweet in tweets:
            if tweet["tweet_id"] == tweet_id_str:
                return tweet
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This tweet doesn't exist!"
        )


# ### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_tweet(
    tweet_id: UUID = Path(
        ...,
        title="Tweet ID",
        description="This is the tweet ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66af43"
    )
):
    """
    Delete a Tweet

    This path operation delete a tweet.

    Parameters:
    - Path parameter
        - tweet_id: UUID

    Returns a json with the deleted tweet information:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        tweet_id_str = str(tweet_id)
        tweets = json.loads(f.read())
        for index in range(len(tweets)):
            if tweets[index]["tweet_id"] == tweet_id_str:
                result = tweets.pop(index)
                f.seek(0)
                f.write(json.dumps(tweets))
                f.truncate()
                return result
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This tweet doesn't exist!"
        )


# ### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_tweet(
    tweet_id: UUID = Path(
        ...,
        title="Tweet ID",
        description="This is the tweet ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66af43"
    ),
    tweet: Tweet = Body(...)
):
    """
    Update a Tweet


    Parameters:
    - Path parameter
        - tweet_id: UUID
    - Request body parameter
        - tweet: Tweet

    Returns a json with the updated tweet information:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        tweet_id_str = str(tweet_id)
        tweets = json.loads(f.read())
        tweet_dict = tweet.dict()
        for index in range(len(tweets)):
            if tweets[index]["tweet_id"] == tweet_id_str:
                tweets[index]["tweet_id"] = tweet_id_str
                tweets[index]["content"] = tweet_dict["content"]
                tweets[index]["created_at"] = str(tweet_dict["created_at"])
                tweets[index]["updated_at"] = str(tweet_dict["updated_at"])
                tweets[index]["by"] = tweet_dict["by"]
                tweets[index]["by"]["user_id"] = str(
                    tweet_dict["by"]["user_id"])
                tweets[index]["by"]["birth_date"] = str(
                    tweet_dict["by"]["birth_date"])
                f.seek(0)
                f.write(json.dumps(tweets))
                f.truncate()
                return tweets[index]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This tweet doesn't exist!"
        )
