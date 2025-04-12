import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from src.logger import get_logger

logger = get_logger(__name__)

DB_HOST = "***"
DB_NAME = "postgres"
DB_USER = "***"
DB_PASSWORD = "***"
DB_PORT = "5432"

class PostgresConnection:
    def __init__(self, minconn=1, maxconn=5):
        self.db_config = {
            'host': DB_HOST,
            'port': DB_PORT,
            'database': DB_NAME,
            'user': DB_USER,
            'password': DB_PASSWORD,
        }
        self.pool = pool.SimpleConnectionPool(minconn, maxconn, **self.db_config)

    @contextmanager
    def get_cursor(self):
        conn = self.pool.getconn()
        try:
            yield conn.cursor()
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.pool.putconn(conn)

    def close_all(self):
        self.pool.closeall()

def select_product_price_availability(product_name=None):
    db = PostgresConnection()

    with db.get_cursor() as cur:
        cur.execute("""
SELECT p.product_name, p.store_link, p.product_price, p.last_date
FROM gc_tracker.product_availability p
INNER JOIN (SELECT product_name, MAX(last_date) as last_date
FROM gc_tracker.product_availability
GROUP BY product_name) latest
ON p.product_name = latest.product_name AND p.last_date = latest.last_date
WHERE p.availability = true
order by product_price
;
        """)
        rows = cur.fetchall()

    db.close_all()
    return rows

def insert_product_availability(product_name=None, store_link=None, availability=False, product_price=None, error_log=None):      
    db = PostgresConnection()
    if product_price == 'inf':
        product_price = None    
    try:
        with db.get_cursor() as cur:
            cur.execute("""
    INSERT INTO gc_tracker.product_availability (
        product_name,
        store_link,
        availability,
        product_price,
        last_date,
        error_log
    ) VALUES (%s, %s, %s, %s, NOW(), %s);
            """, (product_name, store_link, availability, product_price, error_log))
    except Exception as err:
        logger.error(f"Database error: {err}")
    finally:
        db.close_all()

def create_product_availability():
    db = PostgresConnection()

    with db.get_cursor() as cur:
        cur.execute("""
CREATE TABLE IF NOT EXISTS gc_tracker.product_availability (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    store_link VARCHAR(255),
    availability BOOLEAN,
    product_price NUMERIC(10, 2),
    last_date TIMESTAMP,
    error_log TEXT
);        
        """)
    db.close_all()
