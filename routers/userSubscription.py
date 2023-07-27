from fastapi.routing import APIRouter
from routers.config import engine
import schemas
import datetime
from routers import Response
from typing import Optional
from fastapi import Query
import json
from routers.services.mail import sendEmail
from routers.services.sms import sendSMS

router= APIRouter(prefix=('/userSubscription'),tags=['userSubscription'])

@router.get('')
def getUserSubscription(passId:Optional[int]=Query(None),userId:Optional[int]=Query(None),subscriptionId:Optional[int]=Query(None),taxId:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute("EXEC [dbo].[getuserSubscription] ?,?,?,?",passId,userId,subscriptionId,taxId)
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.post('')
def postUsersubscription(request:schemas.userSubscription):
    try:
        with engine.connect()as cur:
            result=cur.execute(f"""EXEC [dbo].[postuserSubscription]
                                    @userId=?,
                                    @subscriptionId=?,
                                    @validityFrom=?,
                                    @validityTo=?,
                                    @actualCount=?,
                                    @remainingCount=?,
                                    @taxId=?,
                                    @amount=?,
                                    @tax=?,
                                    @totalAmount=?,
                                    @passType=?
                                    """,
                                (request.userId,
                                request.subscriptionId,
                                request.validityFrom,
                                request.validityTo,
                                request.actualCount,
                                request.remainingCount,
                                request.taxId,
                                request.amount,
                                request.tax,
                                request.totalAmount,
                                request.passType
                                ))
            row=result.fetchall()
            if int(row[0][1])==1:
                userData=json.loads(row[0][2])
                tempData=json.loads(row[0][3])
                for i in tempData:
                    if i["templateType"]=='M' and userData[0]['emailId']!=None:
                        Message_str = i["messageBody"].replace("[customer name]",userData[0]['userName'])
                        Data={"subject":i["subject"],"contact":userData[0]['emailId'],"mail_content":Message_str}
                        sendEmail(Data)     
                    # elif i["templateType"]=='S' and userData[0]['phoneNumber']!=None:
                    #     sendSMS("smart-parking",userData[0]['phoneNumber'],i["messageBody"],i["peid"],i["tpid"])
                return {"statusCode": int(row[0][1]), "response": row[0][0]}
            else:
                return {"statusCode": int(row[0][1]), "response": row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putUsersubscription(request:schemas.putuserSubscription):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putuserSubscription]
                                    @validityFrom=?,
                                    @validityTo=?,
                                    @actualCount=?,
                                    @remainingCount=?,
                                    @amount=?,
                                    @tax=?,
                                    @totalAmount=?,
                                    @passType=?,
                                    @passId=?,
                                    @userId=?,
                                    @subscriptionId=?,
                                    @taxId=?""",
                                (
                                request.validityFrom,
                                request.validityTo,
                                request.actualCount,
                                request.remainingCount,
                                request.amount,
                                request.tax,
                                request.totalAmount,
                                request.passType,
                                request.passId,
                                request.userId,
                                request.subscriptionId,
                                request.taxId))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.delete('')
def deleteUserSubscription(passId:int):
    try:
        with engine.connect() as cur:
            result=cur.execute("DELETE FROM userSubscription WHERE passId=?",passId)
            result.close()
            if result.rowcount>=1:
                return Response("deleteMsg")
            else:
                return Response("NotDelete")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

