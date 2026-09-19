import os

from dotenv import load_dotenv

load_dotenv(override=True)

CCTQ_API_KEY = os.getenv('CCTQ_API_KEY')
CCTQ_BASE_URL = os.getenv('CCTQ_BASE_URL')

SHUSHENG_API_KEY = os.getenv('SHUSHENG_API_KEY')
SHUSHENG_BASE_URL = os.getenv('SHUSHENG_BASE_URL')
