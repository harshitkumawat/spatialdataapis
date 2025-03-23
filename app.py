from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from db_config import get_db_connection, init_db

app = Flask(__name__)


# Point endpoints
@app.route('/api/points', methods=['POST'])
def create_point():
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            INSERT INTO spatial_points (name, description, location)
            VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
            RETURNING id;
        """, (
            data['name'],
            data.get('description', ''),
            data['longitude'],
            data['latitude']
        ))

        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Point created successfully', 'id': result['id']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/points/<int:point_id>', methods=['PUT'])
def update_point(point_id):
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        update_parts = []
        values = []

        if 'name' in data:
            update_parts.append("name = %s")
            values.append(data['name'])

        if 'description' in data:
            update_parts.append("description = %s")
            values.append(data['description'])

        if 'longitude' in data and 'latitude' in data:
            update_parts.append("location = ST_SetSRID(ST_MakePoint(%s, %s), 4326)")
            values.extend([data['longitude'], data['latitude']])

        if update_parts:
            values.append(point_id)
            query = f"""
                UPDATE spatial_points
                SET {', '.join(update_parts)}
                WHERE id = %s
            """
            cur.execute(query, values)

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Point updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/point/<int:point_id>', methods=['DELETE'])
def delete_point(point_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        values = []
        values.append(point_id)
        query = """
            DELETE from spatial_points WHERE id = %s
        """
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Point Deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/points', methods=['GET'])
def get_points():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT 
                id,
                name,
                description,
                ST_X(location::geometry) as longitude,
                ST_Y(location::geometry) as latitude
            FROM spatial_points;
        """)

        points = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify(points)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Polygon endpoints
@app.route('/api/polygons', methods=['POST'])
def create_polygon():
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Convert coordinates to WKT format
        coordinates = data['coordinates'][0]
        wkt = f"POLYGON(({','.join([f'{x} {y}' for x, y in coordinates])}))"

        cur.execute("""
            INSERT INTO spatial_polygons (name, description, area)
            VALUES (%s, %s, ST_SetSRID(ST_GeomFromText(%s), 4326))
            RETURNING id;
        """, (
            data['name'],
            data.get('description', ''),
            wkt
        ))

        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Polygon created successfully', 'id': result['id']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/polygons/<int:polygon_id>', methods=['PUT'])
def update_polygon(polygon_id):
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        update_parts = []
        values = []

        if 'name' in data:
            update_parts.append("name = %s")
            values.append(data['name'])

        if 'description' in data:
            update_parts.append("description = %s")
            values.append(data['description'])

        if 'coordinates' in data:
            coordinates = data['coordinates'][0]
            wkt = f"POLYGON(({','.join([f'{x} {y}' for x, y in coordinates])}))"
            update_parts.append("area = ST_SetSRID(ST_GeomFromText(%s), 4326)")
            values.append(wkt)

        if update_parts:
            values.append(polygon_id)
            query = f"""
                UPDATE spatial_polygons
                SET {', '.join(update_parts)}
                WHERE id = %s
            """
            cur.execute(query, values)

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Polygon updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/polygons', methods=['GET'])
def get_polygons():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT 
                id,
                name,
                description,
                ST_AsGeoJSON(area)::json->'coordinates' as coordinates
            FROM spatial_polygons;
        """)

        polygons = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify(polygons)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/polygon/<int:point_id>', methods=['DELETE'])
def delete_polygon(point_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        values = []
        values.append(point_id)
        query = """
            DELETE from spatial_polygons WHERE id = %s
        """
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Polygon Deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    init_db()
    app.run(debug=True)