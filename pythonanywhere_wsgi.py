"""
WSGI configuration template for PythonAnywhere Free Tier deployment.
Copy the contents of this file into your PythonAnywhere WSGI configuration file
(located under the Web tab -> Code section -> WSGI configuration file).
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Replace 'yourusername' with your actual PythonAnywhere username
PROJECT_DIR = Path("/home/yourusername/100-humanity")
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

load_dotenv(PROJECT_DIR / ".env")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
