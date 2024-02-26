import strawberry
from datetime import datetime
from typing import List, Any
import Database.Models as DBModels
import repositories.CRUD as CRUD
from pydantic import BaseModel


def convert(cls: type, obj: Any):
    return cls(**{f: getattr(obj, f) for f in cls.fields()})


@strawberry.type
class PersonalData:
    id: int
    name: str
    surname: str
    email: str
    phone: str

    class Input(BaseModel):
        name: str
        surname: str
        email: str
        phone: str

    @classmethod
    def fields(self) -> List[str]:
        return ["id", "name", "surname", "email", "phone"]

    @strawberry.field
    def cards(self) -> List["Card"]:
        operations = CRUD.Operations(
            filters=[DBModels.Card.customer_id == self.id], orders_by=[DBModels.Card.id]
        )
        return CRUD.all(DBModels.Card, operations)

    @classmethod
    def all(self) -> List["PersonalData"]:
        operations = CRUD.Operations(orders_by=[DBModels.PersonalData.id])
        return CRUD.all(DBModels.PersonalData, operations)

    @classmethod
    def get(self, id: int) -> "PersonalData":
        operations = CRUD.Operations(filters=[DBModels.PersonalData.id == id])
        return CRUD.one(DBModels.PersonalData, operations)

    @classmethod
    def update(self, id: int, item: Input) -> "PersonalData":
        operations = CRUD.Operations(filters=[DBModels.PersonalData.id == id])
        return CRUD.update(DBModels.PersonalData, operations, **item.dict())

    @classmethod
    def create(self, item: Input) -> "PersonalData":
        return CRUD.create(DBModels.PersonalData, **item.dict())

    @classmethod
    def delete(self, id: int) -> str:
        operations = CRUD.Operations(filters=[DBModels.PersonalData.id == id])
        return CRUD.delete(DBModels.PersonalData, operations)

    @classmethod
    def delete_table(self) -> str:
        return CRUD.delete_table(DBModels.PersonalData)


@strawberry.type
class Card:
    id: int
    customer_id: int

    class Input(BaseModel):
        customer_id: int

    @classmethod
    def fields(self) -> List[str]:
        return ["id", "customer_id"]

    @strawberry.field
    def customer(self) -> PersonalData:
        return PersonalData.get(id=self.customer_id)

    @strawberry.field
    def transactions(self) -> List["Transaction"]:
        operations = CRUD.Operations(
            filters=[DBModels.Transaction.card_id == self.id],
            orders_by=[DBModels.Transaction.id],
        )
        return CRUD.all(DBModels.Transaction, operations)

    @classmethod
    def all(self) -> List["Card"]:
        operations = CRUD.Operations(orders_by=[DBModels.Card.id])
        return CRUD.all(DBModels.Card, operations)

    @classmethod
    def get(self, id: int) -> "Card":
        operations = CRUD.Operations(filters=[DBModels.Card.id == id])
        return CRUD.one(DBModels.Card, operations)

    @classmethod
    def create(self, customer_id: int) -> "Card":
        return CRUD.create(DBModels.Card, customer_id=customer_id)

    @classmethod
    def update(self, id: int, customer_id: int) -> "Card":
        operations = CRUD.Operations(filters=[DBModels.Card.id == id])
        return CRUD.update(DBModels.Card, operations, customer_id=customer_id)

    @classmethod
    def delete(self, id: int) -> str:
        operations = CRUD.Operations(filters=[DBModels.Card.id == id])
        return CRUD.delete(DBModels.Card, operations)

    @classmethod
    def delete_table(self) -> str:
        return CRUD.delete_table(DBModels.Card)


