#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Base URL
API_URL="http://localhost:8000"

# Function to run test and save results
run_test() {
    local scenario=$1
    local requests=$2
    local concurrency=$3
    local endpoint=$4
    
    echo -e "${BLUE}Running $scenario${NC}"
    echo "Requests: $requests, Concurrency: $concurrency"
    echo "Endpoint: $endpoint"
    
    # Run test and save results
    ab -n $requests -c $concurrency "$API_URL$endpoint" > "results_${scenario}.txt"
    
    # Extract key metrics
    rps=$(grep "Requests per second" "results_${scenario}.txt" | awk '{print $4}')
    mean_time=$(grep "Time per request" "results_${scenario}.txt" | head -n 1 | awk '{print $4}')
    p95=$(grep "95%" "results_${scenario}.txt" | awk '{print $2}')
    
    echo -e "${GREEN}Results:${NC}"
    echo "Requests per second: $rps"
    echo "Mean time per request: $mean_time ms"
    echo "95th percentile: $p95 ms"
    echo "----------------------------------------"
}

# Scenario 1: Baseline Load (100 concurrent users)
echo -e "${BLUE}Starting Baseline Load Test${NC}"
run_test "baseline_health" 1000 100 "/health"
run_test "baseline_concerts" 1000 100 "/concerts"

# Scenario 2: Medium Load (500 concurrent users)
echo -e "${BLUE}Starting Medium Load Test${NC}"
run_test "medium_health" 5000 500 "/health"
run_test "medium_concerts" 5000 500 "/concerts"

# Scenario 3: High Load (1000 concurrent users)
echo -e "${BLUE}Starting High Load Test${NC}"
run_test "high_health" 10000 1000 "/health"
run_test "high_concerts" 10000 1000 "/concerts"

# Scenario 4: Spike Test (2000 concurrent users, short burst)
echo -e "${BLUE}Starting Spike Test${NC}"
run_test "spike_health" 5000 2000 "/health"
run_test "spike_concerts" 5000 2000 "/concerts"

# Create summary report
echo -e "${GREEN}Creating Test Summary Report${NC}"
echo "# Load Test Results Summary" > test_summary.md
echo "## Test Scenarios and Results" >> test_summary.md
echo "### Environment" >> test_summary.md
echo "- Date: $(date)" >> test_summary.md
echo "- Backend URL: $API_URL" >> test_summary.md
echo "- Docker Resources: Default configuration" >> test_summary.md

for scenario in baseline medium high spike; do
    echo "### ${scenario^} Load Test Results" >> test_summary.md
    echo "\`\`\`" >> test_summary.md
    echo "Health Endpoint:" >> test_summary.md
    grep -A 15 "Requests per second" "results_${scenario}_health.txt" >> test_summary.md
    echo -e "\nConcerts Endpoint:" >> test_summary.md
    grep -A 15 "Requests per second" "results_${scenario}_concerts.txt" >> test_summary.md
    echo "\`\`\`" >> test_summary.md
done

echo -e "${GREEN}Load testing completed. Results saved in test_summary.md${NC}" 