from fastapi.routing import APIRouter
from routers.config import engine
from typing import Optional
from fastapi import Query
from routers.config import engine,cursorCommit
import ast,json
from routers.services.mail import sendEmail
from routers.services.sms import sendSMS
import schemas

router=APIRouter(prefix="/sendNotification",tags=['sendNotification'])



@router.post('')
def sendNotification(request:schemas.SendNotification):
    try:
        with engine.connect() as cur:
            if request.type == "P":
                result = cur.execute(f"""SELECT mt.* FROM messageTemplates AS mt WHERE mt.messageHeader='Pass' FOR json path""")
                rows = result.fetchall()
                if rows!=None:
                    tempData = json.loads(rows[0][0])
                    for i in tempData:
                        if i["templateType"] == 'M' and request.emailId !=None:
                            Message_str = i["messageBody"].replace("[Link]", request.link)
                            Data = {"subject": i["subject"], "contact":request.emailId, "mail_content": Message_str}
                            sendEmail(Data)
                        # elif i["templateType"] == 'S' and request.mobileNo !=None:
                        #     sendSMS(
                        #         "smart-parking", request.mobileNo, i["messageBody"].replace("[Link]", request.link), i["peid"], i["tpid"])
                    return {"statusCode": 1, "response": "Email/Sms sended successfully"}
                else:
                    return {"statusCode": 0, "response": "Message Template Not Found"}

            elif request.type == "U":
                result = cur.execute(f"""SELECT mt.* FROM messageTemplates AS mt WHERE mt.messageHeader='UPI payment' FOR json path""")
                rows = result.fetchall()
                if rows!=None:
                    tempData = json.loads(rows[0][0])
                    for i in tempData:
                        if i["templateType"] == 'M' and request.emailId !=None:
                            Message_str = i["messageBody"].replace("[Link]", request.link)
                            Data = {"subject": i["subject"], "contact":request.emailId, "mail_content": Message_str}
                            sendEmail(Data)
                        # elif i["templateType"] == 'S' and request.mobileNo !=None:
                        #     sendSMS(
                        #         "smart-parking", request.mobileNo, i["messageBody"].replace("[Link]", request.link), i["peid"], i["tpid"])
                    return {"statusCode": 1, "response": "Email/Sms sended successfully"}
                else:
                    return {"statusCode": 0, "response": "Message Template Not Found"}
                    
            else:
                return {"statusCode": 0, "response": "please enter valid type"}
            
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode": 0, "response":"Server Error"}