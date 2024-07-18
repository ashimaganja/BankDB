from sqlalchemy import Boolean, Column, Integer, String, Date, Time, FLOAT, ForeignKey
from routers import (db_access)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Bank(Base):
    __tablename__ = 'bank'

    bank_id = Column(String(50), primary_key=True, index=True)
    bank_name = Column(String(50))
    date = Column(Date)
    time = Column(Time)

class Creditcard(Base):
    __tablename__ = 'creditcard'

    credit_card_id = Column(String(50), primary_key=True, index=True)
    bank_id = Column(String(50))
    limit = Column(FLOAT)
    credit_zipcode = Column(Integer)
    date = Column(Date)
    time = Column(Time)


class Fraud(Base):
    __tablename__ = 'fraud'

    fraud_id =  Column(String(50), primary_key=True, index=True)
    issuer = Column(String(50))
    date = Column(Date)
    time = Column(Time)
    

class Transaction(Base):
    __tablename__ = 'Transactions'

    transaction_id = Column(String(50), primary_key=True, index=True)
    credit_card_id = Column(String(50))
    amount = Column(FLOAT(8,2))
    vendor_name = Column(String(50))
    vendor_zipcode = Column(Integer)
    date = Column(Date)
    time = Column(Time)


class Demographic(Base):
    __tablename__ = 'Demographics'

    demographic_id = Column(String(50),primary_key=True, index=True )
    credit_card_id = Column(String(50))
    customer_name = Column(String(50))
    home_zipcode = Column(Integer)
    date = Column(Date)
    time = Column(Time)



