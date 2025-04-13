import yaml
from psycopg2 import pool
from contextlib import contextmanager
from src.logger import get_logger

logger = get_logger(__name__)

with open("./src/config/config.yml", "r") as file:
    configs = yaml.safe_load(file)["postgresql"]

DB_HOST = configs["DB_HOST"]
DB_NAME = configs["DB_NAME"]
DB_USER = configs["DB_USER"]
DB_PASSWORD = configs["DB_PASSWORD"]
DB_PORT = configs["DB_PORT"]


class PostgresConnection:
    def __init__(self, minconn=1, maxconn=5):
        self.db_config = {
            "host": DB_HOST,
            "port": DB_PORT,
            "database": DB_NAME,
            "user": DB_USER,
            "password": DB_PASSWORD,
        }
        self.pool = pool.SimpleConnectionPool(minconn, maxconn, **self.db_config)

    @contextmanager
    def get_cursor(self):
        conn = self.pool.getconn()
        try:
            yield conn.cursor()
            conn.commit()
        except Exception as err:
            conn.rollback()
            raise err
        finally:
            self.pool.putconn(conn)

    def close_all(self):
        if self.pool:
            self.pool.closeall()


def execute_query(query, params=None):
    db = PostgresConnection()
    try:
        with db.get_cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
        return rows
    except Exception as err:
        logger.error(f"Query error: {err}")
        raise
    finally:
        db.close_all()


def select_product_last_data(product_name=None):
    query = """
    WITH latest AS (
        SELECT store_link, MAX(last_date) AS last_date
        FROM gc_tracker.product_availability
        GROUP BY store_link
    )
    SELECT p.id, COALESCE(pu.product_name, p.product_name) AS product_name, p.store_link, p.availability, p.product_price, p.last_date
    FROM gc_tracker.product_availability p
    INNER JOIN latest ON p.store_link = latest.store_link AND p.last_date = latest.last_date
    LEFT JOIN gc_tracker.product_url pu ON pu.store_link = p.store_link;
    """
    return execute_query(query)


def select_product_url(product_name=None):
    query = "SELECT * FROM gc_tracker.product_url WHERE activated = TRUE;"
    return execute_query(query)

def select_product_url_monitoring(product_name=None):
    query = """ 
    SELECT product_name, store_link, activated FROM gc_tracker.product_url
    order by product_name, store_link, activated
    ;
    """
    return execute_query(query)


def select_product_price_availability(product_name=None):
    query = """
WITH MinPrices AS (
    SELECT
        COALESCE(pu.product_name, pa.product_name) AS product_name,
        MIN(pa.product_price) AS min_price
    FROM
        gc_tracker.product_availability pa
    LEFT JOIN
        gc_tracker.product_url pu
    ON
        pu.store_link = pa.store_link
    WHERE
        pa.availability = TRUE
    GROUP BY
        COALESCE(pu.product_name, pa.product_name)
),
FilteredAvailability AS (
    SELECT
        COALESCE(pu.product_name, p.product_name) AS product_name,
        p.store_link,
        p.product_price,
        p.last_date,
        ROW_NUMBER() OVER (
            PARTITION BY COALESCE(pu.product_name, p.product_name)
            ORDER BY p.product_price ASC, p.last_date DESC
        ) as row_num
    FROM
        gc_tracker.product_availability p
    LEFT JOIN
        gc_tracker.product_url pu
    ON
        pu.store_link = p.store_link
    INNER JOIN
        MinPrices mp
    ON
        COALESCE(pu.product_name, p.product_name) = mp.product_name
        AND p.product_price = mp.min_price
    WHERE
        p.availability = TRUE
)
SELECT
    product_name,
    store_link,
    product_price,
    last_date
FROM
    FilteredAvailability
WHERE
    row_num = 1
ORDER BY
    product_price
;
        """
    return execute_query(query)


def insert_product_availability(
    product_name=None,
    store_link=None,
    availability=False,
    product_price=None,
    error_log=None,
):
    db = PostgresConnection()
    if product_price == "inf":
        product_price = None
    try:
        with db.get_cursor() as cur:
            cur.execute(
                """
    INSERT INTO gc_tracker.product_availability (
        product_name,
        store_link,
        availability,
        product_price,
        last_date,
        error_log
    ) VALUES (%s, %s, %s, %s, NOW(), %s);
            """,
                (product_name, store_link, availability, product_price, error_log),
            )
    except Exception as err:
        logger.error(f"Database error: {err}")
    finally:
        db.close_all()


def create_product_availability():
    db = PostgresConnection()

    with db.get_cursor() as cur:
        cur.execute(
            """
CREATE TABLE IF NOT EXISTS gc_tracker.product_availability (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    store_link VARCHAR(255),
    availability BOOLEAN,
    product_price NUMERIC(10, 2),
    last_date TIMESTAMP,
    error_log TEXT
);        
        """
        )
    db.close_all()
