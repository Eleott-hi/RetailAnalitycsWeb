import strawberry
from datetime import datetime
from typing import List, Dict
from Database.Database import get_db
import Database.Models as DBModels
from sqlalchemy.orm import Query
import Database.CRUD as CRUD


@strawberry.type
class PersonalData:
    id: int
    name: str
    surname: str
    email: str
    phone: str

    @strawberry.field
    def cards(self) -> List["Card"]:
        def f(q): return q.filter(DBModels.Card.customer_id == self.id)
        return CRUD.all(DBModels.Card, f)

    @classmethod
    def all(self) -> List['PersonalData']:
        return CRUD.all(DBModels.PersonalData)

    @classmethod
    def get(self, id: int) -> 'PersonalData':
        def f(q): return q.filter(DBModels.PersonalData.id == id)
        return CRUD.get(DBModels.PersonalData, f)

    @classmethod
    def create(self,  name: str, surname: str, email: str, phone: str) -> 'PersonalData':
        return CRUD.create(DBModels.PersonalData, name=name, surname=surname, email=email, phone=phone)

    @classmethod
    def update(self, id: int, name: str, surname: str, email: str, phone: str) -> 'PersonalData':
        def f(q): return q.filter(DBModels.PersonalData.id == id)
        return CRUD.update(DBModels.PersonalData, f, name=name, surname=surname, email=email, phone=phone)

    @classmethod
    def delete(self, id: int) -> str:
        def f(q): return q.filter(DBModels.PersonalData.id == id)
        return CRUD.delete(DBModels.PersonalData, f)


@strawberry.type
class Card:
    id: int
    customer_id: int

    @strawberry.field
    def customer(self) -> PersonalData:
        return PersonalData.get(id=self.customer_id)

    @strawberry.field
    def transactions(self) -> List['Transaction']:
        def f(q): return q.filter(DBModels.Transaction.card_id == self.id)
        return CRUD.all(DBModels.Transaction, f)

    @classmethod
    def all(self) -> List['Card']:
        return CRUD.all(DBModels.Card)

    @classmethod
    def get(self, id: int) -> 'Card':
        def f(q): return q.filter(DBModels.Card.id == id)
        return CRUD.get(DBModels.Card, f)

    @classmethod
    def create(self, customer_id: int) -> 'Card':
        return CRUD.create(DBModels.Card, customer_id=customer_id)

    @classmethod
    def update(self, id: int, customer_id: int) -> 'Card':
        def f(q): return q.filter(DBModels.Card.id == id)
        return CRUD.update(DBModels.Card, f, customer_id=customer_id)

    @classmethod
    def delete(self, id: int) -> str:
        def f(q): return q.filter(DBModels.Card.id == id)
        return CRUD.delete(DBModels.Card, f)


