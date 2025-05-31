#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Function to modify docker-compose resources
update_resources() {
    local scenario=$1
    local backend_cpu=$2
    local backend_memory=$3
    local replicas=$4

    # Create scenario-specific docker-compose override
    cat > docker-compose.${scenario}.yml <<EOF
version: '3.8'

services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '${backend_cpu}'
          memory: ${backend_memory}
      replicas: ${replicas}
    environment:
      - SCENARIO=${scenario}

  db:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
EOF

    echo -e "${GREEN}Created docker-compose.${scenario}.yml with:${NC}"
    echo "- CPU: ${backend_cpu}"
    echo "- Memory: ${backend_memory}"
    echo "- Replicas: ${replicas}"
}

# Function to run scenario
run_scenario() {
    local scenario=$1
    local duration=$2

    echo -e "${BLUE}Running ${scenario} scenario for ${duration} seconds${NC}"
    
    # Start services with scenario config
    docker-compose -f docker-compose.yml -f docker-compose.${scenario}.yml up -d
    
    # Wait for services to stabilize
    sleep 10
    
    # Run load test
    ./run_load_test.sh ${scenario}
    
    # Collect metrics for duration
    echo -e "${BLUE}Collecting metrics for ${duration} seconds...${NC}"
    sleep $duration
    
    # Save container stats
    docker stats --no-stream > "results_${scenario}_stats.txt"
    
    # Stop services
    docker-compose -f docker-compose.yml -f docker-compose.${scenario}.yml down
    
    echo -e "${GREEN}Completed ${scenario} scenario${NC}"
}

# Create scenarios
echo -e "${BLUE}Creating test scenarios...${NC}"

# Baseline scenario (1 replica, limited resources)
update_resources "baseline" "1.0" "512M" 1

# Medium load scenario (2 replicas, moderate resources)
update_resources "medium" "2.0" "1G" 2

# High load scenario (3 replicas, higher resources)
update_resources "high" "3.0" "2G" 3

# Spike scenario (5 replicas, maximum resources)
update_resources "spike" "4.0" "4G" 5

# Run scenarios
echo -e "${BLUE}Starting load simulation scenarios...${NC}"

# Run each scenario for 5 minutes
run_scenario "baseline" 300
run_scenario "medium" 300
run_scenario "high" 300
run_scenario "spike" 300

# Generate summary report
echo -e "${BLUE}Generating summary report...${NC}"

echo "# Load Simulation Results" > simulation_summary.md
echo "## Test Scenarios" >> simulation_summary.md

for scenario in baseline medium high spike; do
    echo "### ${scenario^} Scenario Results" >> simulation_summary.md
    echo "#### Container Stats" >> simulation_summary.md
    echo "\`\`\`" >> simulation_summary.md
    cat "results_${scenario}_stats.txt" >> simulation_summary.md
    echo "\`\`\`" >> simulation_summary.md
    
    echo "#### Load Test Results" >> simulation_summary.md
    echo "\`\`\`" >> simulation_summary.md
    cat "results_${scenario}.txt" >> simulation_summary.md
    echo "\`\`\`" >> simulation_summary.md
done

echo -e "${GREEN}Simulation completed. Results saved in simulation_summary.md${NC}" 