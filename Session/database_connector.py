import MySQLdb
from MySQLdb.connections import Connection
from MySQLdb.cursors import Cursor # pip install mysqlclient~=2.0.3 | sudo apt-get install python-dev libmysqlclient-dev
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
    'host': '127.0.0.1',
    'database': 'amazon_adds',
    'user': 'root',
    'password': '',
    'charset': 'utf8mb4'
}

with cursor(**db_credentials) as c:
    c.execute("describe Brands_related_to_your_search;")
    re = c.fetchall()
    desc = c.description
    print(re)
    print([a[0] for a in desc])