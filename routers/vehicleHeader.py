from fastapi.routing import APIRouter
from routers.config import engine
import json
from routers.services.mail import sendEmail
from routers.services.sms import sendSMS
import schemas
from routers.fireBaseNotification import send_topic_push

router=APIRouter(prefix='/vehicleHeader',tags=["vehicleHeader"])


@router.post('')
def postVehicleHeader(request:schemas.PostVehicleHeader):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postVehicleHeader]
                                                @bookingIdType=?,
                                                @bookingPassId =?,
                                                @vehicleNumberType =?,
                                                @vehicleType =?,
                                                @vehicleNumber =?,
                                                @inTime =?,
                                                @vehicleStatus =?,
                                                @createdBy =?                      
                                                """,
                                            (request.bookingIdType,
                                            request.bookingPassId,
                                            request.vehicleNumberType,
                                            request.vehicleType,
                                            request.vehicleNumber,
                                            request.inTime,
                                            request.vehicleStatus,
                                            request.createdBy
                                            )
                                            )
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]} 

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putVehicleHeader(request:schemas.PutVehicleHeader):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putVehicleHeader] ?,?,?,?,?,?,?,?,?,?,?""",(request.inTime,request.outTime,request.vehicleHeaderId,request.updatedBy,request.vehicleStatus, request.slotId,request.paidAmount,request.paymentType,request.transactionId,request.bankName,request.bankReferenceNumber))
            rows=result.fetchall()
            if int(rows[0][1])==1:
                userData=json.loads(rows[0][3])
                tempData=json.loads(rows[0][4])
                for i in tempData:
                    try:
                        if i["templateType"]=='M' and userData[0].get('emailId'):
                            Message_str = i["messageBody"].replace("[customer name]",userData[0]['userName']).replace("[vehicle type parking]",userData[0]['vehicleName']).replace("[date-time]",str(rows[0][2]))
                            Data={"subject":i["subject"].replace("[Name of parking]",userData[0]['parkingName']),"contact":userData[0]['emailId'],"mail_content":Message_str}
                            sendEmail(Data)     
                        if userData[0]['userId'] !=0:
                            result = cur.execute('SELECT registrationToken FROM userMaster WHERE userId = ?', (userData[0]['userId']))
                            row = result.fetchone()
                            if row[0]:
                                try:
                                    res=send_topic_push(row[0],i["subject"], Message_str,userData[0]['userId'] )
                                    return res
                                except Exception as e:
                                    print("Exception Error",str(e))
                                    pass                                 
                        # else:
                        #     if i["templateType"]=='S' and userData[0].get('phoneNumber')!='NULL':
                        #         # sendSMS("smart-parking",userData[0]['phoneNumber'],i["messageBody"],i["peid"],i["tpid"])
                        #         sendSMS("smart-parking",userData[0]['phoneNumber'],i["messageBody"].replace("customer name",str(userData[0]['userName'])).replace("vehicle type parking",str(userData[0]['vehicleNumber'])).replace("date-time",str(rows[0][2])),i["peid"],i["tpid"])
                    except Exception as e:
                        print("Exception Error",str(e))
                        pass
                return {"statusCode": int(rows[0][1]), "response": rows[0][0]}
            else:
                return {"statusCode": int(rows[0][1]), "response": rows[0][0]}
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}