@strawberry.type
class GroupSKU:
    id: int
    name: str

    class Input(BaseModel):
        name: str

    @classmethod
    def fields(self) -> List[str]:
        return ["id", "name"]

    @strawberry.field
    def skus(self) -> List["SKU"]:
        operations = CRUD.Operations(
            filters=[DBModels.SKU.group_id == self.id], orders_by=[DBModels.SKU.id]
        )
        return CRUD.all(DBModels.SKU, operations)

    @classmethod
    def all(self) -> List["GroupSKU"]:
        operations = CRUD.Operations(orders_by=[DBModels.GroupSKU.id])
        return CRUD.all(DBModels.GroupSKU, operations)

    @classmethod
    def get(self, id: int) -> "GroupSKU":
        def f(q):
            return q.filter(DBModels.GroupSKU.id == id)

        return CRUD.one(DBModels.GroupSKU, f)

    @classmethod
    def create(self, name: str) -> "GroupSKU":
        return CRUD.create(DBModels.GroupSKU, name=name)

    @classmethod
    def update(self, id: int, name: str) -> "GroupSKU":
        operations = CRUD.Operations(filters=[DBModels.GroupSKU.id == id])
        return CRUD.update(DBModels.GroupSKU, operations, name=name)

    @classmethod
    def delete(self, id: int) -> str:
        operations = CRUD.Operations(filters=[DBModels.GroupSKU.id == id])
        return CRUD.delete(DBModels.GroupSKU, operations)

    @classmethod
    def delete_table(self) -> str:
        return CRUD.delete_table(DBModels.GroupSKU)


@strawberry.type
class SKU:
    id: int
    name: str
    group_id: int

    class Input(BaseModel):
        name: str
        group_id: int

    @classmethod
    def fields(self) -> List[str]:
        return ["id", "name", "group_id"]

    @strawberry.field
    def group(self) -> GroupSKU:
        return GroupSKU.get(id=self.group_id)

    @strawberry.field
    def stores(self) -> List["Store"]:
        operations = CRUD.Operations(
            DBModels.Store.sku_id == self.id, orders_by=[DBModels.Store.id]
        )
        return CRUD.all(DBModels.Store, operations)

    @strawberry.field
    def checks(self) -> List["Check"]:
        operations = CRUD.Operations(
            filters=[DBModels.Check.sku_id == self.id], orders_by=[DBModels.Check.id]
        )
        return CRUD.all(DBModels.Check, operations)

    @classmethod
    def all(self) -> List["SKU"]:
        operations = CRUD.Operations(orders_by=[DBModels.SKU.id])
        return CRUD.all(DBModels.SKU, operations)

    @classmethod
    def get(self, id: int) -> "SKU":
        operations = CRUD.Operations(filters=[DBModels.SKU.id == id])
        return CRUD.one(DBModels.SKU, operations)

    @classmethod
    def create(self, name: str, group_id: int) -> "SKU":
        return CRUD.create(DBModels.SKU, name=name, group_id=group_id)

    @classmethod
    def update(self, id: int, name: str, group_id: int) -> "SKU":
        operations = CRUD.Operations(filters=[DBModels.SKU.id == id])
        return CRUD.update(DBModels.SKU, operations, name=name, group_id=group_id)

    @classmethod
    def delete(self, id: int) -> str:
        operations = CRUD.Operations(filters=[DBModels.SKU.id == id])
        return CRUD.delete(DBModels.SKU, operations)

    @classmethod
    def delete_table(self) -> str:
        return CRUD.delete_table(DBModels.SKU)


