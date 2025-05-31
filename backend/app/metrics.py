from prometheus_client import Counter, Histogram

# Request metrics
request_count = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

request_latency = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
)

# Business metrics
ticket_purchase_count = Counter(
    'ticket_purchases_total',
    'Total number of ticket purchase attempts',
    ['status']  # success or failure
)

tickets_remaining_gauge = Histogram(
    'tickets_remaining',
    'Number of tickets remaining for concerts',
    ['concert_id']
) 