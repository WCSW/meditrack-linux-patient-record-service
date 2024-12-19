import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Database Configuration
DB_CONFIG = {
    "host": "meditrack-db2.cloiwow0uz31.ap-south-1.rds.amazonaws.com",
    "database": "meditrack-db2",
    "user": "postgres",
    "password": "postgres2025"
}

# Database Connection
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

@app.route("/patient", methods=["POST"])
def create_patient():
    try:
        body = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO patients (id, name, age, diagnosis ) VALUES (%s, %s, %s, %s)",
            (body["id"], body["name"], body["age"], body["diagnosis"])
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Patient created", "id": body["id"]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/patient/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        patient = cur.fetchone()
        cur.close()
        conn.close()
        if patient:
            return jsonify({"id": patient[0], "name": patient[1], "age": patient[2], "diagnosis": patient[3]}), 200
        else:
            return jsonify({"error": "Patient not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/patient/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    try:
        body = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE patients SET name = %s, age = %s, diagnosis = %s WHERE id = %s",
            (body["name"], body["age"], body["diagnosis"], patient_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Patient updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/patient/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Patient deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
