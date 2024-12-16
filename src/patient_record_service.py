import json

# Simulated in-memory database
PATIENT_RECORDS = {}

def lambda_handler(event, context):
    try:
        http_method = event.get("httpMethod")
        if http_method == "POST":
            return create_patient(event)
        elif http_method == "GET":
            return get_patient(event)
        elif http_method == "PUT":
            return update_patient(event)
        elif http_method == "DELETE":
            return delete_patient(event)
        else:
            return {"statusCode": 405, "body": json.dumps("Method Not Allowed")}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(str(e))}

def create_patient(event):
    body = json.loads(event["body"])
    patient_id = body["id"]
    PATIENT_RECORDS[patient_id] = body
    return {"statusCode": 201, "body": json.dumps({"message": "Patient created", "id": patient_id})}

def get_patient(event):
    patient_id = event["queryStringParameters"]["id"]
    patient = PATIENT_RECORDS.get(patient_id)
    if patient:
        return {"statusCode": 200, "body": json.dumps(patient)}
    else:
        return {"statusCode": 404, "body": json.dumps({"message": "Patient not found"})}

def update_patient(event):
    body = json.loads(event["body"])
    patient_id = body["id"]
    if patient_id in PATIENT_RECORDS:
        PATIENT_RECORDS[patient_id] = body
        return {"statusCode": 200, "body": json.dumps({"message": "Patient updated"})}
    else:
        return {"statusCode": 404, "body": json.dumps({"message": "Patient not found"})}

def delete_patient(event):
    patient_id = event["queryStringParameters"]["id"]
    if patient_id in PATIENT_RECORDS:
        del PATIENT_RECORDS[patient_id]
        return {"statusCode": 200, "body": json.dumps({"message": "Patient deleted"})}
    else:
        return {"statusCode": 404, "body": json.dumps({"message": "Patient not found"})}
