#!/bin/bash

# Install required packages from requirements.txt
pip install -r requirements.txt

# Start the docker-compose services
docker-compose up -d

# Wait for 2 minutes
echo "Waiting for 2 minutes..."
sleep 120

# Execute the databaseCreation.py code
echo "Creating the database..."
python3 databaseCreation.py

# Wait for an additional 30 seconds
echo "Waiting for 30 seconds..."
sleep 30

# Execute the scrapy crawl madrid_routes command
echo "Starting crawling spider for madrid routes..."
scrapy crawl madrid_routes
