# config.py

# Switch between environments easily
USE_LOCALHOST = True

# Define URLs
LOCAL_API_URL = "http://localhost:8000"
PROD_API_URL = "https://your.production.server"

# Central API base URL
API_BASE_URL = LOCAL_API_URL if USE_LOCALHOST else PROD_API_URL