from locust import HttpUser, task, between


TOKEN = "Bearer your_user_token"


class TimelineUser(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def read_from_db(self):
        self.client.get(
            "/api/v1/tweets/db/timeline?limit=10&offset=0",
            headers={"Authorization": TOKEN}
        )

    @task(1)
    def read_from_cache(self):
        self.client.get(
            "/api/v1/tweets/cache/timeline?limit=10&offset=0",
            headers={"Authorization": TOKEN}
        )
