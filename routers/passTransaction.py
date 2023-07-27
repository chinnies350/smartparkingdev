from fastapi.routing import APIRouter
from routers.config import engine
from routers import Response
import schemas
from datetime import date
from typing import Optional
from fastapi import Query
import ast,json
from joblib import Parallel, delayed
from routers.services.mail import sendEmail
from routers.services.sms import sendSMS

router=APIRouter(prefix='/passTransaction',tags=['passTransaction'])

def callFunction(i):
    return i.dict()

@router.get('')
def getpassTransaction(ParkingPassTransactionId:Optional[int]=Query(None),passId:Optional[int]=Query(None),parkingOwnerId:Optional[int]=Query(None),branchId:Optional[int]=Query(None),taxId:Optional[int]=Query(None),userId:Optional[int]=Query(None),type:Optional[str]=Query(None), phoneNumber:Optional[str]=Query(None), vehicleType:Optional[int]=Query(None),fromDate:Optional[date]=Query(None),toDate:Optional[date]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute("EXEC [dbo].[getpassTransaction]?,?,?,?,?,?,?,?,?,?,?",(ParkingPassTransactionId,passId,parkingOwnerId,branchId,taxId,userId,type, phoneNumber, vehicleType,fromDate,toDate))
            rows= result.fetchone()
            result.close()
            if rows[0]:
                return{"statusCode":1,"response":json.loads(rows[0])if rows[0]!=None else[]}
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.post('')
def postpassTransaction(request:schemas.postpassTransaction):
    try:
        with engine.connect()as cur:
            r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.passTransactionDetails)
            result=cur.execute(f"""EXEC[dbo].[postpassTransaction]
                                    @passTransactionDetailsJson=?""",    
                                    (json.dumps(r,indent=4, sort_keys=True, default=str)))
            row=result.fetchall()
           
            if int(row[0][1])==1:
                userData=json.loads(row[0][2])
                tempData=json.loads(row[0][3])
                for i in tempData:
                    if i["templateType"]=='M' and userData[0]['emailId']!='':
                        Subject_str=i["subject"].replace("[pass type]",userData[0]['passType']).replace("[parking name]",userData[0]['parkingName'])
                        Message_str = i["messageBody"].replace("[user name]",userData[0]['userName']).replace("[pass Type]",userData[0]['passType']).replace("[parking name]",userData[0]['parkingName']).replace("[fromDate]",userData[0]['validStartDate']).replace("[toDate]",userData[0]['validEndDate']).replace("[link]",'prematix.com')
                        Data={"subject":Subject_str,"contact":userData[0]['emailId'],"mail_content":Message_str}
                        sendEmail(Data)     
                    # elif i["templateType"]=='S' and userData[0]['phoneNumber']!='':
                    #     sendSMS("smart-parking",userData[0]['phoneNumber'],i["messageBody"],i["peid"],i["tpid"])
                return {"statusCode": int(row[0][1]), "response": row[0][0],"parkingPassTransId":json.loads(row[0][4])}
            else:
                return {"statusCode": int(row[0][1]), "response": row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}



@router.delete('')
def deletepassTransaction(activestatus:str,ParkingPassTransactionId:int):
    try: 
        with engine.connect() as cur:
            result=cur.execute("UPDATE passTransaction SET activestatus=? WHERE ParkingPassTransactionId=?",activestatus,ParkingPassTransactionId)
            result.close()
            if result.rowcount>=1:
                if activestatus=='D':
                    return Response("deactiveMsg")
                else:
                    return Response("ActiveMsg")
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}
