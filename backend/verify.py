from fastapi.testclient import TestClient
from app.main import app
from app.database.session import engine
from app.database.base import Base

# Ensure tables are created
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_auth():
    # Register
    print("Testing Registration...")
    response = client.post("/api/v1/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    
    if response.status_code == 201:
        print("Registration Successful")
    elif response.status_code == 400 and "already exists" in response.text:
        print("User already exists, proceeding to login...")
    else:
        print(f"Registration Failed: {response.status_code} {response.text}")
        return

    # Login
    print("Testing Login...")
    response = client.post("/api/v1/login", data={
        "username": "test@example.com",
        "password": "password123"
    })
    if response.status_code != 200:
        print(f"Login Failed: {response.status_code} {response.text}")
        return
        
    token = response.json()["access_token"]
    print("Login Successful, got token.")

    # Get Me
    print("Testing /users/me...")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/users/me", headers=headers)
    if response.status_code == 200:
        print("Get Me Successful:", response.json())
    else:
        print(f"Get Me Failed: {response.status_code} {response.text}")

    # Test Unauthorized
    print("Testing Unauthorized access...")
    response = client.get("/api/v1/users/me")
    if response.status_code == 401:
        print("Unauthorized correctly rejected.")
    else:
        print(f"Unauthorized check failed: {response.status_code}")

if __name__ == "__main__":
    test_auth()