@strawberry.type
class Store:
    id: int
    sku_id: int
    purchase_price: float
    retail_price: float

    class Input(BaseModel):
        sku_id: int
        purchase_price: float
        retail_price: float

    @classmethod
    def fields(self) -> List[str]:
        return ["id", "sku_id", "purchase_price", "retail_price"]

    @strawberry.field
    def sku(self) -> SKU:
        return SKU.get(id=self.sku_id)

    @strawberry.field
    def transactions(self) -> List["Transaction"]:
        operations = CRUD.Operations(
            filters=[DBModels.Transaction.store_id == self.id],
            orders_by=[DBModels.Transaction.id],
        )
        return CRUD.all(DBModels.Transaction, operations)

    @classmethod
    def all(self) -> List["Store"]:
        operations = CRUD.Operations(orders_by=[DBModels.Store.id])
        return CRUD.all(DBModels.Store, operations)

    @classmethod
    def get(self, id: int) -> "Store":
        operations = CRUD.Operations(filters=[DBModels.Store.id == id])
        return CRUD.one(DBModels.Store, operations)

    @classmethod
    def create(
        self, sku_id: int, purchase_price: float, retail_price: float
    ) -> "Store":
        return CRUD.create(
            DBModels.Store,
            sku_id=sku_id,
            purchase_price=purchase_price,
            retail_price=retail_price,
        )

    @classmethod
    def update(
        self, id: int, sku_id: int, purchase_price: float, retail_price: float
    ) -> "Store":
        operations = CRUD.Operations(filters=[DBModels.Store.id == id])
        return CRUD.update(
            DBModels.Store,
            operations,
            sku_id=sku_id,
            purchase_price=purchase_price,
            retail_price=retail_price,
        )

    @classmethod
    def delete(self, id: int) -> str:
        operations = CRUD.Operations(filters=[DBModels.Store.id == id])
        return CRUD.delete(DBModels.Store, operations)

    @classmethod
    def delete_table(self) -> str:
        return CRUD.delete_table(DBModels.Store)


@strawberry.type
class Transaction:
    id: int
    card_id: int
    sum: float
    datetime: str
    store_id: int

    class Input(BaseModel):
        card_id: int
        sum: float
        datetime: str
        store_id: int

    @classmethod
    def fields(self) -> List[str]:
        return ["id", "card_id", "sum", "datetime", "store_id"]

    @strawberry.field
    def card(self) -> Card:
        return Card.get(id=self.card_id)

    @strawberry.field
    def store(self) -> Store:
        return Store.get(id=self.store_id)

    @strawberry.field
    def check(self) -> "Check":
        operations = CRUD.Operations(filters=[DBModels.Check.transaction_id == self.id])
        return CRUD.one(DBModels.Check, operations)

    @classmethod
    def all(self) -> List["Transaction"]:
        operations = CRUD.Operations(orders_by=[DBModels.Transaction.id])
        return CRUD.all(DBModels.Transaction, operations)

    @classmethod
    def get(self, id: int) -> "Transaction":
        operations = CRUD.Operations(filters=[DBModels.Transaction.id == id])
        return CRUD.one(DBModels.Transaction, operations)

    @classmethod
    def create(
        self, card_id: int, sum: float, datetime: str, store_id: int
    ) -> "Transaction":
        return CRUD.create(
            DBModels.Transaction,
            card_id=card_id,
            sum=sum,
            datetime=datetime,
            store_id=store_id,
        )

    @classmethod
    def update(
        self, id: int, card_id: int, sum: float, datetime: str, store_id: int
    ) -> "Transaction":
        operations = CRUD.Operations(filters=[DBModels.Transaction.id == id])
        return CRUD.update(
            DBModels.Transaction,
            operations,
            card_id=card_id,
            sum=sum,
            datetime=datetime,
            store_id=store_id,
        )

    @classmethod
    def delete(self, id: int) -> str:
        operations = CRUD.Operations(filters=[DBModels.Transaction.id == id])
        return CRUD.delete(DBModels.Transaction, operations)

    @classmethod
    def delete_table(self) -> str:
        return CRUD.delete_table(DBModels.Transaction)


