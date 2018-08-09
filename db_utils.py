import logging
import sqlalchemy as sa
from sqlalchemy.exc import OperationalError


# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger("sqlalchemy.engine.base")
# logger.setLevel(logging.DEBUG)


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
    try:
        conn = engine.connect()
    except OperationalError as e:
        e.add_detail("CANNOT CONNECT TO DB")
        raise e

    table = get_table(engine, table_name)
    clause = table.insert()
    conn.execute(clause, data)


# engine.connect()
# conn.execute("""SELECT * FROM "alembic_version";""").fetchone()
