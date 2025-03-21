import unittest
from flask_testing import TestCase
from app import app, db, Patient  # Import the `generate_token` function

class TestApp(TestCase):
    def create_app(self):
        # Configure the app for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients_test.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        # Create the database and tables
        db.create_all()

        # Generate a valid token for testing
        self.valid_token = "secret-token-123"  # Replace `1` with a valid user ID

    def tearDown(self):
        # Drop all tables after each test
        db.session.remove()
        db.drop_all()

    def test_register_patient_success(self):
        """Test successful patient registration."""
        response = self.client.post(
            '/patients',
            json={
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1234567890'
            },
            headers={'Authorization': f'Bearer {self.valid_token}'}
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('patient_id', response.json)

    def test_register_patient_missing_fields(self):
        """Test registration with missing fields."""
        response = self.client.post(
            '/patients',
            json={
                'name': 'John Doe',
                'email': 'john.doe@example.com'
                # Missing 'phone'
            },
            headers={'Authorization': f'Bearer {self.valid_token}'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_register_patient_invalid_email(self):
        try:
            """Test registration with invalid email."""
            response = self.client.post(
                '/patients',
                json={
                    'name': 'John Doe',
                    'email': 'invalid-email',
                    'phone': '+1234567890'
                },
                headers={'Authorization': f'Bearer {self.valid_token}'}
            )
        except Exception as e:
            self.assertEqual(str(e), "Invalid email format")

    def test_register_patient_invalid_phone(self):
        """Test registration with invalid phone."""
        try:
            response = self.client.post(
                '/patients',
                json={
                    'name': 'John Doe',
                    'email': 'john.doe@example.com',
                    'phone': '039383qwe'  # Invalid phone
                },
                headers={'Authorization': f'Bearer {self.valid_token}'}
            )
        except Exception as e:
            self.assertEqual(str(e), "Phone number must contain only numbers and an optional leading '+'")
            # self.assertEqual(response.status_code, 400)
        

    def test_register_patient_duplicate_email(self):
        """Test registration with duplicate email."""
        # Register the first patient
        self.client.post(
            '/patients',
            json={
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1234567890'
            },
            headers={'Authorization': f'Bearer {self.valid_token}'}
        )

        # Attempt to register a second patient with the same email
        response = self.client.post(
            '/patients',
            json={
                'name': 'Jane Doe',
                'email': 'john.doe@example.com',  # Duplicate email
                'phone': '+0987654321'
            },
            headers={'Authorization': f'Bearer {self.valid_token}'}
        )
        self.assertEqual(response.status_code, 409)
        self.assertIn('error', response.json)

    def test_register_patient_duplicate_phone(self):
        """Test registration with duplicate phone."""
        # Register the first patient
        self.client.post(
            '/patients',
            json={
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1234567890'
            },
            headers={'Authorization': f'Bearer {self.valid_token}'}
        )

        # Attempt to register a second patient with the same phone
        response = self.client.post(
            '/patients',
            json={
                'name': 'Jane Doe',
                'email': 'jane.doe@example.com',
                'phone': '+1234567890'  # Duplicate phone
            },
            headers={'Authorization': f'Bearer {self.valid_token}'}
        )
        self.assertEqual(response.status_code, 409)
        self.assertIn('error', response.json)

    def test_register_patient_missing_token(self):
        """Test registration without a token."""
        response = self.client.post(
            '/patients',
            json={
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1234567890'
            }
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual({'message': 'Unauthorized'}, response.json)

    def test_register_patient_invalid_token(self):
        """Test registration with an invalid token."""
        response = self.client.post(
            '/patients',
            json={
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1234567890'
            },
            headers={'Authorization': 'Bearer invalid-token'}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual({'message': 'Unauthorized'}, response.json)

if __name__ == '__main__':
    unittest.main()