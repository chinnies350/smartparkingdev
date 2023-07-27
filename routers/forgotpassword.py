from fastapi.routing import APIRouter
from routers.config import engine
from routers import Response
import json
import schemas
from routers.services.mail import sendEmail
from routers.services.sms import sendSMS

router=APIRouter(prefix='/forgotpassword',tags=['forgotpassword'])

@router.put('')
def forgotpassword(request:schemas.Forgotpassword):
    try:
        with engine.connect()as cur:
            result=cur.execute(f"""EXEC [dbo].[Passwordrecovery]?,?""",(request.password,request.username))            
            rows=result.fetchall()
            result.close()
            if rows[0][0]!=0:
                sample=json.loads(rows[0][3])
                for i in sample:
                    if i["templateType"]=='M' and rows[0][0]!=None:
                        Message_str = i["messageBody"].replace("[customer name]",str(rows[0][2]))
                        # index = Message_str.find(',')
                        # Message = Message_str[:index] + "" + Message_str[index:] 
                        Data={"subject":i["subject"],"contact":rows[0][0],"mail_content":Message_str}
                        sendEmail(Data)     
                    # elif i["templateType"]=='S' and rows[0][1]!=None:
                    #     sendSMS("smart-parking",rows[0][1],i["messageBody"],i["peid"],i["tpid"])
                return {"statusCode": 1, "response": "Data Updated Successfully!"}              
                                           
            else:
                return Response("NotUpdate")
            
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}