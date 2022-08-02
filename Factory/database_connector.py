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


"""db_credentials = {
    'host': '10.10.10.19',
    'database': 'amazon_krzysiek',
    'user': 'krzysiek',
    'password': 'ndXs5RzCCPot90Se',
    'charset': 'utf8mb4'
}"""

db_credentials = {
    'host': '127.0.0.1',
    'database': 'Amazon_ads',
    'user': 'root',
    'password': '',
    'charset': 'utf8mb4'
}


class SQLAdManager(object):

    def __init__(self):
        self.data_set_id = None

    def insert_query(self):
        query_insert = """
                        INSERT INTO 
                            ads_meta_data
                            (filename, width, height, location_x, location_y, text, 
                            timestamp, id_ad_type, id_session, price)
                        VALUES
                            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
                        """

        with cursor(**db_credentials) as c:
            c.execute(query_insert)
        self.data_set_id = str(c.lastrowid)

    def update_query(self, width: int, height: int, location_x: int, location_y: int, text: str,
                     timestamp: str, id_ad_type: int, id_session: int, price: str):
        query_update = f"""
                UPDATE ads_meta_data
                SET filename = '{self.data_set_id + ".png"}', 
                width = %s, 
                height = %s, 
                location_x = %s, 
                location_y = %s,
                text = %s, 
                timestamp = %s, 
                id_ad_type = %s, 
                id_session = %s, 
                price = %s
                WHERE id = {self.data_set_id};
                """
        with cursor(**db_credentials) as c:
            if not text:
                text = None

            c.execute(
                query_update,
                (width, height, location_x, location_y, text, timestamp, id_ad_type, id_session, price)
            )

    def send_data_to_db(self, width, height, location_x, location_y, text, timestamp, ad_type, id_session, price):
        self.insert_query()
        self.update_query(width, height, location_x, location_y, text, timestamp, ad_type, id_session, price)

    def get_last_saved_id_from_db(self) -> int:
        return self.data_set_id

    @staticmethod
    def get_last_saved_session_id_from_db() -> int:
        query = "SELECT MAX(id_session) FROM ads_meta_data;"

        with cursor(**db_credentials) as c:
            c.execute(query)
            result = c.fetchone()

        if result[0] is None:
            return 0
        return int(result[0])

