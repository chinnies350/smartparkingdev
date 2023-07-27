from fastapi.routing import APIRouter
import schemas
from routers.config import engine
import json
from routers import Response
from typing import Optional
from fastapi import Query

router=APIRouter(prefix="/addressMaster",tags=['addressMaster'])

@router.get('')
def getAddressMaster(addressId:Optional[int]=Query(None),userId:Optional[int]=Query(None)):
    try:
      with engine.connect() as cur:
          result=cur.execute(f"""EXEC [dbo].[getAddressMaster] ?,?""",(addressId,userId))
          rows=result.fetchone()
          result.close()
          if rows[0]:
            return {"statusCode": 1, "response":  json.loads(rows[0]) if rows[0] != None else []}
          else:
            return Response("NotFound")
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}

@router.post('')
def postAddressMaster(request:schemas.AddressMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[postAddressMaster]
                                            @userId =?,
                                            @alternatePhoneNumber =?,
                                            @address =?,
                                            @district =?,
                                            @state =?,
                                            @city =?,
                                            @pincode =?,
                                            @createdBy =?""",
                                            (
                                            request.userId,
                                            request.alternatePhoneNumber,
                                            request.address,
                                            request.district,
                                            request.state,
                                            request.city,
                                            request.pincode,
                                            request.createdBy))
            rows=result.fetchall()
            return{"statusCode":int(rows[0][1]),"response":rows[0][0]}
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}


@router.put('')
def putAddressMaster(request:schemas.PutAddressMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[putAddressMaster]
                                            @addressId=?,
                                            @userId =?,
                                            @alternatePhoneNumber =?,
                                            @address =?,
                                            @district =?,
                                            @state =?,
                                            @city =?,
                                            @pincode =?,
                                            @updatedBy =?""",
                                            (
                                            request.addressId,
                                            request.userId,
                                            request.alternatePhoneNumber,
                                            request.address,
                                            request.district,
                                            request.state,
                                            request.city,
                                            request.pincode,
                                            request.updatedBy))
            rows=result.fetchall()
            return{"statusCode":int(rows[0][1]),"response":rows[0][0]}
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}