import logging
import sqlalchemy as sa


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("sqlalchemy.engine.base")
logger.setLevel(logging.DEBUG)


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


def create_characters_table(db_uri):
    engine = sa.create_engine(db_uri)
    metadata = sa.MetaData()
    characters = sa.Table(
        "characters",
        metadata,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(25), nullable=False),
        sa.Column("url", sa.String(25), nullable=True),
        sa.Column("is_not_in_manga", sa.Boolean, nullable=False),
    )
    logger.debug(metadata.tables)

    # Store in the DB the schema we have just defined
    metadata.create_all(engine)
    return characters


def bulk_insert(db_uri, table, data):
    engine = sa.create_engine(db_uri)
    conn = engine.connect()
    clause = table.insert()
    conn.execute(clause, data)


def insert(conn, table, datum):
    clause = table.insert()
    conn.execute(clause, datum)
