import logging
import sqlalchemy as sa
from sqlalchemy.exc import OperationalError, IntegrityError


# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("sqlalchemy.engine.base")
# logger.setLevel(logging.DEBUG)
# logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
formatter_str = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(formatter_str)


def get_table(engine, table_name):
    """Connect to a pre-existing table via reflection.

    Parameters
    ----------
    engine : sqlalchemy.engine.base.Engine
    table_name : str

    Returns
    -------
    table : sqlalchemy.sql.schema.Table
    """
    table = sa.Table(table_name, sa.MetaData(engine), autoload=True)
    return table


def bulk_insert(db_uri, table_name, data):
    engine = sa.create_engine(db_uri)
    conn = engine.connect()
    table = get_table(engine, table_name)
    clause = table.insert()
    conn.execute(clause, data)


# engine.connect()
# conn.execute("""SELECT * FROM "alembic_version";""").fetchone()
