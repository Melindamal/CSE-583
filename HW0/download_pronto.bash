#!/bin/bash

# Make a directory called pronto
mkdir -p pronto

# Create a README.txt in pronto that explains the data
echo "Pronto Cycle Share (Seattle) open data from its first year of operation: trip, station, and weather data." > pronto/README.txt

# Make a sub-directory called data inside pronto
mkdir -p pronto/data

# Download the Pronto bike data into the data directory
curl -o pronto/data/open_data_year_one.zip https://s3.amazonaws.com/pronto-data/open_data_year_one.zip

# Unzip the file into the data directory
unzip -o pronto/data/open_data_year_one.zip -d pronto/data

# Show the first few lines of the 2015 trip data
head pronto/data/2015_trip_data.csv
