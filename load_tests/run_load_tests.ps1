# Load Testing Script using Apache Benchmark
$API_ENDPOINT="http://localhost:8000"

Write-Host "Starting Load Tests..."

# Scenario 1: Baseline Performance (50 concurrent users, 1000 requests)
Write-Host "`nRunning Baseline Test..."
ab -n 1000 -c 50 "$API_ENDPOINT/health"
ab -n 1000 -c 50 "$API_ENDPOINT/concerts"

# Scenario 2: Medium Load (200 concurrent users, 5000 requests)
Write-Host "`nRunning Medium Load Test..."
ab -n 5000 -c 200 "$API_ENDPOINT/health"
ab -n 5000 -c 200 "$API_ENDPOINT/concerts"

# Scenario 3: High Load (500 concurrent users, 10000 requests)
Write-Host "`nRunning High Load Test..."
ab -n 10000 -c 500 "$API_ENDPOINT/health"
ab -n 10000 -c 500 "$API_ENDPOINT/concerts"

Write-Host "`nLoad Testing Complete!" 