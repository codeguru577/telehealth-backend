from flask_sqlalchemy import SQLAlchemy
import uuid
import re
from sqlalchemy.orm import validates

db = SQLAlchemy()

# Patient Model
class Patient(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    @validates('email')
    def validate_email(self, key, email):
        """Validate email format."""
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise ValueError("Invalid email format")
        return email

    @validates('phone')
    def validate_phone(self, key, phone):
        """Validate phone number format: only numbers and an optional leading '+'."""
        if not re.match(r'^\+?\d+$', phone):  # Only numbers and an optional '+'
            raise ValueError("Phone number must contain only numbers and an optional leading '+'")
        return phone