import strawberry
import GraphQL.Models as GQLModels
import fastapi.exceptions as HTTPException
from typing import Dict, NewType, Any
import json


# def parseJSON(v: str) -> dict:
#     try:
#         print("Call parse", v)
#         python_obj = json.loads(v)

#         return python_obj

#     except json.JSONDecodeError as e:
#         raise Exception(f"Error parsing JSON: {e}")


# def serialize(v):
#     print("Call serialize", v)
#     return v


# JSON = strawberry.scalar(
#     NewType("JSON", object),
#     description="The `JSON` scalar type represents JSON values as specified by ECMA-404",
#     serialize=serialize,
#     parse_value=parseJSON,
# )


@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_table_item(
        self,
        t_name: str,
        item: str,
    ) -> GQLModels.ModelsUnion:
        try:
            cls = GQLModels.tables[t_name]

            item = cls.Input.parse_raw(item)
            res = cls.create(item)
            res = GQLModels.convert(cls, res)

            return res

        except Exception as e:
            raise e

    @strawberry.mutation
    def update_table_item(
        self,
        t_name: str,
        id: int,
        item: str,
    ) -> GQLModels.ModelsUnion:
        try:
            cls = GQLModels.tables[t_name]

            item = cls.Input.parse_raw(item)
            res = cls.update(id, item)
            res = GQLModels.convert(cls, res)

            return res

        except Exception as e:
            raise e

    @strawberry.mutation
    def delete_table_item(self, t_name: str, id: int) -> str:
        try:
            res = GQLModels.tables[t_name].delete(id)
            return res

        except Exception as e:
            raise e

    @strawberry.mutation
    def delete_table(self, t_name: str) -> str:
        try:
            res = GQLModels.tables[t_name].delete_table()
            return res

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    
