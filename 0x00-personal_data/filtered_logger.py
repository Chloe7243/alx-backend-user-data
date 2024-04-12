#!/usr/bin/env python3
""" Filter datum """
import re
import logging
from os import getenv
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.__fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Formatter"""
        record.msg = filter_datum(
            self.__fields, self.REDACTION, record.msg, self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Filter datum"""
    for f in fields:
        message = re.sub(f"{f}=.+?{separator}",
                         f"{f}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """Returns a logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a database Connection"""
    username = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username, password=password, host=host, database=db_name
    )


def main() -> None:
    """
    The function will obtain a database connection using get_db
    and retrieve all rows in the users table and display
    each row under a filtered format
    """
    logger = get_logger()
    logger.setLevel(logging.INFO)

    # Obtain a database connection
    db = get_db()
    cursor = db.cursor()

    # Retrieve all rows in the users table
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Display each row under a filtered format
    for row in rows:
        message = "; ".join([f"{field}={row[field]}" for field in row.keys()])
        logger.info(
            filter_datum(
                PII_FIELDS,
                RedactingFormatter.REDACTION,
                message,
                RedactingFormatter.SEPARATOR,
            )
        )


if __name__ == "__main__":
    main()
