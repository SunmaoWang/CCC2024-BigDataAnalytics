# CCC2024 Big Data Analytics

## Overview

Welcome to the CCC2024 Big Data Analytics project! This project is designed to analyze big data related to chronic diseases, population and air pollution, also demographic distributions using data analytics and machine learning and other visualization techniques. Our system integrates multiple components including backend services, databases, and frontend, all orchestrated with Kubernetes.

## Project Structure

- **README.md** - This file, containing documentation for the project.
- **backend/** - Contains all backend scripts including RESTful APIs and data querying modules.
- **data/** - Directory for raw/preprocessed data and data processing scripts.
- **database/** - Scripts and files related to database setup and maintenance.
- **docs/** - Documentation files and additional resources.
- **frontend/** - Frontend Jupyter Notebook files for visualization and interaction.
- **test/** - Test scripts and test data for validating the application components.

## Prerequisites

Before setting up the project, ensure you have the following installed:
- Kubernetes
- Python 3.8+
- Elasticsearch / Kibana / Fission
- Required Python packages: `requirements.txt`

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SunmaoWang/CCC2024-BigDataAnalytics.git
   cd CCC2024-BigDataAnalytics

## Elastic Search Indexes

Select functions contained in the backend folder are utilised to create Elastic Search indexes. These are then used to store data harvested from other select functions contained in the backend folder.

Some examples of Elastic Search indices are:

- **population2021:** Index to store population data for each LGA.

- **useful:** Index to store LGA shapefiles in a more useful, preprocessed, format.

- **environmental_data_lga:** Index to store air pollution data for each monitoring station.

- **chronic_diseases_epa:** Index to store both air pollution data and chronic disease data for each LGA together, utilising a parent child relationship.

## RESTful API

Select functions contained in the backend folder are utilised to implement a RESTful API using Fission. This API is used by the front end to request relevant data.

Some examples of HTTP triggers are:

- **/chronicepa79:** Returns the latest epa reading for all air monitoring stations, joined with their respective lga's chronic disease data.

- **/chronicepa79/{lga}:** Same as \textbf{/chronicepa79}, but filtered for a specific lga.

- **/populationepalga:** Returns all lga's population data.

- **/populationepalga/{lga}:** Same as \textbf{/populationepalga}, but filtered for a specific lga.

- **/airpol**: Returns latest air pollution data from all stations.

## Automated Data Harvesters

Select functions contained in the backend folder are utilised to implement an automated data harvester, specifically for air pollution data from the EPA, using Fission. This is performed every hour, with the tata being indexed appropriately. 
