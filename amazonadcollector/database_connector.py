import MySQLdb
from MySQLdb.connections import Connection
from MySQLdb.cursors import \
    Cursor
import contextlib
from typing import (
    ContextManager,
)
import yaml
import os


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


class SQLAdManager(object):
    def __init__(self):
        self.data_set_id = None
        self.path = os.path.join(os.path.dirname(__file__), "../data/config.yaml")
        with open(self.path, "r") as file:
            self.config = yaml.safe_load(file)
        self.db_credentials = {
            'host': self.config["DATABASE"]["HOST"],
            'database': self.config["DATABASE"]["DB"],
            'user': self.config["DATABASE"]["USERNAME"],
            'password': self.config["DATABASE"]["PASSWORD"],
            'charset': self.config["DATABASE"]["CHARSET"]
        }

    def insert_empty_query(self):
        query_insert = """
                        INSERT INTO 
                            ads_meta_data
                            (filename, width, height, location_x, location_y, text, 
                            timestamp, id_ad_type, id_session, keyword_id, id_host_ip, id_emulator)
                        VALUES
                            (0, 0, 0, 0, 0, 0, 0, 0, 0, NULL, NULL, NULL);
                        """

        with cursor(**self.db_credentials) as c:
            c.execute(query_insert)
        self.data_set_id = str(c.lastrowid)

    def update_query(self, width: int, height: int, location_x: int, location_y: int, text: str,
                     timestamp: str, id_ad_type: int, id_session: int, keyword_id: int, ip: int, udid: int) -> None:
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
                keyword_id = %s,
                id_host_ip = %s,
                id_emulator = %s
                WHERE id = {self.data_set_id};
                """
        with cursor(**self.db_credentials) as c:
            if not text:
                text = None

            c.execute(
                query_update,
                (width, height, location_x, location_y, text, timestamp, id_ad_type, id_session, keyword_id, ip, udid)
            )

    def send_data_to_db(self, width, height, location_x, location_y, text,
                        timestamp, ad_type, id_session, keyword_id, udid) -> None:
        self.insert_empty_query()
        self.update_query(width, height, location_x, location_y, text, timestamp, ad_type,
                          id_session, keyword_id, self.config["COMPUTER"]["IP"], udid)

    def get_last_saved_id_from_db(self) -> int:
        return self.data_set_id

    def get_last_saved_session_id_from_db(self) -> int:
        query = "SELECT COALESCE(MAX(id_session), 0) FROM ads_meta_data;"
        with cursor(**self.db_credentials) as c:
            c.execute(query)
            result = c.fetchone()[0]
        return int(result)

    def get_random_keyword(self) -> {}:
        """get random keyword and id of this keyword form database

        Returns:
            returns a dictionary (id, keyword) of random keyword from database
        """

        query = """
            SELECT id, keyword 
            FROM keywords
            ORDER BY RAND()
            LIMIT 1;
            """

        with cursor(**self.db_credentials) as c:
            c.execute(query)
            result_of_query = c.fetchone()

        result: dict[str, str | int] = {
            "id": int(result_of_query[0]),
            "keyword": str(result_of_query[1])
        }

        return result

    def get_proxy_address(self, emulator_id: int) -> str:
        """
        Returns:
            proxy_address
        """

        query = f"""
            SELECT proxy 
            FROM emulators
            WHERE id_host_ip = {self.config["COMPUTER"]["IP"]}
            AND udid = {emulator_id}
            """

        with cursor(**self.db_credentials) as c:
            c.execute(query)
            result = c.fetchone()[0]

        return result

    def get_proxy_port(self, emulator_id: int) -> str:
        """
        Returns:
            proxy_port
        """

        query = f"""
            SELECT proxy_port
            FROM emulators
            WHERE id_host_ip = {self.config["COMPUTER"]["IP"]}
            AND udid = {emulator_id}
            """

        with cursor(**self.db_credentials) as c:
            c.execute(query)
            result = c.fetchone()[0]

        return result
