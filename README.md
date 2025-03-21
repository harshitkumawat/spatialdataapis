# Spatial Data Platform API

This is a Flask-based REST API for handling spatial data (points and polygons) using PostgreSQL with PostGIS extension.

## Prerequisites

1. PostgreSQL with PostGIS extension installed
2. Python 3.7+
3. Required Python packages (install using `pip install -r requirements.txt`)

## Database Setup

1. Create a PostgreSQL database:
```sql
CREATE DATABASE spatial_db;
```

2. Enable PostGIS extension:
```sql
\c spatial_db
CREATE EXTENSION postgis;
```

## API Endpoints

### Points

- **POST /api/points**
  - Create a new point
  - Body: 
    ```json
    {
      "name": "Location Name",
      "description": "Location Description",
      "longitude": -73.935242,
      "latitude": 40.730610
    }
    ```

- **PUT /api/points/<point_id>**
  - Update an existing point
  - Body: Same as POST (all fields optional)

- **GET /api/points**
  - Retrieve all points

### Polygons

- **POST /api/polygons**
  - Create a new polygon
  - Body:
    ```json
    {
      "name": "Area Name",
      "description": "Area Description",
      "coordinates": [
        [
          [-73.935242, 40.730610],
          [-73.935242, 40.731610],
          [-73.934242, 40.731610],
          [-73.934242, 40.730610],
          [-73.935242, 40.730610]
        ]
      ]
    }
    ```

- **PUT /api/polygons/<polygon_id>**
  - Update an existing polygon
  - Body: Same as POST (all fields optional)

- **GET /api/polygons**
  - Retrieve all polygons

## Running the Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

## Running Tests

```bash
python -m pytest
```
