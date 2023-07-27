from fastapi.routing import APIRouter
from routers.config import engine
from routers import Response
import schemas
import datetime
from fastapi import Query
from typing import Optional
import json
from joblib import Parallel, delayed

router=APIRouter(prefix='/offerRules',tags=['offerRules'])

def callFunction(i):
    return i.dict()

@router.get('')
def getofferRules(offerRuleId:Optional[int]=Query(None),offerId:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getofferRules]?,?,?""",offerRuleId,offerId,activeStatus)
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
def postofferRules(request:schemas.postofferRulesDetails):
    try:
        with engine.connect() as cur:
            r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.offerRulesDetails)
            offerRulesDetailsJson=json.dumps(r,indent=4, sort_keys=True, default=str)
            result=cur.execute(f"""EXEC [dbo].[postofferRules]
                                     @offerId=?,@offerRulesDetailsJson=?""",
                                    request.offerId,offerRulesDetailsJson)
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.put('')
def putofferRules(request:schemas.putofferRulesDetails):
    try:
        with engine.connect() as cur:
            r = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.offerRulesDetails)
            result=cur.execute(f"""EXEC [dbo].[putofferRules]
                                    @offerRulesDetailsJson=?""",
                                    json.dumps(r,indent=4, sort_keys=True, default=str))
            row=result.fetchall()
            return{"statusCode":int(row[0][1]),"response":row[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.delete('')
def deleteofferRules(activeStatus:str,offerRuleId:int):
    try:
        with engine.connect() as cur:
            result=cur.execute("UPDATE offerRules SET activeStatus=? WHERE offerRuleId=?",activeStatus,offerRuleId)
            result.close()
            if result.rowcount >=1:
                if activeStatus=='D':
                    return Response("deactiveMsg")
                else:
                    return Response("ActiveMsg")
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}