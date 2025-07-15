import psycopg2
import os
import time
import json
from pprint import pprint

from django.conf import settings
from django.core.cache import cache
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db_conn():
    try:
        conn = psycopg2.connect(
            dbname =    os.environ.get("PM_DBNAME"),
            user =      os.environ.get("PM_DBUSERNAME"),
            password =  os.environ.get("PM_DBPASS"),
            host =      os.environ.get("PM_DBHOST"),
            port =      os.environ.get("PM_DBPORT"),
        )

        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error connecting to the database: {error}")

        raise






