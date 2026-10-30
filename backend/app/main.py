from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.schemas.db_service import get_connection


class CustomerCreate(BaseModel):
    CustomerName: str
    ContactNo: str
    Email: str
    Country: str

# 1. Define a lifespan event to test the DB connection on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up...")
    # get_db_connection() # This triggers your print statements!
    # await get_customers()
    # await create_customer("John Doe", "john.doe@example.com", "123-456-7890", "USA")
    yield
    print("Application shutting down...")

# 2. Pass the lifespan to FastAPI
app = FastAPI(
    title="FastAPI + Vue 3 Monolith-Alternative",
    description="Clean decoupled architecture.",
    version="1.0.0",
    lifespan=lifespan 
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
async def health_check():
    print("Health check endpoint called.")
    return {"status": "healthy", "message": "Backend connected smoothly!"}

def get_db_connection():
    print("Attempting to connect to the database...")
    try:
        connection = get_connection()
        print(f"Database connection established: {connection}")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.get("/api/v1/get_customers")
async def get_customers():
    print("Fetching customers...")
    connection = get_db_connection()
    if connection is None:
        return {"status": "error", "message": "Failed to connect to the database."}
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customers")  # Adjust the table name as needed
            customers = cursor.fetchall()
            # print(f"Fetched customers: {customers}")
            return {"status": "success", "data": customers}
    except Exception as e:
        print(f"Error fetching customers: {e}")
        return {"status": "error", "message": "Failed to fetch customers."}
    finally:
        connection.close()

@app.post("/api/v1/create_customer")
async def create_customer(customer: CustomerCreate):
    print(f"Received customer data: {customer.model_dump()}")
    connection = get_db_connection()
    if connection is None:
        return {"status": "error", "message": "Failed to connect to the database."}
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO customers (CustomerName, ContactNo, Country, email) VALUES (%s, %s, %s, %s)",
                (customer.CustomerName, customer.ContactNo, customer.Country, customer.Email)
            )
            connection.commit()
            print("Customer created successfully.")
            return {"status": "success", "message": "Customer created successfully."}
    except Exception as e:
        print(f"Error creating customer: {e}")
        return {"status": "error", "message": "Failed to create customer."}
    finally:
        connection.close()

@app.get("/api/v1/get_customer/{customerId}")
async def get_customer(customerId: int):
    print(f"Fetching customer with ID: {customerId}")
    connection = get_db_connection()
    if connection is None:
        return {"status": "error", "message": "Failed to connect to the database."}
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customers WHERE CustomerID = %s", (customerId,))
            customer = cursor.fetchone()
            if customer:
                print(f"Fetched customer: {customer}")
                return {"status": "success", "data": customer}
            else:
                print("Customer not found.")
                return {"status": "error", "message": "Customer not found."}
    except Exception as e:
        print(f"Error fetching customer: {e}")
        return {"status": "error", "message": "Failed to fetch customer."}
    finally:
        connection.close()

@app.put("/api/v1/update_customer/{customer_id}")
async def update_customer(customer_id: int, customer: CustomerCreate):
    print(f"Updating customer with ID: {customer_id} with data: {customer.model_dump()}")
    connection = get_db_connection()
    if connection is None:
        return {"status": "error", "message": "Failed to connect to the database."}
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE customers SET CustomerName = %s, ContactNo = %s, Country = %s, Email = %s WHERE CustomerID = %s",
                (customer.CustomerName, customer.ContactNo, customer.Country, customer.Email, customer_id)
            )
            connection.commit()
            if cursor.rowcount == 0:
                print("Customer not found for update.")
                return {"status": "error", "message": "Customer not found."}
            print("Customer updated successfully.")
            return {"status": "success", "message": "Customer updated successfully."}
    except Exception as e:
        print(f"Error updating customer: {e}")
        return {"status": "error", "message": "Failed to update customer."}
    finally:
        connection.close()

@app.delete("/api/v1/delete_customer/{customerId}")
async def delete_customer(customerId: int):
    print("Inside delete function")
    print(f"Deleting customer with ID: {customerId}")
    # return {"status": "success", "message": "Delete test"}
    connection = get_db_connection()
    if connection is None:
        return {"status": "error", "message": "Failed to connect to the database."}
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM customers WHERE CustomerID = %s", (customerId,))
            connection.commit()
            if cursor.rowcount == 0:
                print("Customer not found for deletion.")
                return {"status": "error", "message": "Customer not found."}
            print("Customer deleted successfully.")
            return {"status": "success", "message": "Customer deleted successfully."}
    except Exception as e:
        print(f"Error deleting customer: {e}")
        return {"status": "error", "message": "Failed to delete customer."}
    finally:
        connection.close()