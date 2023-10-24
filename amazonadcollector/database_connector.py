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
    def __init__(self, udid: int):
        self.__udid = udid
        self.__data_set_id = None
        with open(os.path.join(os.path.dirname(__file__), "../data/config.yaml"), "r") as file:
            self.config = yaml.safe_load(file)
        self.db_credentials = {
            'host': self.config["DATABASE"]["HOST"],
            'database': self.config["DATABASE"]["DB"],
            'user': self.config["DATABASE"]["USERNAME"],
            'password': self.config["DATABASE"]["PASSWORD"],
            'charset': self.config["DATABASE"]["CHARSET"]
        }
        self.__session_id: int = self.__get_last_saved_session_id_from_db() + 1

    def get_udid(self) -> int:
        return self.__udid

    def get_last_saved_id_from_db(self) -> str:
        return self.__data_set_id

    def get_session_id(self) -> int:
        return self.__session_id

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
        self.__data_set_id = str(c.lastrowid)

    def update_query(self, width: int, height: int, location_x: int, location_y: int, text: str,
                     timestamp: str, id_ad_type: int, keyword_id: int) -> None:

        with cursor(**self.db_credentials) as c:

            query_update = f"""
                    UPDATE ads_meta_data 
                    SET filename = '{self.get_last_saved_id_from_db() + ".png"}',
                    width = {width},
                    height = {height},
                    location_x = {location_x},
                    location_y = {location_y},
                    text = '{text.strip()}',
                    timestamp = '{timestamp}',
                    id_ad_type = {id_ad_type},
                    id_session = {self.get_session_id()},
                    keyword_id = {keyword_id},
                    id_host_ip = {self.config["COMPUTER"]["IP"]},
                    id_emulator = {self.get_id_emulator()} 
                    WHERE id = {self.get_last_saved_id_from_db()};
                    """

            c.execute(query_update)

    def send_data_to_db(self, width: int, height: int, location_x: int, location_y: int, text: str,
                        timestamp: str, ad_type: int, keyword_id: int) -> int:
        """
        Sends collected data to database and return id of that data set

        Args:
            width: width of ad
            height: height of ad
            location_x: location_x of ad
            location_y: location_y of ad
            text: text of ad
            timestamp: timestamp of ad creation
            ad_type: type of ad
            keyword_id: id of keyword used to locating ad

        Returns:
            data_set_id: int
        """
        self.insert_empty_query()
        self.update_query(width, height, location_x, location_y, text, timestamp, ad_type, keyword_id)
        return self.__data_set_id

    def __get_last_saved_session_id_from_db(self) -> int:
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

    def get_proxy_port(self, emulator_id: int) -> int:
        """
        Returns:
            proxy_port from db
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

        return int(result)

    def get_id_emulator(self) -> int:
        """
        Returns:
            emulator id from db
        """

        """gets from database udid based on computer ip_id and udid of an emulator"""

        query = f"""
            SELECT id
            FROM emulators
            WHERE udid = {self.__udid} 
            AND id_host_ip = {self.config["COMPUTER"]["IP"]}
            """

        with cursor(**self.db_credentials) as c:
            c.execute(query)
            result = c.fetchone()[0]

        return int(result)
