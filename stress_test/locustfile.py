from locust import HttpUser, between, task
import os

class APIUser(HttpUser):
    wait_time = between(1, 5)

    # Put your stress tests here.
    # See https://docs.locust.io/en/stable/writing-a-locustfile.html for help.
    # TODO

    @task
    def index(self):
        self.client.get("http://localhost/")

    @task
    def indexpost(self):
        self.client.post("http://localhost/")

    @task
    def predict(self):
        file_path = os.path.join(os.path.dirname(__file__),'dog.jpeg')
        with open(file_path,'rb') as f:
            files = {'file': ('dog.jpeg', f, 'image/jpeg')}
            headers = {}
            payload = {}
        
            self.client.post("http://localhost/predict",
                            data = payload,
                            files= files,
                            headers= headers
                            )

    # raise NotImplementedError
