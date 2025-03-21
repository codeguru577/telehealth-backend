from flask import Flask, request, jsonify
from models import db, Patient
from auth import token_required
from tasks import send_notification
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create Database Tables
with app.app_context():
    db.create_all()

# Endpoints
@app.route('/patients', methods=['POST'])
@token_required
def create_patient():
    data = request.json
    
    required_fields = ['name', 'phone', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    existing_patient = Patient.query.filter(
        (Patient.phone == data['phone']) | (Patient.email == data['email'])
    ).first()

    if existing_patient:
        return jsonify({"error": "Patient with this phone or email already exists"}), 409


    patient = Patient(id=str(uuid.uuid4()), name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(patient)
    db.session.commit()

    # Trigger Celery task
    send_notification.delay(patient.phone)

    return jsonify({"message": "Patient created successfully", "patient_id": patient.id}), 201

@app.route('/patients/<patient_id>', methods=['GET'])
@token_required
def get_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        return jsonify({"id": patient.id, "name": patient.name, "email": patient.email, "phone": patient.phone})
    return jsonify({"message": "Patient not found"}), 404

@app.route('/patients/<patient_id>', methods=['PUT'])
@token_required
def update_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    data = request.json
    patient.name = data.get('name', patient.name)
    patient.email = data.get('email', patient.email)
    patient.phone = data.get('phone', patient.phone)
    db.session.commit()

    # Trigger Celery task
    send_notification.delay(patient.phone)

    return jsonify({"message": "Patient updated successfully"})

@app.route('/patients/<patient_id>', methods=['DELETE'])
@token_required
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"message": "Patient not found"}), 404

    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted successfully"})

@app.route('/patients', methods=['GET'])
@token_required
def get_all_patients():
    patients = Patient.query.all()
    return jsonify([{"id": p.id, "name": p.name, "email": p.email, "phone": p.phone} for p in patients])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)