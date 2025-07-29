import logging
import random
import string
import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000/api/v1"


def get_random_string(n: int) -> str:
    return "".join(random.choices(string.ascii_letters, k=n))


def random_email():
    return f"{get_random_string(5)}@{get_random_string(5)}.com"


def create_user(username: str, email: str, password: str):
    requests.post(f"{API_URL}/users", json={
        "username": username,
        "email": email,
        "password": password
    })
    logger.info(f"User created: {username}")


def login(username: str, password: str):
    response = requests.post(f"{API_URL}/auth/login/access-token", data={"username": username, "password": password})
    token = response.json()["access_token"]
    logger.info(f"Logged in as {username} with token: {token}")
    return token


def create_tweet(title: str, content: str, token: str):
    requests.post(f"{API_URL}/tweets", json={"title": title, "content": content}, headers={"Authorization": f"Bearer {token}"})
    logger.info(f"Tweet created: {title}")


def generate_data():
    for _ in range(100):
        user_data = {"username": get_random_string(10), "email": random_email(), "password": get_random_string(8)}
        create_user(**user_data)
        token = login(user_data["username"], user_data["password"])

        for _ in range(random.randint(10, 100)):
            create_tweet(title=get_random_string(15), content=get_random_string(15), token=token)

    logger.info(f"✅ Done.")


def main():
    logger.info("Initializing service")
    logger.info("🚀 Starting data generation...")
    generate_data()
    logger.info("🎉 Done.")
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
