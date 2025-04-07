import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE = os.getenv("DATABASE")
SUPERADMIN = os.getenv("SUPERADMIN")
