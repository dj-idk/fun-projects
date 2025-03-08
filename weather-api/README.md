# Weather App with FastAPI and Redis Caching

This project provides a weather app that uses FastAPI as the backend to fetch weather data from OpenWeatherMap and Redis for caching to improve performance and reduce redundant API calls.

## Features

- Fetch weather data by city and optional country.
- Displays temperature, condition, wind speed, and humidity.
- Caching with Redis to speed up data retrieval.
- Frontend built with simple HTML and JavaScript.

## Tech Stack

- **Backend**: FastAPI
- **Caching**: Redis
- **Frontend**: HTML, JavaScript

## Setup Instructions

### Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.7+
- Redis server
- FastAPI
- Uvicorn (ASGI server)
- Redis-py

### Backend API

The backend provides an endpoint to get weather information for a specified city and country.

- **Endpoint**: `/weather/{city}`
- **Query Parameters**:
  - `city`: Name of the city (required).
  - `country`: Name of the country (optional).
