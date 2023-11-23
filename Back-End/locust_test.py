from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    # @task
    # def test(self):
    #     self.client.get("market/send_data/kospi/")

    # @task
    # def test(self):
    #     self.client.get("market/send_data/kosdaq/")

    @task
    def test(self):
        self.client.get("market/recommend_data/365/")
