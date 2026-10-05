from sqlalchemy import text

from app.db.database import engine


def test_test_database_connection():
    with engine.connect() as connection:
        database_name = connection.execute(
            text("SELECT current_database()")
        ).scalar_one()

    assert database_name == "personal_os_test"