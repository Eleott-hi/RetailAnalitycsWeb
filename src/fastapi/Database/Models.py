from sqlalchemy import Column, Integer, BigInteger, Numeric, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PersonalData(Base):
    __tablename__ = 'personal_data'

    id = Column("customer_id", BigInteger, primary_key=True)
    name = Column("customer_name", String(100), nullable=False)
    surname = Column("customer_surname", String(100), nullable=False)
    email = Column("customer_primary_email", String(100), unique=True)
    phone = Column("customer_primary_phone", String(12), unique=True)

    cards = relationship("Card", back_populates="customer")


class Card(Base):
    __tablename__ = 'cards'

    id = Column("customer_card_id", Integer,
                primary_key=True, autoincrement=True)
    customer_id = Column(BigInteger, ForeignKey('personal_data.customer_id'))

    customer = relationship("PersonalData", back_populates="cards")
    transactions = relationship("Transaction", back_populates="card")


class GroupSKU(Base):
    __tablename__ = 'group_sku'

    id = Column("group_id", Integer, primary_key=True)
    name = Column("group_name", String, unique=True, nullable=False)

    skus = relationship("SKU", back_populates="group")


class SKU(Base):
    __tablename__ = 'sku'

    id = Column('sku_id', Integer, primary_key=True)
    name = Column('sku_name', String(100), nullable=False)
    group_id = Column(BigInteger, ForeignKey('group_sku.group_id'))

    group = relationship("GroupSKU", back_populates="skus")
    stores = relationship("Store", back_populates="sku")
    checks = relationship("Check", back_populates="sku")


class Store(Base):
    __tablename__ = 'stores'

    id = Column('transaction_store_id', BigInteger,
                primary_key=True, nullable=False, autoincrement=True)
    sku_id = Column('sku_id', BigInteger, ForeignKey('sku.sku_id'))
    purchase_price = Column('sku_purchase_price', Numeric, nullable=False)
    retail_price = Column('sku_retail_price', Numeric, nullable=False)

    sku = relationship("SKU", back_populates="stores")
    transactions = relationship("Transaction", back_populates="store")


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column('transaction_id', Integer,
                primary_key=True, autoincrement=True)
    card_id = Column('customer_card_id', BigInteger,
                     ForeignKey('cards.customer_card_id'))
    sum = Column('transaction_summ', Numeric)
    datetime = Column('transaction_datetime', TIMESTAMP)
    store_id = Column('transaction_store_id', BigInteger,
                      ForeignKey('stores.transaction_store_id'))

    card = relationship("Card", back_populates="transactions")
    store = relationship("Store", back_populates="transactions")
    check = relationship("Check", back_populates="transaction")


class Check(Base):
    __tablename__ = 'checks'

    transaction_id = Column(BigInteger, ForeignKey(
        'transactions.transaction_id'), primary_key=True)
    sku_id = Column(BigInteger, ForeignKey('sku.sku_id'), primary_key=True)
    sku_amount = Column(Numeric, nullable=False)
    sku_summ = Column(Numeric, nullable=False)
    sku_summ_paid = Column(Numeric, nullable=False)
    sku_discount = Column(Numeric, nullable=False)

    transaction = relationship("Transaction", back_populates="check")
    sku = relationship("SKU", back_populates="checks")


class DateOfAnalysisFormation(Base):
    __tablename__ = 'date_of_analysis_formation'

    date = Column('analysis_date', TIMESTAMP, primary_key=True)


class Segment(Base):
    __tablename__ = 'segments'

    segment = Column(Integer, primary_key=True)
    average_check = Column(String(50), nullable=False)
    purchase_frequency = Column(String(50), nullable=False)
    churn_probability = Column(String(50), nullable=False)
