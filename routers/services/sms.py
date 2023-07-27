from routers.config import SMS_API_SAFETY_KEY,SMS_URL
import requests
# from fastapi.routing import APIRouter

# router=APIRouter(prefix='/sms',tags=['sms'])
# @router.post('')
def sendSMS(securitykey, MobileNumber, Message,peid,tpid):
    try:
        assert securitykey == SMS_API_SAFETY_KEY, "Invalid Authorization!"
        querystring = {"userid": "prematix", "password": "matixpre", "sender": "PAYPRE",
                       "peid": peid, "tpid": tpid, "mobileno": MobileNumber, "msg": Message}
        headers = {'cache-control': "no-cache"}
        response = requests.request(
            "GET", SMS_URL, headers=headers, params=querystring)
        assert response.text != None, response.text 
        return {"statusCode": 1, "response": response.text}
    except Exception as e:
        return {"statusCode": 0, "response": str(e)}
    
# data=sendSMS("smart-parking",'6382594417',"Your Paypre verification code is","1201159447435425122","1707161702160449135")
