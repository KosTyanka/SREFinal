from locust import HttpUser, task, between

class ConcertUser(HttpUser):
    wait_time = between(1, 3)  # Random wait between requests
    
    @task(3)
    def view_concerts(self):
        self.client.get("/concerts")
    
    @task(2)
    def health_check(self):
        self.client.get("/health")
    
    @task(1)
    def book_ticket(self):
        concert_id = 1  # Example concert ID
        self.client.post("/book-ticket", 
            json={
                "concert_id": concert_id,
                "quantity": 1,
                "user_email": "test@example.com"
            }
        ) 