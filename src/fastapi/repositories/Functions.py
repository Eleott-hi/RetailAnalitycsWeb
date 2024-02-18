from database.Database import get_db
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


# def execute_query(query) -> list[any]:

#     with get_db() as session:
#         groups = 3
#         max_churn_rate = 3
#         max_stability_index = 0.5
#         max_sku_share = 100
#         max_margin_share = 30

#         result = session.query(
#             func.fnc_personal_offers_aimed_at_cross_selling(
#                 groups,
#                 max_churn_rate,
#                 max_stability_index,
#                 max_sku_share,
#                 max_margin_share
#             )
#         ).all()

#         print('RESULT:', result)


#         return []
