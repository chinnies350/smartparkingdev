from unittest import result
from fastapi.routing import APIRouter
from routers.config import engine
from routers import Response
import ast,json
import schemas
from routers.services.mail import sendEmail
from routers.services.sms import sendSMS
from random import randint

router=APIRouter(prefix='/signupOtp',tags=['signupOtp'])

@router.post('')
def signupOtp(request:schemas.signupOtp):
    try:
        with engine.connect()as cur:
            OTP = randint(1000, 9999)
            result=cur.execute(f"""EXEC [dbo].[signupOtp] ?""",(request.username))            
            rows=result.fetchall()
            result.close()
            if rows[0][0]!=0:
                sample=json.loads(rows[0][2])
                for i in sample:
                    if i["templateType"]=='M' and rows[0][1]!=None:
                        Message_str = i["messageBody"].replace(
                            '[customerName]',str(request.username)).replace('[OTP Number]',str(OTP))
                        Data={"subject":i["subject"],"contact":rows[0][1],"mail_content":Message_str}
                        sendEmail(Data)                 
                    # elif i["templateType"]=='S' and rows[0][1]!=None:
                    #     sendSMS("smart-parking",rows[0][1],i["messageBody"],i["peid"],i["tpid"])
                return {"statusCode": 1, "response": "OTP sent Successfully!",'OTP':OTP}                   
            else:
                return {"statusCode":rows[0][0], "response": rows[0][1]} 
            
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}