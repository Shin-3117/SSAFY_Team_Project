from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        print('test start')
    
    # @task
    # def load_csv(self):
    #     self.client.get("test/load_csv/")
    
    # @task
    # def handle_missing_data(self):
    #     self.client.get("test/handle_missing_data/")
    
    @task
    def test(self):
        self.client.get("market/send_data/kospi/")