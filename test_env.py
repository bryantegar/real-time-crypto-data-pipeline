from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

print("KAFKA_BOOTSTRAP_SERVER =", os.getenv("KAFKA_BOOTSTRAP_SERVER"))
print("KAFKA_TOPIC =", os.getenv("KAFKA_TOPIC"))
