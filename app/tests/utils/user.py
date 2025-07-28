from app.core.config import settings


def authentication_token_from_email(*, client, email, session) -> dict[str, str]:
    data = {"username": email, "password": ""}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    return {"Authorization": f"Bearer {auth_token}"}
