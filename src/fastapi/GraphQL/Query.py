import strawberry
from typing import List, Optional
import GraphQL.Models as GQLModels


@strawberry.type
class Query:

    @strawberry.field
    def tables(self) -> List[str]:
        return [
            "PersonalData",
            "Card",
            "GroupSKU",
            "SKU",
            "Check",
            "Store",
            "Transaction",
            "Analytics",
            "AnalisisDate",
            "Segment",
        ]

    @strawberry.field
    def personal_datas(self) -> List[GQLModels.PersonalData]:
        return GQLModels.PersonalData.all()

    @strawberry.field
    def personal_data(self, id: int) -> GQLModels.PersonalData:
        return GQLModels.PersonalData.get(id=id)

    @strawberry.field
    def personal_data_fields(self) -> List[str]:
        return GQLModels.PersonalData.fields()

    @strawberry.field
    def cards(self) -> List[GQLModels.Card]:
        return GQLModels.Card.all()

    @strawberry.field
    def card(self, id: int) -> GQLModels.Card:
        return GQLModels.Card.get(id=id)

    @strawberry.field
    def card_fields(self) -> List[str]:
        return GQLModels.Card.fields()

    @strawberry.field
    def sku_groups(self) -> List[GQLModels.GroupSKU]:
        return GQLModels.GroupSKU.all()

    @strawberry.field
    def sku_group(self, id: int) -> GQLModels.GroupSKU:
        return GQLModels.GroupSKU.get(id=id)

    @strawberry.field
    def sku_group_fields(self) -> List[str]:
        return GQLModels.GroupSKU.fields()

    @strawberry.field
    def skus(self) -> List[GQLModels.SKU]:
        return GQLModels.SKU.all()

    @strawberry.field
    def sku(self, id: int) -> GQLModels.SKU:
        return GQLModels.SKU.get(id=id)

    @strawberry.field
    def sku_fields(self) -> List[str]:
        return GQLModels.SKU.fields()

    @strawberry.field
    def stores(self) -> List[GQLModels.Store]:
        return GQLModels.Store.all()

    @strawberry.field
    def store(self, id: int) -> GQLModels.Store:
        return GQLModels.Store.get(id=id)

    @strawberry.field
    def store_fields(self) -> List[str]:
        return GQLModels.Store.fields()

    @strawberry.field
    def transactions(self) -> List[GQLModels.Transaction]:
        return GQLModels.Transaction.all()

    @strawberry.field
    def transaction(self, id: int) -> GQLModels.Transaction:
        return GQLModels.Transaction.get(id=id)

    @strawberry.field
    def transaction_fields(self) -> List[str]:
        return GQLModels.Transaction.fields()

    @strawberry.field
    def checks(self) -> List[GQLModels.Check]:
        return GQLModels.Check.all()

    @strawberry.field
    def check(self, transaction_id: int) -> GQLModels.Check:
        return GQLModels.Check.get(transaction_id=transaction_id)

    @strawberry.field
    def check_fields(self) -> List[str]:
        return GQLModels.Check.fields()

    @strawberry.field
    def analisis_dates(self) -> List[GQLModels.DateOfAnalysisFormation]:
        return GQLModels.DateOfAnalysisFormation.all()

    @strawberry.field
    def analisis_date_fields(self) -> List[str]:
        return GQLModels.DateOfAnalysisFormation.fields()

    @strawberry.field
    def segments(self) -> List[GQLModels.Segment]:
        return GQLModels.Segment.all()

    @strawberry.field
    def segment_fields(self) -> List[str]:
        return GQLModels.Segment.fields()
