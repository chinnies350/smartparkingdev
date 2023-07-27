from fastapi.routing import APIRouter
import schemas
from routers import Response
from routers.config import engine
from typing import Optional
from fastapi import Query
from routers.config import engine,cursorCommit
from joblib import Parallel, delayed
import json
from geopy.geocoders import Nominatim

router=APIRouter(prefix="/branchMaster",tags=['branchMaster'])

def callFunction(i):
    return i.dict()

@router.get('')
def getBranchMaster(parkingOwnerId:Optional[int]=Query(None),branchId:Optional[int]=Query(None),approvalStatus:Optional[str]=Query(None),activeStatus:Optional[str]=Query(None),lat:Optional[float]=Query(None),lng:Optional[float]=Query(None),vehicleType:Optional[str]=Query(None),type:Optional[str]=Query(None),district:Optional[str]=Query(None),state:Optional[str]=Query(None),city:Optional[str]=Query(None),pincode:Optional[int]=Query(None),onlineBookingAvailability:Optional[str]=Query(None),configId:Optional[int]=Query(None),configTypeId:Optional[int]=Query(None)):
	try:
		with engine.connect() as cur:
			if type=='S':
				geolocator = Nominatim(user_agent="MyApp")
				location = geolocator.geocode(city)
				lat=location.latitude
				lng=location.longitude
			result=cur.execute(f"""EXEC [dbo].[getBranchMaster] ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?""",(parkingOwnerId,branchId,approvalStatus,activeStatus,lat,lng,vehicleType,type,district,state,city,pincode,onlineBookingAvailability,configId,configTypeId))
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
def postBranchMaster(request:schemas.BranchMaster):
    try:
        with engine.connect() as cur:
            if request.branchImageMasterDetails!=None:
                branchImageMasterJson = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.branchImageMasterDetails)
                branchImageMasterJson=json.dumps(branchImageMasterJson,indent=4, sort_keys=True, default=str)
            else:
                
                branchImageMasterJson=None
            if request.branchWorkingHrsDetails:
                branchWorkingHrsJson= Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.branchWorkingHrsDetails)
                branchWorkingHrsJson=json.dumps(branchWorkingHrsJson,indent=4, sort_keys=True, default=str)
            else:
                branchWorkingHrsJson=None
            result=cur.execute(f""" EXEC [dbo].[postBranchMaster]
                                    @parkingOwnerId =?,
									@branchName =?,
									@shortName=?,
									@latitude =?,
									@longitude =?,
									@address1 =?,
									@address2 =?,
									@district =?,
									@state =?,
									@city =?,
									@pincode =?,
									@phoneNumber =?,
									@alternatePhoneNumber =?,
									@emailId =?,
									@licenseNo =?,
									@licensePeriodFrom =?,
									@licensePeriodTo =?,
									@license =?,
									@document1 =?,
									@document2 =?,
									@multiBook =?,
									@activeStatus =?,
									@approvalStatus =?,
                                    @onlineBookingAvailability=?,
									@isPayBookAvailable=?,
									@isBookCheckInAvailable=?,
									@isPayAtCheckoutAvailable=?,
									@isPayLaterAvaialble=?,
									@advanceBookingHourOrDayType=?,
									@advanceBookingHourOrDay =?,
									@advanceBookingCharges=?,
									@minHour =?,
									@maxHour =?,
									@minDay =?,
									@maxDay =?,
									@createdBy =?,
         							@branchWorkingHrsJson=?,
									@branchImageMasterJson=?""",
                                    (
                                    request.parkingOwnerId,
									request.branchName,
									request.shortName,
									request.latitude,
									request.longitude,
									request.address1,
									request.address2,
									request.district,
									request.state,
									request.city,
									request.pincode,
									request.phoneNumber,
									request.alternatePhoneNumber,
									request.emailId,
									request.licenseNo,
									request.licensePeriodFrom,
									request.licensePeriodTo,
									request.license,
									request.document1,
									request.document2,
									request.multiBook,
									request.activeStatus,
									request.approvalStatus,
                                    request.onlineBookingAvailability,
									request.isPayBookAvailable,
									request.isBookCheckInAvailable,
									request.isPayAtCheckoutAvailable,
									request.isPayLaterAvaialble,
									request.advanceBookingHourOrDayType,
									request.advanceBookingHourOrDay,
									request.advanceBookingCharges,
									request.minHour,
									request.maxHour,
									request.minDay,
									request.maxDay,
									request.createdBy,
									branchWorkingHrsJson,
									branchImageMasterJson
                                    ))
            rows=result.fetchall()
			
            return{"statusCode":rows[0][1],"response":rows[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}


@router.put('')           
def putBranchMaster(request:schemas.PutBranchMaster):
	try:
		with engine.connect() as cur:
			if request.branchWorkingHrs!=None:
				branchWorkingHrsDetails = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.branchWorkingHrs)
				branchWorkingHrsDetails=json.dumps(branchWorkingHrsDetails,indent=4, sort_keys=True, default=str)
			else:
				branchWorkingHrsDetails=None
			if request.branchImageMasterDetails!=None:
				branchImageMasterDetails = Parallel(n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.branchImageMasterDetails)
				branchImageMasterDetails=json.dumps(branchImageMasterDetails,indent=4, sort_keys=True, default=str)
			else:
				branchImageMasterDetails=None
			result=cur.execute(f"""EXEC [dbo].[putBranchMaster]
                                    @branchId=?,
                                    @parkingOwnerId =?,
									@branchName =?,
									@shortName=?,
									@latitude =?,
									@longitude =?,
									@address1 =?,
									@address2 =?,
									@district =?,
									@state =?,
									@city =?,
									@pincode =?,
									@phoneNumber =?,
									@alternatePhoneNumber =?,
									@emailId =?,
									@licenseNo =?,
									@licensePeriodFrom =?,
									@licensePeriodTo =?,
									@license =?,
									@document1 =?,
									@document2 =?,
									@multiBook =?,
									@approvalStatus =?,
									@onlineBookingAvailability=?,
									@isPayBookAvailable=?,
									@isBookCheckInAvailable=?,
									@isPayAtCheckoutAvailable=?,
									@isPayLaterAvaialble=?,
									@advanceBookingHourOrDayType=?,
									@advanceBookingHourOrDay =?,
									@advanceBookingCharges=?,
									@minHour =?,
									@maxHour =?,
									@minDay =?,
									@maxDay =?,
									@updatedBy =?,
									@branchWorkingHrsJson =?,
									@branchImageMasterJson =?""",
                                    (
                                    request.branchId,
                                    request.parkingOwnerId,
									request.branchName,
									request.shortName,
									request.latitude,
									request.longitude,
									request.address1,
									request.address2,
									request.district,
									request.state,
									request.city,
									request.pincode,
									request.phoneNumber,
									request.alternatePhoneNumber,
									request.emailId,
									request.licenseNo,
									request.licensePeriodFrom,
									request.licensePeriodTo,
									request.license,
									request.document1,
									request.document2,
									request.multiBook,
									request.approvalStatus,
									request.onlineBookingAvailability,
									request.isPayBookAvailable,
									request.isBookCheckInAvailable,
									request.isPayAtCheckoutAvailable,
									request.isPayLaterAvaialble,
									request.advanceBookingHourOrDayType,
									request.advanceBookingHourOrDay,
									request.advanceBookingCharges,
									request.minHour,
									request.maxHour,
									request.minDay,
									request.maxDay,
									request.updatedBy,
									branchWorkingHrsDetails,
									branchImageMasterDetails
                                    
                                    ))
			rows=result.fetchall()
			return{"statusCode":rows[0][1],"response":rows[0][0]}
	except Exception as e:
		print("Exception Error",str(e))
		return{"statusCode":0,"response":"Server Error"}

@router.delete('')     
def deleteBranchMaster(branchId:int,activeStatus:str):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""UPDATE branchMaster SET activeStatus=? WHERE branchId=?""",(activeStatus,branchId))
            if result.rowcount>=1:
                if activeStatus=="D":
                    return Response("deactiveMsg")
                else:
                    return Response("ActiveMsg")
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}