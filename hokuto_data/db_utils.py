import logging
import sqlalchemy as sa

# from sqlalchemy.exc import OperationalError, IntegrityError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(formatter_str)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# Add another logger to log SQLAlchemy operations
logger_sa = logging.getLogger("sqlalchemy.engine.base")
logger_sa.setLevel(logging.INFO)
logger_sa.addHandler(ch)


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


def delete_all(engine, table_name):
    logger.warning(f"Delete all records from table {table_name}")
    table = get_table(engine, table_name)
    engine.execute(table.delete())


def alembic_revision(conn):
    result = conn.execute("""SELECT * FROM "alembic_version";""").fetchone()
    db_revision = result._row[0]
    logger.info(f"DB revision (alembic_version): {db_revision}")
    return db_revision