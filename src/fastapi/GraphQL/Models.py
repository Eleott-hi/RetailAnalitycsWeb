import strawberry
from datetime import datetime
from typing import List, Dict
from database.Database import get_db
import database.Models as DBModels
from sqlalchemy.orm import Query
import repositories.CRUD as CRUD


@strawberry.type
class PersonalData:
    id: int
    name: str
    surname: str
    email: str
    phone: str

    @strawberry.field
    def cards(self) -> List["Card"]:
        operations = CRUD.Operations(
            filters=[DBModels.Card.customer_id == self.id],
            orders_by=[DBModels.Card.id]
        )
        return CRUD.all(DBModels.Card, operations)

    @classmethod
    def all(self) -> List['PersonalData']:
        operations = CRUD.Operations(orders_by=[DBModels.PersonalData.id])
        return CRUD.all(DBModels.PersonalData, operations)

    @classmethod
    def get(self, id: int) -> 'PersonalData':
        operations = CRUD.Operations(filters=[DBModels.PersonalData.id == id])
        return CRUD.one(DBModels.PersonalData, operations)

    @classmethod
    def create(self,  name: str, surname: str, email: str, phone: str) -> 'PersonalData':
        return CRUD.create(DBModels.PersonalData, name=name, surname=surname, email=email, phone=phone)

    @classmethod
    def update(self, id: int, name: str, surname: str, email: str, phone: str) -> 'PersonalData':
        operations = CRUD.Operations(filters=[DBModels.PersonalData.id == id])
        return CRUD.update(DBModels.PersonalData, operations, name=name, surname=surname, email=email, phone=phone)

    @classmethod
    def delete(self, id: int) -> str:
        operations = CRUD.Operations(filters=[DBModels.PersonalData.id == id])
        return CRUD.delete(DBModels.PersonalData, operations)


@strawberry.type
class Card:
    id: int
    customer_id: int

    @strawberry.field
    def customer(self) -> PersonalData:
        return PersonalData.get(id=self.customer_id)

    @strawberry.field
    def transactions(self) -> List['Transaction']:
        operations = CRUD.Operations(
            filters=[DBModels.Transaction.card_id == self.id],
            orders_by=[DBModels.Transaction.id]
        )
        return CRUD.all(DBModels.Transaction, operations)

    @classmethod
    def all(self) -> List['Card']:
        operations = CRUD.Operations(orders_by=[DBModels.Card.id])
        return CRUD.all(DBModels.Card, operations)

    @classmethod
    def get(self, id: int) -> 'Card':
        operations = CRUD.Operations(filters=[DBModels.Card.id == id])
        return CRUD.one(DBModels.Card, operations)

    @classmethod
    def create(self, customer_id: int) -> 'Card':
        return CRUD.create(DBModels.Card, customer_id=customer_id)

    @classmethod
    def update(self, id: int, customer_id: int) -> 'Card':
        operations = CRUD.Operations(filters=[DBModels.Card.id == id])
        return CRUD.update(DBModels.Card, operations, customer_id=customer_id)

    @classmethod
    def delete(self, id: int) -> str:
        operations = CRUD.Operations(filters=[DBModels.Card.id == id])
        return CRUD.delete(DBModels.Card, operations)


@strawberry.type
class GroupSKU:
    id: int
    name: str

    @strawberry.field
    def skus(self) -> List['SKU']:
        operations = CRUD.Operations(
            filters=[DBModels.SKU.group_id == self.id],
            orders_by=[DBModels.SKU.id]
        )
        return CRUD.all(DBModels.SKU, operations)

    @classmethod
    def all(self) -> List['GroupSKU']:
        operations = CRUD.Operations(orders_by=[DBModels.GroupSKU.id])
        return CRUD.all(DBModels.GroupSKU, operations)

    @classmethod
    def get(self, id: int) -> 'GroupSKU':
        def f(q): return q.filter(DBModels.GroupSKU.id == id)
        return CRUD.one(DBModels.GroupSKU, f)

    @classmethod
    def create(self, name: str) -> 'GroupSKU':
        return CRUD.create(DBModels.GroupSKU, name=name)

    @classmethod
    def update(self, id: int, name: str) -> 'GroupSKU':
        operations = CRUD.Operations(filters=[DBModels.GroupSKU.id == id])
        return CRUD.update(DBModels.GroupSKU, operations, name=name)

    @classmethod
    def delete(self, id: int) -> str:
        operations = CRUD.Operations(filters=[DBModels.GroupSKU.id == id])
        return CRUD.delete(DBModels.GroupSKU, operations)


@strawberry.type
class SKU:
    id: int
    name: str
    group_id: int

    @strawberry.field
    def group(self) -> GroupSKU:
        return GroupSKU.get(id=self.group_id)

    @strawberry.field
    def stores(self) -> List['Store']:
        operations = CRUD.Operations(
            DBModels.Store.sku_id == self.id,
            orders_by=[DBModels.Store.id]
        )
        return CRUD.all(DBModels.Store, operations)

    @strawberry.field
    def checks(self) -> List['Check']:
        operations = CRUD.Operations(
            filters=[DBModels.Check.sku_id == self.id],
            orders_by=[DBModels.Check.id]
        )
        return CRUD.all(DBModels.Check, operations)

    @classmethod
    def all(self) -> List['SKU']:
        operations = CRUD.Operations(orders_by=[DBModels.SKU.id])
        return CRUD.all(DBModels.SKU, operations)

    @classmethod
    def get(self, id: int) -> 'SKU':
        operations = CRUD.Operations(filters=[DBModels.SKU.id == id])
        return CRUD.one(DBModels.SKU, operations)

    @classmethod
    def create(self, name: str, group_id: int) -> 'SKU':
        return CRUD.create(DBModels.SKU, name=name, group_id=group_id)

    @classmethod
    def update(self, id: int, name: str, group_id: int) -> 'SKU':
        operations = CRUD.Operations(filters=[DBModels.SKU.id == id])
        return CRUD.update(DBModels.SKU, operations, name=name, group_id=group_id)

    @classmethod
    def delete(self, id: int) -> str:
        operations = CRUD.Operations(filters=[DBModels.SKU.id == id])
        return CRUD.delete(DBModels.SKU, operations)


