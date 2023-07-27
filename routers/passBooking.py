from fastapi.routing import APIRouter
import schemas
from routers.config import engine
from joblib import Parallel, delayed
from routers import Response
import json
from typing import Optional
from fastapi import Query
from datetime import date
router=APIRouter(prefix="/passBooking",tags=['passBooking'])
def callFunction(i):
    return i.dict()

@router.get('')
def getpassbooking(branchId:Optional[int]=Query(None),parkingOwnerId:Optional[int]=Query(None),passId:Optional[int]=Query(None),type:Optional[str]=Query(None),inOutDetails: Optional[str] = Query(None),number: Optional[int] = Query(None),floorId: Optional[int] = Query(None),fromDate: Optional[date] = Query(None),toDate: Optional[date] = Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute("EXEC [dbo].[getpassbooking] ?,?,?,?,?,?,?,?,?",branchId,parkingOwnerId,passId,type,inOutDetails,number,floorId,fromDate,toDate)
            rows= result.fetchone()
            result.close()
            if rows[0]:
                return{"statusCode":1,"response":json.loads(rows[0])if rows[0]!=None else[]}
            else:
                return Response("NotFound")

    except Exception as e:
        return {"statusCode":0,"response":str(e)}

@router.post('')
def postBookingMaster(request:schemas.PassBokking):
	try:
		with engine.connect() as cur:
			if request.userSlotDetails!=None:
				userSlotDetails = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.userSlotDetails)
				userSlotDetails=json.dumps(userSlotDetails)
			else:
				userSlotDetails=None
			if request.extraFeesDetails!=None:
				extraFeesDetails = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.extraFeesDetails)
				extraFeesDetails=json.dumps(extraFeesDetails)
			else:
				extraFeesDetails=None 
			if request.vehicleHeaderDetails!=None:
				vehicleHeaderDetails = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.vehicleHeaderDetails)
				vehicleHeaderDetails=json.dumps(vehicleHeaderDetails,indent=4, sort_keys=True, default=str)
			else:
				vehicleHeaderDetails=None
			if request.extraFeaturesDetails!=None:
				extraFeaturesDetails = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.extraFeaturesDetails)
				extraFeaturesDetails=json.dumps(extraFeaturesDetails)
			else:
				extraFeaturesDetails=None
			result=cur.execute(f""" EXEC [dbo].[postPassBooking]
									@passTransactionId=?,
									@blockId=?,
									@floorId=?,
									@totalAmount=?,
									@paymentStatus=?,
									@paymentType=?,
									@transactionId=?,
									@bankName=?,
									@bankReferenceNumber=?,
									@createdBy =?,
									@vehicleHeaderJson =?,
									@extraFeaturesJson =?,
									@userSlotJson=?,
									@extraFeesJson=?
									""",
                                    (
									request.passTransactionId,
									request.blockId,
									request.floorId,
									request.totalAmount,
									request.paymentStatus,
									request.paymentType,
									request.transactionId,
									request.bankName,
									request.bankReferenceNumber,
									request.createdBy,
									vehicleHeaderDetails,
                                    extraFeaturesDetails,
									userSlotDetails,
									extraFeesDetails
                                    ))
			rows=result.fetchall()
			return{"statusCode":rows[0][1],"response":rows[0][0],"passBookingTransactionId":rows[0][2]} 
	except Exception as e:
		print("Exception Error",str(e))
		return {"statusCode":0,"response":"Server Error"}