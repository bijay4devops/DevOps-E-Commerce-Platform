import os
from dotenv import load_dotenv

load_dotenv()

# Pytest runs on the EC2 host, not inside Docker.
os.environ["MYSQL_HOST"] = "127.0.0.1"
os.environ.setdefault("MYSQL_PORT", "3306")
