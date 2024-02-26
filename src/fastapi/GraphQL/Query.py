import strawberry
from typing import List, Optional, Union
import GraphQL.Models as GQLModels


@strawberry.type
class Query:

    @strawberry.field
    def tables(self) -> List[str]:
        return [table for table in GQLModels.tables.keys()]

    @strawberry.field
    def table_fields(self, t_name: str) -> List[str]:
        try:

            return GQLModels.tables[t_name].fields()
        except Exception as e:
            raise e

    @strawberry.field
    def table_all(self, t_name: str) -> List[GQLModels.ModelsUnion]:
        try:
            cls = GQLModels.tables[t_name]
            items = cls.all()
            items = [GQLModels.convert(cls, item) for item in items]

            return items

        except Exception as e:
            raise e

    @strawberry.field
    def table_one(self, t_name: str, id: int) -> GQLModels.ModelsUnion:
        try:
            cls = GQLModels.tables[t_name]
            item = cls.get(id=id)
            item = GQLModels.convert(cls, item)

            return item

        except Exception as e:
            raise e
