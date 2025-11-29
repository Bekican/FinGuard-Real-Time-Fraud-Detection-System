from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port = "5433",
        database="finguard",
        user="admin",
        password="password123"
    )

@app.get("/")
def read_root():
    return {"System" : "FinGuard Fraud Detection API","Status" :"Active"}

@app.get("/alerts")
def get_alerts():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM fraud_alerts ORDER BY timestamp DESC LIMIT 50")
        alerts = cur.fetchall()

        cur.close()
        conn.close()
        return {"count" : len(alerts),"data" : alerts}
    except Exception as e:
        return {"error" : str(e)}
@app.get("/stats")
def get_status():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM fraud_alerts")
    total_fraud = cur.fetchone()[0]
    conn.close()
    return {"total_fraud_detected" : total_fraud}
