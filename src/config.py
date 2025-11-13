"""
Load configurations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_DB = int(os.getenv("REDIS_DB"))

# Kafka Configuration
KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")
KAFKA_AUTO_OFFSET_RESET = os.getenv("KAFKA_AUTO_OFFSET_RESET")
LOG_LEVEL = os.getenv("LOG_LEVEL")

for env_variable in ["DB_HOST", "DB_PORT","DB_NAME","DB_USER","DB_PASSWORD","REDIS_HOST","REDIS_PORT","REDIS_DB","KAFKA_HOST", "KAFKA_TOPIC", "KAFKA_GROUP_ID", "KAFKA_AUTO_OFFSET_RESET", "LOG_LEVEL"]:
    if globals()[env_variable] is None:
        raise EnvironmentError(f"Variable {env_variable} n'était pas trouvé dans votre fichier .env.")