from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated in-memory database
PATIENT_RECORDS = {}

@app.route("/patient", methods=["POST"])
def create_patient():
    try:
        body = request.get_json()
        patient_id = body["id"]
        PATIENT_RECORDS[patient_id] = body
        return jsonify({"message": "Patient created", "id": patient_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/patient", methods=["GET"])
def get_patient():
    try:
        patient_id = request.args.get("id")
        patient = PATIENT_RECORDS.get(patient_id)
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({"message": "Patient not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/patient", methods=["PUT"])
def update_patient():
    try:
        body = request.get_json()
        patient_id = body["id"]
        if patient_id in PATIENT_RECORDS:
            PATIENT_RECORDS[patient_id] = body
            return jsonify({"message": "Patient updated"}), 200
        else:
            return jsonify({"message": "Patient not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/patient", methods=["DELETE"])
def delete_patient():
    try:
        patient_id = request.args.get("id")
        if patient_id in PATIENT_RECORDS:
            del PATIENT_RECORDS[patient_id]
            return jsonify({"message": "Patient deleted"}), 200
        else:
            return jsonify({"message": "Patient not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)