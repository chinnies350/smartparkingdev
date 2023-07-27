from unittest import result
from fastapi.routing import APIRouter
from routers.config import engine
from routers import Response
import json
import schemas
from routers.services.mail import sendEmail
from routers.services.sms import sendSMS
from random import randint
from routers.fireBaseNotification import send_topic_push

router=APIRouter(prefix='/verifyOTP',tags=['verifyOTP'])

@router.post('')
def verifyOTP(request:schemas.VerifyOTP):
    try:
        OTP = randint(100000, 999999)
        with engine.connect()as cur:
            result=cur.execute(f"""EXEC [dbo].[VerifyOTP] ?""",(request.username))            
            rows=result.fetchall()
            result.close()
            if rows[0][1]!=0:
                sample=json.loads(rows[0][3])
                for i in sample:
                    if i["templateType"]=='M' and rows[0][0]!=None:
                        Message_str = i["messageBody"].replace("[customerName]",rows[0][2] if rows[0][2] else 'user').replace("[OTP Number]",str(OTP))
                        # index = Message_str.find(',')
                        # Message = Message_str[:index] + "" + Message_str[index:] 
                        Data={"subject":i["subject"],"contact":rows[0][0],"mail_content":Message_str}
                        sendEmail(Data)                 
                    if rows[0][4] !=0:
                        result = cur.execute('SELECT registrationToken FROM userMaster WHERE userId = ?', (rows[0][4]))
                        row = result.fetchone()
                        if row[0]:
                            try:
                                res=send_topic_push(row[0],i["subject"], Message_str,rows[0][4] )
                                if res['statusCode']==1:
                                    return {"statusCode": 1, "response": "OTP sent Successfully!",'OTP':OTP}
                            except Exception as e:
                                print("Exception Error",str(e))
                                pass                 
                    # else: 
                    #     if["templateType"]=='S' and rows[0][1]!=None:
                    #         sendSMS("smart-parking",rows[0][1],i["messageBody"].replace("[OTP]",str(OTP)),i["peid"],i["tpid"])
                return {"statusCode": 1, "response": "OTP sent Successfully!",'OTP':OTP}                   
            else:
                return {"statusCode":rows[0][1], "response": str(rows[0][0])}
            
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}