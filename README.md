# **Telehealth Patient Management API**

This project is a Flask-based RESTful API for managing patient records. It includes CRUD operations for patients, asynchronous background task processing using Celery and Redis, and token-based authentication.

---

## **Table of Contents**
1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Setup Instructions](#setup-instructions)
4. [API Endpoints](#api-endpoints)
5. [Design Decisions](#design-decisions)
6. [Testing](#testing)

---

## **Features**
- **CRUD Operations**: Create, read, update, and delete patient records.
- **Asynchronous Tasks**: Background tasks for sending notifications using Celery and Redis.
- **Token-Based Authentication**: Secure API endpoints with a simple token-based authentication mechanism.
- **Unit Tests**: Basic unit tests for API endpoints.

---

## **Technology Stack**
- **Python**: Primary programming language.
- **Flask**: Web framework for building the API.
- **SQLite**: Lightweight database for storing patient records.
- **Celery**: Distributed task queue for background processing.
- **Redis**: Message broker for Celery.
- **SQLAlchemy**: ORM for database interactions.
- **Token-Based Authentication**: Simple authentication mechanism.

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/codeguru577/telehealth-backend.git
cd telehealth-api
```



### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```


### **3. Start Redis**
Redis is required for Celery to handle background tasks. Start Redis using:
```bash
redis-stable/src/redis-server
```

### **4. Start Celery**
Run the Celery worker to process background tasks:
```bash
celery -A tasks worker --loglevel=info
```

### **5. Run the Flask Application**
Start the Flask development server:
```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`.

---

## **API Endpoints**

### **1. Create a Patient**
- **Endpoint**: `POST /patients`
- **Request**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Patient created successfully",
    "patient_id": "3ce2dd50-7764-42bf-847a-a84b3071eaeb"
  }
  ```

### **2. Retrieve a Patient**
- **Endpoint**: `GET /patients/<patient_id>`
- **Response**:
  ```json
  {
    "email": "john@example.com",
    "id": "3ce2dd50-7764-42bf-847a-a84b3071eaeb",
    "name": "John Doe",
    "phone": "1234567890"
  }
  ```

### **3. Update a Patient**
- **Endpoint**: `PUT /patients/<patient_id>`
- **Request**:
  ```json
  {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "0987654321"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Patient updated successfully"
  }
  ```

### **4. Delete a Patient**
- **Endpoint**: `DELETE /patients/<patient_id>`
- **Response**:
  ```json
  {
    "message": "Patient deleted successfully"
  }
  ```

### **5. Retrieve All Patients**
- **Endpoint**: `GET /patients`
- **Response**:
  ```json
  [
    {
        "email": "jane@example.com",
        "id": "5757715b-cbcc-4c7a-8be0-e2a5e0f7376c",
        "name": "Jane Doe",
        "phone": "0987654321"
    },
    {
        "email": "john@example.com",
        "id": "28b2df58-7e8e-4cea-8bff-c118f9deaee4",
        "name": "John Smith",
        "phone": "330987654321"
    }
  ]
  ```

---

## **Design Decisions**

### **1. Celery and Redis Integration**
- **Why Celery?**
  - Celery allows asynchronous processing of background tasks, ensuring the API remains responsive.
  - It handles task retries and failures gracefully, which is crucial for sending notifications.
- **Why Redis?**
  - Redis is a fast, in-memory data store that acts as a message broker for Celery.
  - It ensures reliable communication between the Flask app and Celery workers.

### **2. Token-Based Authentication**
- A simple token-based authentication mechanism is implemented to secure API endpoints.
- Each request must include the header:
  ```
  Authorization: Bearer secret-token-123
  ```

### **3. SQLite Database**
- SQLite is used for simplicity during development.
- The code is written to be compatible with PostgreSQL for easy migration to a production environment.

---

## **Testing**

### **Run Unit Tests**
To run the unit tests, execute the following command:
```bash
python -m unittest tests/test_api.py
```

### **Test Coverage**
The tests cover:
- Creating, retrieving, updating, and deleting patients.
- Authentication and error handling.