@strawberry.type
class Check:
    transaction_id: int
    sku_id: int
    sku_amount: float
    sku_summ: float
    sku_summ_paid: float
    sku_discount: float

    class Input(BaseModel):
        transaction_id: int
        sku_id: int
        sku_amount: float
        sku_summ: float
        sku_summ_paid: float
        sku_discount: float

    @classmethod
    def fields(self) -> List[str]:
        return [
            "transaction_id",
            "sku_id",
            "sku_amount",
            "sku_summ",
            "sku_summ_paid",
            "sku_discount",
        ]

    @strawberry.field
    def transaction(self) -> Transaction:
        return Transaction.get(id=self.transaction_id)

    @strawberry.field
    def sku(self) -> SKU:
        return SKU.get(id=self.sku_id)

    @classmethod
    def all(self) -> List["Check"]:
        operations = CRUD.Operations(orders_by=[DBModels.Check.transaction_id])
        return CRUD.all(DBModels.Check, operations)

    @classmethod
    def get(self, transaction_id: int) -> "Check":
        operations = CRUD.Operations(
            filters=[DBModels.Check.transaction_id == transaction_id]
        )
        return CRUD.one(DBModels.Check, operations)

    @classmethod
    def create(
        self,
        transaction_id: int,
        sku_id: int,
        sku_amount: float,
        sku_summ: float,
        sku_summ_paid: float,
        sku_discount: float,
    ) -> "Check":
        return CRUD.create(
            DBModels.Check,
            transaction_id=transaction_id,
            sku_id=sku_id,
            sku_amount=sku_amount,
            sku_summ=sku_summ,
            sku_summ_paid=sku_summ_paid,
            sku_discount=sku_discount,
        )

    @classmethod
    def delete(self, transaction_id: int) -> str:
        operations = CRUD.Operations(
            filters=[DBModels.Check.transaction_id == transaction_id]
        )
        return CRUD.delete(DBModels.Check, operations)

    @classmethod
    def delete_table(self) -> str:
        return CRUD.delete_table(DBModels.Check)


@strawberry.type
class DateOfAnalysisFormation:
    date: datetime

    class Input(BaseModel):
        date: datetime

    @classmethod
    def fields(self) -> List[str]:
        return ["date"]

    @classmethod
    def all(self) -> List["DateOfAnalysisFormation"]:
        operations = CRUD.Operations(orders_by=[DBModels.DateOfAnalysisFormation.date])
        return CRUD.all(DBModels.DateOfAnalysisFormation, operations)

    @classmethod
    def delete_table(self) -> str:
        return CRUD.delete_table(DBModels.DateOfAnalysisFormation)


@strawberry.type
class Segment:
    segment: int
    average_check: str
    purchase_frequency: str
    churn_probability: str

    class Input(BaseModel):
        segment: int
        average_check: str
        purchase_frequency: str
        churn_probability: str

    @classmethod
    def fields(self) -> List[str]:
        return ["segment", "average_check", "purchase_frequency", "churn_probability"]

    @classmethod
    def all(self) -> List["Segment"]:
        operations = CRUD.Operations(orders_by=[DBModels.Segment.segment])
        return CRUD.all(DBModels.Segment, operations)

    @classmethod
    def get(self, segment: int) -> "Segment":
        operations = CRUD.Operations(filters=[DBModels.Segment.segment == segment])
        return CRUD.one(DBModels.Segment, operations)

    @classmethod
    def create(
        self,
        average_check: str,
        purchase_frequency: str,
        churn_probability: str,
    ) -> "Segment":
        return CRUD.create(
            DBModels.Segment,
            average_check=average_check,
            purchase_frequency=purchase_frequency,
            churn_probability=churn_probability,
        )

    @classmethod
    def update(
        self,
        segment: int,
        average_check: str,
        purchase_frequency: str,
        churn_probability: str,
    ) -> "Segment":
        operations = CRUD.Operations(filters=[DBModels.Segment.segment == segment])
        return CRUD.update(
            DBModels.Segment,
            operations,
            average_check=average_check,
            purchase_frequency=purchase_frequency,
            churn_probability=churn_probability,
        )

    @classmethod
    def delete(self, segment: int) -> str:
        operations = CRUD.Operations(filters=[DBModels.Segment.segment == segment])
        return CRUD.delete(DBModels.Segment, operations)

    @classmethod
    def delete_table(self) -> str:
        return CRUD.delete_table(DBModels.Segment)


tables = {
    "PersonalData": PersonalData,
    "Card": Card,
    "GroupSKU": GroupSKU,
    "SKU": SKU,
    "Check": Check,
    "Store": Store,
    "Transaction": Transaction,
    "DateOfAnalysisFormation": DateOfAnalysisFormation,
    "Segment": Segment,
}

ModelsUnion = (
    PersonalData
    | Card
    | GroupSKU
    | SKU
    | Check
    | Store
    | Transaction
    | DateOfAnalysisFormation
    | Segment
)
