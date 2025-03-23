import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="spatialdb",
            user="root",
            password="******",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise e


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Enable PostGIS extension if not enabled
    cur.execute("""
        CREATE EXTENSION IF NOT EXISTS postgis;
    """)

    # Create spatial_points table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS spatial_points (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            location GEOMETRY(Point, 4326)
        );
    """)

    # Create spatial index for points
    cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_spatial_points_location 
            ON spatial_points 
            USING GIST(location);
        """)

    # Create spatial_polygons table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS spatial_polygons (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            area GEOMETRY(Polygon, 4326)
        );
    """)

    # Create spatial index for polygons
    cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_spatial_polygons_area 
            ON spatial_polygons 
            USING GIST(area);
        """)

    conn.commit()
    cur.close()
    conn.close()