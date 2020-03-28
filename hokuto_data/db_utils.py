import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(formatter_str)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)


def delete_all(cursor, table_name):
    logger.warning(f"Delete all records from table {table_name}")
    cursor.execute(f"DELETE from {table_name}")
