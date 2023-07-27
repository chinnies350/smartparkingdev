from fastapi.routing import APIRouter
import schemas
from routers.config import engine
import json
from routers import Response
from typing import Optional
from fastapi import Query

router=APIRouter(prefix="/addOnService")

@router.get('')
def getAddOnService(branchId:Optional[int]=Query(None),userId:Optional[int]=Query(None),type:Optional[str]=Query(None)):
    try:
      with engine.connect() as cur:
          result=cur.execute(f"""EXEC [dbo].[getAddOnService] ?,?,?""",(userId,branchId,type))
          rows=result.fetchone()
          result.close()
          if rows[0]:
            return {"statusCode": 1, "response":  json.loads(rows[0]) if rows[0] != None else []}
          else:
            return Response("NotFound")
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}