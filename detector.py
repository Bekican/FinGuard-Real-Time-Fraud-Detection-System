import json
import time
from kafka import KafkaConsumer
import redis
import psycopg2

TOPIC_NAME = 'financial_transactions'
api_version=(0, 10, 1),
BOOTSTRAP_SERVERS = ['localhost:9092']


r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port = "5433",
        database="finguard",
        user="admin",
        password="password123"
    )


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fraud_alerts (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(50),
            amount DECIMAL,
            location VARCHAR(100),
            fraud_reason VARCHAR(200),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


init_db()

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(" Dedektif (Detector) Veritabanına Bağlandı! İzleme Başladı...")

for message in consumer:
    transaction = message.value
    user_id = str(transaction['user_id'])
    loc = transaction['location']
    amt = transaction['amount']
    
    fraud_reason = None

   
    last_loc = r.get(f"user:{user_id}:location")
    if last_loc and last_loc != loc:
            fraud_reason = f"Impossible Travel: {last_loc} -> {loc}"

  
    if amt > 10000:
        fraud_reason = f"High Amount Limit: {amt} TL"

    
    if fraud_reason:
        print(f"🚨 [ALARM] {fraud_reason} - User: {user_id}")
        
      
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO fraud_alerts (user_id, amount, location, fraud_reason) VALUES (%s, %s, %s, %s)",
                (user_id, amt, loc, fraud_reason)
            )
            conn.commit()
            cur.close()
            conn.close()
            print("  Veritabanına kaydedildi.")
        except Exception as e:
            print(f"   DB Hatası: {e}")
    

    r.set(f"user:{user_id}:location", loc)