@strawberry.type
class Store:
    id: int
    sku_id: int
    purchase_price: float
    retail_price: float

    @strawberry.field
    def sku(self) -> SKU:
        return SKU.get(id=self.sku_id)

    @strawberry.field
    def transactions(self) -> List['Transaction']:
        operations = CRUD.Operations(
            filters=[DBModels.Transaction.store_id == self.id],
            orders_by=[DBModels.Transaction.id]
        )
        return CRUD.all(DBModels.Transaction, operations)

    @classmethod
    def all(self) -> List['Store']:
        operations = CRUD.Operations(orders_by=[DBModels.Store.id])
        return CRUD.all(DBModels.Store, operations)

    @classmethod
    def get(self, id: int) -> 'Store':
        operations = CRUD.Operations(filters=[DBModels.Store.id == id])
        return CRUD.one(DBModels.Store, operations)

    @classmethod
    def create(self, sku_id: int, purchase_price: float, retail_price: float) -> 'Store':
        return CRUD.create(DBModels.Store, sku_id=sku_id, purchase_price=purchase_price, retail_price=retail_price)

    @classmethod
    def update(self, id: int, sku_id: int, purchase_price: float, retail_price: float) -> 'Store':
        operations = CRUD.Operations(filters=[DBModels.Store.id == id])
        return CRUD.update(DBModels.Store, operations, sku_id=sku_id, purchase_price=purchase_price, retail_price=retail_price)

    @classmethod
    def delete(self, id: int) -> str:
        operations = CRUD.Operations(filters=[DBModels.Store.id == id])
        return CRUD.delete(DBModels.Store, operations)


@strawberry.type
class Transaction:
    id: int
    card_id: int
    sum: float
    datetime: str
    store_id: int

    @strawberry.field
    def card(self) -> Card:
        return Card.get(id=self.card_id)

    @strawberry.field
    def store(self) -> Store:
        return Store.get(id=self.store_id)

    @strawberry.field
    def check(self) -> 'Check':
        operations = CRUD.Operations(
            filters=[DBModels.Check.transaction_id == self.id]
        )
        return CRUD.one(DBModels.Check, operations)

    @classmethod
    def all(self) -> List['Transaction']:
        operations = CRUD.Operations(orders_by=[DBModels.Transaction.id])
        return CRUD.all(DBModels.Transaction, operations)

    @classmethod
    def get(self, id: int) -> 'Transaction':
        operations = CRUD.Operations(filters=[DBModels.Transaction.id == id])
        return CRUD.one(DBModels.Transaction, operations)

    @classmethod
    def create(self, card_id: int, sum: float, datetime: str, store_id: int) -> 'Transaction':
        return CRUD.create(DBModels.Transaction, card_id=card_id, sum=sum, datetime=datetime, store_id=store_id)

    @classmethod
    def update(self, id: int, card_id: int, sum: float, datetime: str, store_id: int) -> 'Transaction':
        operations = CRUD.Operations(filters=[DBModels.Transaction.id == id])
        return CRUD.update(DBModels.Transaction, operations, card_id=card_id, sum=sum, datetime=datetime, store_id=store_id)


@strawberry.type
class Check:
    transaction_id: int
    sku_id: int
    sku_amount: float
    sku_summ: float
    sku_summ_paid: float
    sku_discount: float

    @strawberry.field
    def transaction(self) -> Transaction:
        return Transaction.get(id=self.transaction_id)

    @strawberry.field
    def sku(self) -> SKU:
        return SKU.get(id=self.sku_id)

    @classmethod
    def all(self) -> List['Check']:
        operations = CRUD.Operations(orders_by=[DBModels.Check.transaction_id])
        return CRUD.all(DBModels.Check, operations)

    @classmethod
    def get(self, transaction_id: int) -> 'Check':
        operations = CRUD.Operations(
            filters=[DBModels.Check.transaction_id == transaction_id])
        return CRUD.one(DBModels.Check, operations)


@strawberry.type
class DateOfAnalysisFormation:
    date: datetime

    @classmethod
    def all(self) -> List['DateOfAnalysisFormation']:
        operations = CRUD.Operations(
            orders_by=[DBModels.DateOfAnalysisFormation.date]
        )
        return CRUD.all(DBModels.DateOfAnalysisFormation, operations)


@strawberry.type
class Segment:
    segment: int
    average_check: str
    purchase_frequency: str
    churn_probability: str

    @classmethod
    def all(self) -> List['Segment']:
        operations = CRUD.Operations(orders_by=[DBModels.Segment.segment])
        return CRUD.all(DBModels.Segment, operations)
