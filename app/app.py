from flask import Flask
import os
import mysql.connector
import redis

app = Flask(__name__)

db_config = {
    "host": os.getenv("DB_HOST", "db"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "connection_timeout": 3,
}

redis_host = os.getenv("REDIS_HOST", "redis")


@app.route("/")
def home():
    return "Task Manager API is running!", 200


@app.route("/live")
def live():
    return {
        "status": "alive"
    }, 200


@app.route("/health")
def health():
    db = None

    try:
        db = mysql.connector.connect(**db_config)

        r = redis.Redis(
            host=redis_host,
            port=6379,
            socket_connect_timeout=3,
            socket_timeout=3,
        )
        r.ping()

        return {
            "status": "healthy",
            "mysql": "ok",
            "redis": "ok",
        }, 200

    except Exception as error:
        return {
            "status": "unhealthy",
            "error": str(error),
        }, 503

    finally:
        if db is not None and db.is_connected():
            db.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

