from Database.Database import get_db
from dataclasses import dataclass, field
from sqlalchemy import func, text


def execute_function(f_name: str, **kwargs):
    with get_db() as session:

        params = [f":{key}" for key in kwargs.keys()]
        params = ", ".join(params)

        query = text(f"SELECT * FROM {f_name}({params})")

        result = session.execute(query, kwargs)
        response = result.fetchall()

        return response

