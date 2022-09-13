from locust import HttpUser, task, between, constant, SequentialTaskSet

class QuickstartUser(HttpUser):

    def __init__(self, parent):
        super(QuickstartUser, self).__init__(parent)
        self.token = ""

    wait_time = between(1, 2)

    @task
    def index_page(self):
        self.client.get("/")

    @task(3)
    def view_item(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")

    def on_start(self):
        with self.client.get(url="/login") as response:
            self.token = response.json()["token"]

class MyScript(SequentialTaskSet):

    # def __init__(self, parent):
    #     super().__init__(parent)
    #     self.test_data = CsvRead("DataParameterization\\customer-data.csv").read()

        @task
        def place_order(self):
            test_data = CsvRead("DataParameterization\\customer-data.csv").read()
            print(test_data)

            data = {
                "custname": test_data['name'],
                "custtel": test_data['phone'],
                "custemail": test_data['email'],
                "size": test_data['size'],
                "topping": test_data['toppings'],
                "delivery": test_data['time'],
                "comments": test_data['instructions']
            }

            name = "Order for " + test_data['name']

            with self.client.post("/post", catch_response=True, name=name, data=data) as response:
                if response.status_code == 200 and test_data['name'] in response.text:
                    response.success()
                else:
                    response.failure("Failure in processing the order")


class MyLoadTest(HttpUser):
    host = "https://httpbin.org"
    wait_time = constant(1)
    tasks = [MyScript]
