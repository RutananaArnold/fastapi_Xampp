from fastapi import APIRouter, HTTPException
from sqlalchemy.util.compat import b
from config.db import conn
from models.index import users
from schemas.index import User
from schemas.user import SendMoney
from sqlalchemy import update
import random

user = APIRouter()


@user.get("/fetchall")
async def read_data():
    return conn.execute(users.select()).fetchall()


@user.get("/fetch/userProfile/{id}")
async def get_user_profile(id: int):
    return conn.execute(
        users.select().where(users.c.id == id)).fetchone()


@user.get("/fetch/userBalance/{id}")
async def get_user_balance(id: int):
    senderBalance = conn.execute(
        users.select().where(users.c.id == id)).fetchone()
    print(senderBalance['balance'])
    return {"userBalance": senderBalance['balance']}


@user.post("/register/user")
async def register_user(user: User):
    accNumber = random.randrange(100000,999999)
    actAccNumber = "ABCD"+ str(accNumber)
    print(actAccNumber)
    result = conn.execute(users.insert().values(
        name=user.name,
        email=user.email,
        password=user.password,
        accountNumber=actAccNumber,
    ))
    print(result.lastrowid)
    return {"user_id": result.lastrowid}


@user.put("/topup/{id}")
async def update_data(id: int, newBalance: SendMoney):
    lastBalance = conn.execute(
        users.select().where(users.c.id == id)).fetchone()
    newUserBalance = lastBalance['balance'] + newBalance.balance
    stmt = (
        update(users).
        where(users.c.id == id).
        values(balance=newUserBalance)
    )
    conn.execute(stmt)
    return conn.execute(users.select().where(users.c.id == id)).fetchone()


@user.put("/withdraw/{id}")
async def withdraw_data(id: int, newBalance: SendMoney):
    lastBalance = conn.execute(
        users.select().where(users.c.id == id)).fetchone()
    newUserBalance = lastBalance['balance'] - newBalance.balance
    stmt = (
        update(users).
        where(users.c.id == id).
        values(balance=newUserBalance)
    )
    conn.execute(stmt)
    return conn.execute(users.select().where(users.c.id == id)).fetchone()


@user.put("/send/{id}/{accountNumber}")
async def send_balance(id: int, accountNumber: str, amountToSend: SendMoney):
    print(accountNumber)
    senderBalance = conn.execute(
        users.select().where(users.c.id == id)).fetchone()
    fieldName = conn.execute(
        users.select().where(users.c.accountNumber == accountNumber)).fetchone()
    print(fieldName['name'].strip())
    print("name of sender", amountToSend.accountNumber)
    print("senderBalance", senderBalance['balance'])
    print("amount to send", amountToSend.balance)
    if fieldName['accountNumber'].strip() == amountToSend.accountNumber:
        if senderBalance['balance'] > amountToSend.balance:
            substractedAmount = senderBalance['balance'] - amountToSend.balance
            toppedUpAmount = fieldName['balance'] + amountToSend.balance
            stmtsender = (
                update(users).
                where(users.c.id == id).
                values(balance=substractedAmount)
            )
            stmtreceiver = (
                update(users).
                where(users.c.accountNumber == accountNumber).
                values(balance=toppedUpAmount)
            )
            conn.execute(stmtsender)
            conn.execute(stmtreceiver)
            return {"msg": "Funds sent"}
        else:
            return {"msg": "Not enough funds to send"}
    # else:
    #     raise HTTPException(
    #     status_code=404,
    #     detail=f"user with id: {id} does not exist"
    # )
    #     return


@user.delete("/delete/user/{id}")
async def delete_data(id: int):
    conn.execute(users.delete().where(users.c.id == id))
    return conn.execute(users.select()).fetchall()
