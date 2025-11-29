import time
import json
import random
from kafka import KafkaProducer
from faker import Faker

fake = Faker()
TOPIC_NAME = "financial_transactions"
BOOTSTRAP_SERVERS = ['localhost:9092']

producer = KafkaProducer(
    bootstrap_servers = BOOTSTRAP_SERVERS,
    api_version = (0, 10, 1),
    value_serializer = lambda x:json.dumps(x).encode('utf-8')
)

user_pool = [{"user_id":i,"name":fake.name(),"city":fake.city()} for i in range(1,101) ]

def create_transaction():
    is_fraud_scenario = random.random() < 0.1

    user = random.choice(user_pool)

    transaction = {
        "timestamp" : time.time(),
        "user_id" : user["user_id"],
        "card_mask" : f"4543-xxxx-xxxx-{random.randint(1000,9999)}",
        "amount" : round(random.uniform(10,5000),2),
        "merchant" : fake.company(),
        "category": random.choice(["Food", "Electronics", "Clothing", "Gas"]),
        "ip_address": fake.ipv4(),
        "location": user["city"]
    }


    if is_fraud_scenario:
        fraud_type = random.choice(["location_jump","high_amount"])

        if fraud_type == "location_jump":
            transaction["location"] = "Kars"
            transaction["ip_address"] = "192.168.1.50"
            print(f"!!![FRAUD_SIM] Location jump for user{user['user_id']}")


        elif fraud_type == "high_amount":
            transaction["amount"] = 25000.00 
            print(f"!!![FRAUD-SIM] High Amount for User {user['user_id']}")
    return transaction
print("Simülator Başlatıldı . Kafka'ya veri iletiliyor...")

try:
    while True:
        data = create_transaction()
        producer.send(TOPIC_NAME,value=data)

        if data.get("amount") > 10000 or data.get("location") == "Kars":
            pass
        else:
            print(f"[NORMAL] {data['amount']} TL - {data['merchant']}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Simülator durduruldu!")

