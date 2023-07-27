from unittest import result
from fastapi.routing import APIRouter
from routers.config import engine
from routers import Response
import schemas
from  datetime import date
from typing import Optional
from fastapi import Query
import ast,json
from routers.services.mail import sendEmail
from routers.services.sms import sendSMS
import json

router=APIRouter(prefix='/userOffers',tags=['userOffers'])

@router.get('')
def getuserOffers(userOfferId:Optional[int]=Query(None),offerId:Optional[int]=Query(None),fromDate:Optional[date]=Query(None),toDate:Optional[date]=Query(None),userId:Optional[int]=Query(None),type:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getuserOffers]?,?,?,?,?,?""",userOfferId,offerId,fromDate,toDate,userId,type)
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return{"statusCode":1,"response":json.loads(rows[0])if rows[0]!=None else[]}
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.post('')
def postuserOffers(request:schemas.userOffers):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postuserOffers]
                                    @userId=?,
                                    @offerId=?,
                                    @fromDate=?,
                                    @toDate=?,
                                    @fromTime=?,
                                    @toTime=?,
                                    @activeStatus=?""",
                                    (request.userId,
                                    request.offerId,
                                    request.fromDate,
                                    request.toDate,
                                    request.fromTime,
                                    request.toTime,
                                    request.activeStatus))
            row=result.fetchall()
            if int(row[0][1])==1:
                userData=json.loads(row[0][3])
                parkingName=json.loads(row[0][4])
                sample=json.loads(row[0][5])
                for i in sample:
                    if i["templateType"]=='M' and userData[0]['emailId']!=None:
                        Message_str = i["messageBody"].replace("[name]",userData[0]['userName']).replace("[Parking name]",parkingName[0]['parkingName']).replace("[WELCOME]",str(row[0][2]))
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


# @router.delete('')
# def deleteuserOffers(activeStatus:str):
#     try:
#         with engine.connect() as cur:
#             result=cur.execute("")
#             result.close()
#             if result.rowcount>=1:
#                 if activeStatus=='D':
#                     return Response("deactiveMsg")
#                 else:
#                     return Response("ActiveMsg")
#             else:
#                 return Response("NotFound")

#     except Exception as e:
#         print("Exception Error",str(e))
#         return {"statusCode":0,"response":"Server Error"}


