import dotenv
import os

dotenv.load_dotenv()

DEV = os.getenv("DEV") == "true"
MONGODB_URI = os.getenv("MONGODB_URI")

AGENDOR_TOKEN = os.getenv("AGENDOR_TOKEN")

SERVICE_TOKEN = os.getenv("SERVICE_TOKEN")