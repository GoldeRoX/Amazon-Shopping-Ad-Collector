import MySQLdb
from MySQLdb.connections import Connection
from MySQLdb.cursors import \
    Cursor  # pip install mysqlclient~=2.0.3 | sudo apt-get install python-dev libmysqlclient-dev
import contextlib
from typing import (
    ContextManager,
)
import yaml


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


with open("../data/config.yaml", "r") as file:
    config = yaml.safe_load(file)

db_credentials = {
    'host': config["DATABASE"]["HOST"],
    'database': config["DATABASE"]["DB"],
    'user': config["DATABASE"]["USERNAME"],
    'password': config["DATABASE"]["PASSWORD"],
    'charset': config["DATABASE"]["CHARSET"]
}


class SQLAdManager(object):

    def __init__(self):
        self.data_set_id = None

    def insert_empty_query(self):
        query_insert = """
                        INSERT INTO 
                            ads_meta_data
                            (filename, width, height, location_x, location_y, text, 
                            timestamp, id_ad_type, id_session)
                        VALUES
                            (0, 0, 0, 0, 0, 0, 0, 0, 0);
                        """

        with cursor(**db_credentials) as c:
            c.execute(query_insert)
        self.data_set_id = str(c.lastrowid)

    def update_query(self, width: int, height: int, location_x: int, location_y: int, text: str,
                     timestamp: str, id_ad_type: int, id_session: int, keyword_id: int):
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
                keyword_id = %s
                WHERE id = {self.data_set_id};
                """
        with cursor(**db_credentials) as c:
            if not text:
                text = None

            c.execute(
                query_update,
                (width, height, location_x, location_y, text, timestamp, id_ad_type, id_session, keyword_id)
            )

    def send_data_to_db(self, width, height, location_x, location_y, text, timestamp, ad_type, id_session, keyword_id):
        self.insert_empty_query()
        self.update_query(width, height, location_x, location_y, text, timestamp, ad_type, id_session, keyword_id)

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


def get_random_keyword() -> {}:
    """get random keyword and id of this keyword form database

    Returns:
        returns a dictionary (id, keyword) of random keyword from database
    """

    query = """
        SELECT id, keyword FROM keywords
        ORDER BY RAND()
        LIMIT 1;
        """

    with cursor(**db_credentials) as c:
        c.execute(query)
        result_of_query = c.fetchone()

    result = {
        "id": int(result_of_query[0]),
        "keyword": str(result_of_query[1])
    }

    return result
