from fastapi import APIRouter, Request, Form, Response,  Query, HTTPException, Depends, status
from fastapi.templating import Jinja2Templates
from typing import Annotated
from routers import (models)
import pandas as pd
import uuid
from pydantic import Field, constr, UUID4, BaseModel
from datetime import datetime, date, time
import os
import utils
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



router = APIRouter(prefix="/db", tags=["scripts"],)
templates = Jinja2Templates(directory="templates")
data_sources = ["fraud", "bank", "credit_card", "demographic", "transaction"]
URL_DATABASE = "mysql+pymysql://root:password@localhost:3306/fraudserver"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

models.Base.metadata.create_all(bind=engine)

class BankBase(BaseModel):
    bank_name: str
    date: date
    time: time

class CreditcardBase(BaseModel):

    limit: int
    credit_zipcode: int
    date: date
    time: time
    bank_id: str

class FraudBase(BaseModel):
      
    transaction_id : str
    issuer :str
    date : date
    time : time

class TransactionBase(BaseModel):
  
    credit_card_id :str
    amount : float
    vendor_name: str
    vendor_zipcode :int
    date :date
    time : time

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/transaction/{secret_id}", status_code=status.HTTP_201_CREATED)
@utils.check_secret_password(secret_id="password")
async def create_transaction(transaction: TransactionBase, db: db_dependency, secret_id:str ):
    transaction_data = transaction.model_dump()

    transaction_data.update({
        "transaction_id" : str(uuid.uuid4)
    })

    db_user = models.Transaction(**transaction_data)
    db.add(db_user)
    db.commit()


@router.post("/bank/{secret_id}", status_code= status.HTTP_201_CREATED)
@utils.check_secret_password(secret_id="password")
async def create_bank(bank: BankBase, db: db_dependency, secret_id:str):

    # Create a dictionary from the Pydantic model
    bank_data = bank.model_dump()
    
     # Manually add/modify values in the dictionary
    bank_data.update({
        "bank_id": str(uuid.uuid4())
    })

    db_user = models.Bank(**bank_data)
    db.add(db_user)
    db.commit()

@router.post("/fraud/{secret_id}", status_code= status.HTTP_201_CREATED)
@utils.check_secret_password(secret_id="password")
async def create_bank(fraud: FraudBase, db: db_dependency, secret_id:str):

    # Create a dictionary from the Pydantic model
    fraud_data = fraud.model_dump()
    
     # Manually add/modify values in the dictionary
    fraud_data.update({
        "fraud_id": str(uuid.uuid4())
    })

    db_user = models.Fraud(**fraud_data)
    db.add(db_user)
    db.commit()


@router.post("/creditcard/{secret_id}", status_code= status.HTTP_201_CREATED)
@utils.check_secret_password(secret_id="password")
async def create_credit(creditcard: CreditcardBase, db: db_dependency, secret_id:str):

    # Create a dictionary from the Pydantic model
    credit_card_data = creditcard.model_dump()
    
     # Manually add/modify values in the dictionary
    credit_card_data.update({
        "credit_card_id": str(uuid.uuid4())
    })

    db_user = models.Creditcard(**credit_card_data)
    db.add(db_user)
    db.commit()




@router.get("/{secret_id}")
@utils.check_secret_password(secret_id="password")
async def root(request: Request,secret_id: str): #read from the database
    content_html = ""
    for adb in data_sources:
        adb_df = get_adb(adb)

        content_html += "<a href='/db/submit/" + adb + "/password'>" + adb + "</a>" + "<br>\n"
        content_html += adb_df.to_html(index=False, classes="table table-striped", escape=False)
        content_html += "<br>\n"
    return Response(content=content_html, media_type="text/html")

def format_response(df, format_type='html'):
    if format_type == 'html':
        return Response(content=df.to_html(index=False, classes="table table-striped", escape=False), media_type="text/html")
    else:
        return Response(content=df.to_json(orient="records"), media_type="application/json")

@router.post("/transactions/")
#@utils.auth_required(role="all")
async def create_transaction(request: Request):
    df, form_data = await create_adb_entry(request, "transaction")
    df = df[df['credit_card_id'] == form_data["credit_card_id"]] # check for distinct value only
    return format_response(df, format_type="html")

@router.get("/show/transaction/{credit_card_id}/{format_type}")
async def get_transactions(request: Request, credit_card_id: str, format_type:str): #read from the database
    print("^^^accessed get transactions funciton")
    df = get_adb( "transaction")
    if len(df) > 0:
        df = df[df["credit_card_id"] == credit_card_id]
    return format_response(df, format_type)

def get_adb(adb: str):
    csv_file = os.path.join("data", adb + ".csv")
    df = pd.read_csv(csv_file) if os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0 else pd.DataFrame()
    return df

def create_csv_file(adb, form_data, distinct=False, key=None):
    csv_file = os.path.join("data", adb + ".csv")
    existing_df = get_adb(adb)
    print(form_data)
    new_df = pd.DataFrame([form_data], index=[form_data[adb + "_id"]])
    df = pd.concat([existing_df, new_df], ignore_index=True)
    df.to_csv(csv_file, index=False)
    return df

async def create_adb_entry(request, adb):
    form_data = dict(await request.form())
    current_datetime = datetime.now()
    date = str(current_datetime.date())  # Extract the date component
    time = str(current_datetime.time())
    form_data["date"] = date
    form_data["time"] = time
    form_data[adb+ "_id"] = str(uuid.uuid4())
    df = create_csv_file(adb, form_data)
    return df, form_data

@router.post("/{adb}/{secret_id}")
async def insert_adb_entry(request: Request, adb: str):
    df, _ = await create_adb_entry(request, adb)
    return format_response(df)

@router.get("/submit/{adb}/{secret_id}")
@utils.check_secret_password(secret_id="password", exceptions=["transaction"])
async def check_db(request: Request, adb: str, secret_id : str):
    assert adb in data_sources
    return templates.TemplateResponse(adb + ".html.j2", {"request": request})

@router.get("/list/{adb}/{secret_id}/{format_type}")
@utils.check_secret_password(secret_id="password", exceptions=["transaction"])
async def get_adb_data(request: Request, adb:str, secret_id: str, format_type:str): #read from the database
    if not adb in data_sources:
        return adb + " needs to be in " + str(data_sources)
    df = get_adb(adb)
    return format_response(df, format_type)