@strawberry.type
class GroupSKU:
    id: int
    name: str

    @strawberry.field
    def skus(self) -> List['SKU']:
        def f(q): return q.filter(DBModels.SKU.group_id == self.id)
        return CRUD.all(DBModels.SKU, f)

    @classmethod
    def all(self) -> List['GroupSKU']:
        return CRUD.all(DBModels.GroupSKU)

    @classmethod
    def get(self, id: int) -> 'GroupSKU':
        def f(q): return q.filter(DBModels.GroupSKU.id == id)
        return CRUD.get(DBModels.GroupSKU, f)

    @classmethod
    def create(self, name: str) -> 'GroupSKU':
        return CRUD.create(DBModels.GroupSKU, name=name)

    @classmethod
    def update(self, id: int, name: str) -> 'GroupSKU':
        def f(q): return q.filter(DBModels.GroupSKU.id == id)
        return CRUD.update(DBModels.GroupSKU, f, name=name)

    @classmethod
    def delete(self, id: int) -> str:
        def f(q): return q.filter(DBModels.GroupSKU.id == id)
        return CRUD.delete(DBModels.GroupSKU, f)


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
        def f(q): return q.filter(DBModels.Store.sku_id == self.id)
        return CRUD.all(DBModels.Store, f)

    @strawberry.field
    def checks(self) -> List['Check']:
        def f(q): return q.filter(DBModels.Check.sku_id == self.id)
        return CRUD.all(DBModels.Check, f)

    @classmethod
    def all(self) -> List['SKU']:
        return CRUD.all(DBModels.SKU)

    @classmethod
    def get(self, id: int) -> 'SKU':
        def f(q): return q.filter(DBModels.SKU.id == id)
        return CRUD.get(DBModels.SKU, f)

    @classmethod
    def create(self, name: str, group_id: int) -> 'SKU':
        return CRUD.create(DBModels.SKU, name=name, group_id=group_id)

    @classmethod
    def update(self, id: int, name: str, group_id: int) -> 'SKU':
        def f(q): return q.filter(DBModels.SKU.id == id)
        return CRUD.update(DBModels.SKU, f, name=name, group_id=group_id)

    @classmethod
    def delete(self, id: int) -> str:
        def f(q): return q.filter(DBModels.SKU.id == id)
        return CRUD.delete(DBModels.SKU, f)


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
        def f(q): return q.filter(DBModels.Transaction.store_id == self.id)
        return CRUD.all(DBModels.Transaction, f)

    @classmethod
    def all(self) -> List['Store']:
        return CRUD.all(DBModels.Store)

    @classmethod
    def get(self, id: int) -> 'Store':
        def f(q): return q.filter(DBModels.Store.id == id)
        return CRUD.get(DBModels.Store, f)

    @classmethod
    def create(self, sku_id: int, purchase_price: float, retail_price: float) -> 'Store':
        return CRUD.create(DBModels.Store, sku_id=sku_id, purchase_price=purchase_price, retail_price=retail_price)

    @classmethod
    def update(self, id: int, sku_id: int, purchase_price: float, retail_price: float) -> 'Store':
        def f(q): return q.filter(DBModels.Store.id == id)
        return CRUD.update(DBModels.Store, f, sku_id=sku_id, purchase_price=purchase_price, retail_price=retail_price)

    @classmethod
    def delete(self, id: int) -> str:
        def f(q): return q.filter(DBModels.Store.id == id)
        return CRUD.delete(DBModels.Store, f)


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
        def f(q): return q.filter(DBModels.Check.transaction_id == self.id)
        return CRUD.get(DBModels.Check, f)

    @classmethod
    def all(self) -> List['Transaction']:
        return CRUD.all(DBModels.Transaction)

    @classmethod
    def get(self, id: int) -> 'Transaction':
        def f(q): return q.filter(DBModels.Transaction.id == id)
        return CRUD.get(DBModels.Transaction, f)

    @classmethod
    def create(self, card_id: int, sum: float, datetime: str, store_id: int) -> 'Transaction':
        return CRUD.create(DBModels.Transaction, card_id=card_id, sum=sum, datetime=datetime, store_id=store_id)

    @classmethod
    def update(self, id: int, card_id: int, sum: float, datetime: str, store_id: int) -> 'Transaction':
        def f(q): return q.filter(DBModels.Transaction.id == id)
        return CRUD.update(DBModels.Transaction, f, card_id=card_id, sum=sum, datetime=datetime, store_id=store_id)


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
        return CRUD.all(DBModels.Check)

    @classmethod
    def get(self, transaction_id: int) -> 'Check':
        def f(q): return q.filter(
            DBModels.Check.transaction_id == transaction_id)
        return CRUD.get(DBModels.Check, f)


@strawberry.type
class DateOfAnalysisFormation:
    date: datetime

    @classmethod
    def all(self) -> List['DateOfAnalysisFormation']:
        return CRUD.all(DBModels.DateOfAnalysisFormation)


@strawberry.type
class Segment:
    segment: int
    average_check: str
    purchase_frequency: str
    churn_probability: str

    @classmethod
    def all(self) -> List['Segment']:
        return CRUD.all(DBModels.Segment)
