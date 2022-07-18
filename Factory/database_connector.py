import MySQLdb
from MySQLdb.connections import Connection
from MySQLdb.cursors import \
    Cursor  # pip install mysqlclient~=2.0.3 | sudo apt-get install python-dev libmysqlclient-dev
import contextlib
from typing import (
    ContextManager,
)


@contextlib.contextmanager
def connection(*args, **kwargs) -> ContextManager[Connection]:
    conn = MySQLdb.connect(*args, **kwargs)
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()


@contextlib.contextmanager
def cursor(*args, **kwargs) -> ContextManager[Cursor]:
    with connection(*args, **kwargs) as conn:
        cur = conn.cursor()
        try:
            yield cur
        finally:
            cur.close()


db_credentials = {
    'host': '10.10.10.19',
    'database': 'amazon_krzysiek',
    'user': 'krzysiek',
    'password': 'ndXs5RzCCPot90Se',
    'charset': 'utf8mb4'
}

"""db_credentials = {
    'host': '127.0.0.1',
    'database': 'Amazon_ads',
    'user': 'root',
    'password': '',
    'charset': 'utf8mb4'
}"""


def send_data_to_db(filename, width, height, location_x, location_y, text, timestamp, id_ad_type, id_session, price):
    query = """
            INSERT INTO 
                ads_meta_data
                (filename, width, height, location_x, location_y, text, timestamp, id_ad_type, id_session, price)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ;"""

    with cursor(**db_credentials) as c:
        if not text:
            text = None

        c.execute(
            query,
            (filename, width, height, location_x, location_y, text, timestamp, id_ad_type, id_session, price)
        )


def get_last_saved_id_from_db() -> int:
    query = "SELECT MAX(id) FROM ads_meta_data;"

    with cursor(**db_credentials) as c:
        c.execute(query)
        result = c.fetchone()

    if result[0] is None:
        return 0
    return int(result[0])


def get_last_saved_session_id_from_db() -> int:
    query = "SELECT MAX(id_session) FROM ads_meta_data;"

    with cursor(**db_credentials) as c:
        c.execute(query)
        result = c.fetchone()

    if result[0] is None:
        return 0
    return int(result[0])
