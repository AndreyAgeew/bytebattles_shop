from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
JTWTS_KEY = os.getenv('JTWTS_KEY')
JWT_KEY = os.getenv('JWT_KEY')
ALGORITHM_JWT = os.getenv('ALGORITHM_JWT')
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
DOMAIN_NAME = os.getenv('DOMAIN_NAME')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
