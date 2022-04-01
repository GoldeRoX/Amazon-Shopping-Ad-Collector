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

"""insert into DB"""
# with cursor(**db_credentials) as c:
# c.execute(f"INSERT INTO `Brands_related_to_your_search` (`Atrybut_text`, `img`) VALUES (`{str(text)}`, LOAD_FILE(`../Screenshots/Brands related to your search/{filename}.png`));")
# "
# INSERT INTO `Wydawnictwo` (`Id_Wydawnictwo`, `Nazwa_Wydawnictwa`, `Adres_Wydawnictwa`, `E-mail`) VALUES
# (1, 'Nowa Era', 'Malych Lotników 1', 'MalychLotników@interia.pl')

"""with cursor(**db_credentials) as c:
c.execute("describe Brands_related_to_your_search;")
re = c.fetchall()
desc = c.description
print(re)
print([a[0] for a in desc])"""

with cursor(**db_credentials) as c:
    c.execute(f"INSERT INTO `Brands_related_to_your_search` (`Atrybut_text`, `img`) VALUES (`{str('text')}`, LOAD_FILE(`../Screenshots/Brands related to your search/{'com.amazon.mShop.navigation.MainActivity2022_03_31_122114.png'}.png`));")
