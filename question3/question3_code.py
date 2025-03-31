from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2 import sql
import threading

app = FastAPI()

# Database connection setup
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="banking",
        user="username",
        password="password"
    )

# Model for Debit Request
class DebitRequest(BaseModel):
    account_id: int
    amount: float

# Locking function for concurrency safety
def acquire_lock(account_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT lock_status FROM transaction_locks WHERE account_id = %s", (account_id,))
    lock_status = cursor.fetchone()

    if lock_status and lock_status[0]:
        conn.close()
        raise HTTPException(status_code=400, detail="Account is currently locked.")
    
    cursor.execute("UPDATE transaction_locks SET lock_status = TRUE WHERE account_id = %s", (account_id,))
    conn.commit()
    conn.close()

def release_lock(account_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE transaction_locks SET lock_status = FALSE WHERE account_id = %s", (account_id,))
    conn.commit()
    conn.close()

# Debit operation
@app.post("/transaction/debit")
async def debit(request: DebitRequest):
    account_id = request.account_id
    amount = request.amount

    try:
        # Step 1: Acquire lock for concurrency safety
        acquire_lock(account_id)

        # Step 2: Begin transaction
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
        balance = cursor.fetchone()

        if balance is None:
            raise HTTPException(status_code=404, detail="Account not found.")

        if balance[0] < amount:
            raise HTTPException(status_code=400, detail="Insufficient balance.")

        # Step 3: Debit account
        new_balance = balance[0] - amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s", (new_balance, account_id))
        cursor.execute("INSERT INTO transactions (account_id, type, amount, status) VALUES (%s, %s, %s, %s)", 
                       (account_id, 'debit', amount, 'completed'))
        conn.commit()
        conn.close()

        # Step 4: Release lock
        release_lock(account_id)

        return {"status": "success", "message": f"Debited {amount} from account {account_id}"}

    except Exception as e:
        release_lock(account_id)
        raise HTTPException(status_code=500, detail=str(e))
