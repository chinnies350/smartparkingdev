from fastapi.routing import APIRouter
import schemas
from routers import Response
from routers.config import engine
from joblib import Parallel, delayed
import json
from typing import Optional
from fastapi import Query
import json
from datetime import datetime
from routers.services.mail import sendEmail
from routers.services.sms import sendSMS
from datetime import datetime,date,time
from routers.fireBaseNotification import send_topic_push

router = APIRouter(prefix="/bookingMaster", tags=['bookingMaster'])
routerPaidAmount = APIRouter(
    prefix="/bookingMasterPaidAmount", tags=['bookingMaster'])
routerDateTimeExtend = APIRouter(
    prefix="/bookingMasterDateTimeExtend", tags=['bookingMaster'])

routerBasedOnSlotId = APIRouter(prefix='/getDataBasedOnSlotId')

getDataBasedOnVehicleNumberPhone = APIRouter(prefix='/getDataBasedOnVehicleNumberPhone')

def callFunction(i):
    return i.dict()


@router.get('')
def getBookingMaster(paymentStatus: Optional[str] = Query(None), paymentType: Optional[int] = Query(None), cancellationStatus: Optional[str] = Query(None), refundStatus: Optional[str] = Query(None), bookingType: Optional[str] = Query(None), bookingDurationType: Optional[str] = Query(None), loginType: Optional[str] = Query(None), createdBy: Optional[int] = Query(None), createdDate: Optional[datetime] = Query(None), booking: Optional[str] = Query(None), userId: Optional[int] = Query(None), floorId: Optional[int] = Query(None), blockId: Optional[int] = Query(None), parkingOwnerId: Optional[int] = Query(None), branchId: Optional[int] = Query(None), bookingId: Optional[int] = Query(None), type: Optional[str] = Query(None), inOutDetails: Optional[str] = Query(None),fromDate:Optional[datetime]=Query(None),toDate:Optional[datetime]=Query(None),fromTime:Optional[time]=Query(None),toTime:Optional[time]=Query(None), subscriptionId: Optional[int]=Query(None), number: Optional[int] = Query(None), slotId:Optional[int] = Query(None) , phoneNumber: Optional[str] = Query(None), category:Optional[int]=Query(None)):
    try:
        with engine.connect() as cur:
            result = cur.execute(f"""EXEC [dbo].[getBooking] ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?""", (paymentStatus, paymentType, cancellationStatus, refundStatus, bookingType,
                                 bookingDurationType, loginType, createdBy, createdDate,booking if booking else None, userId, floorId, blockId, branchId, parkingOwnerId, bookingId, type, inOutDetails,fromTime,toTime,fromDate,toDate, subscriptionId, number, slotId,phoneNumber,category))
            rows = result.fetchone()
            
            result.close()
            if rows[0]:
                return {"statusCode": 1, "response":  json.loads(rows[0]) if rows[0] != None else []}
            else:
                return Response("NotFound")
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":str(e)}


@router.post('')
def postBookingMaster(request: schemas.BookingMaster):
    try:
        with engine.connect() as cur:
            if request.userSlotDetails != None:
                userSlotDetails = Parallel(
                    n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.userSlotDetails)
                userSlotDetails = json.dumps(userSlotDetails)
            else:
                userSlotDetails = None
            if request.extraFees != None:
                extraFeesDetails = Parallel(
                    n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.extraFees)
                extraFeesDetails = json.dumps(extraFeesDetails)
            else:
                extraFeesDetails = None
            if request.vehicleHeaderDetails != None:
                vehicleHeaderDetails = Parallel(
                    n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.vehicleHeaderDetails)
                vehicleHeaderDetails = json.dumps(vehicleHeaderDetails,indent=4, sort_keys=True, default=str)
            else:
                vehicleHeaderDetails = None
            if request.extraFeaturesDetails != None:
                extraFeaturesDetails = Parallel(
                    n_jobs=-1, verbose=True)(delayed(callFunction)(i) for i in request.extraFeaturesDetails)
                extraFeaturesDetails = json.dumps(extraFeaturesDetails)
            else:
                extraFeaturesDetails = None
            result = cur.execute(f""" EXEC [dbo].[postBookingMaster]
                                    @parkingOwnerId =?,
									@branchId =?,
									@blockId =?,
									@floorId =?,
									@userId =?,
                                    @phoneNumber =?,
									@booking =?,
									@loginType =?,
									@bookingDurationType =?,
									@fromTime =?,
									@toTime =?,
									@fromDate =?,
									@toDate =?,
									@accessories =?,
									@bookingType =?,
									@subscriptionId =?,
                                    @taxId=?,
                                    
									@totalAmount=?,
									@paidAmount =?,
									@paymentStatus =?,
									@paymentType =?,
									@offerId =?,
									@transactionId=?,
                                    @bankName=?,
                                    @bankReferenceNumber=?,
                                    @pinNo=?,
									@createdBy =?,
									@vehicleHeaderJson =?,
									@extraFeaturesJson =?,
									@userSlotJson=?,
									@extraFeesJson=?
									""",
                                 (
                                     request.parkingOwnerId,
                                     request.branchId,
                                     request.blockId,
                                     request.floorId,
                                     request.userId,
                                     request.phoneNumber,
                                     request.booking,
                                     request.loginType,
                                     request.bookingDurationType,
                                     request.fromTime,
                                     request.toTime,
                                     request.fromDate,
                                     request.toDate,
                                     request.accessories,
                                     request.bookingType,
                                     request.subscriptionId,
                                     request.taxId,
                                     
                                     request.totalAmount,
                                     request.paidAmount,
                                     request.paymentStatus,
                                     request.paymentType,
                                     request.offerId,
                                     request.transactionId,
                                     request.bankName,
                                     request.bankReferenceNumber,
                                     request.pinNo,
                                     request.createdBy,
                                     vehicleHeaderDetails,
                                     extraFeaturesDetails,
                                     userSlotDetails,
                                     extraFeesDetails
                                 ))
            rows = result.fetchall()
            if len(rows[0]) > 2: 
                if rows[0][2] == 'P':
                    userData = json.loads(rows[0][3])
                    tempData = userData[0]['MessageTemplate']
                    for i in tempData:
                        if i["templateType"] == 'M' and userData[0].get('emailId'):
                            subject_str=i["subject"].replace(
                                "[Name of parking]", userData[0]['branchName'])
                            
                            Message_str = i["messageBody"].replace(
                                "[customerName]", userData[0]['userName']).replace('[bookingId]',str(userData[0]['bookingDetails'][0]["bookingId"])).replace('[indate-time]', str(userData[0]['bookingDetails'][0]["fromDate"]+' '+userData[0]['bookingDetails'][0]["fromTime"])).replace('[outdate-time]', str(userData[0]['bookingDetails'][0]["toDate"]+' '+userData[0]['bookingDetails'][0]["toTime"])).replace('link','https://c.tenor.com/pB4xWrS4KuUAAAAd/onnum-illa.gif')
                        
                            Data = {"subject": subject_str, "contact": userData[0]
                                    ['emailId'], "mail_content": Message_str}
                            sendEmail(Data)
                    result = cur.execute('SELECT registrationToken FROM userMaster WHERE userId = ?', (request.userId))
                    row = result.fetchone()
                    if row[0]:
                        try:
                            res=send_topic_push(row[0],subject_str, Message_str, request.userId)
                            return res
                        except Exception as e:
                            print("Exception Error",str(e))
                            pass
                    # else:
                    #     if i["templateType"] == 'S' and userData[0].get('phoneNumber'):
                    #         sendSMS(
                    #             "smart-parking", userData[0]['phoneNumber'], i["messageBody"].replace('link','https://c.tenor.com/pB4xWrS4KuUAAAAd/onnum-illa.gif'), i["peid"], i["tpid"])
                    return {"statusCode": int(rows[0][1]), "response": rows[0][0],"bookingId":userData[0]['bookingDetails'][0]["bookingId"]}
                elif rows[0][2] == 'N':
                    return {"statusCode": int(rows[0][1]), "response": rows[0][0],"bookingId":rows[0][3]}
                else:
                    return {"statusCode": int(rows[0][1]), "response": rows[0][0]}
            else:
                return {"statusCode": int(rows[0][1]), "response": rows[0][0]}
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":str(e)}


@router.put('')
def putPaymentStatus(request: schemas.PutPaymentStatus):
    try:
        with engine.connect() as cur:
            result = cur.execute(f"""EXEC [dbo].[putPaymentStatus] ?,?,?,?,?""", (request.paymentStatus,
                                 request.bookingId, request.transactionId, request.bankName, request.bankReferenceNumber))
            rows = result.fetchall()
            if int(rows[0][1]) == 1 and rows[0][2] == 'P':
                userData = json.loads(rows[0][3])
                tempData = json.loads(rows[0][4])
                for i in tempData:
                    if i["templateType"] == 'M':
                        Message_str = i["messageBody"].replace("[Name]", userData[0]['userName']).replace(
                            "[Vehicle type parking]", userData[0]['vehicleTypeName']).replace("[parking name]", userData[0]['parkingName'])
                        Data = {"subject": i["subject"].replace(
                            "[Vehicle type parking]", userData[0]['vehicleTypeName']), "contact": userData[0]['emailId'], "mail_content": Message_str}
                        sendEmail(Data)
                    # elif i["templateType"] == 'S':
                    #     sendSMS(
                    #         "smart-parking", userData[0]['phoneNumber'], i["messageBody"], i["peid"], i["tpid"])
                return {"statusCode": int(rows[0][1]), "response": rows[0][0]}
            else:
                return {"statusCode": int(rows[0][1]), "response": rows[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}


@routerDateTimeExtend.put('')
def putBookingDateTimeExtend(request: schemas.PutBookingDateTimeExtend):
    try:
        with engine.connect() as cur:
            result = cur.execute(f"""EXEC [dbo].[putBookingDateTime]
                                                @bookingDurationType =?,
                                                @toTime=?,
                                                @toDate =?,
                                                @taxAmount=?,
                                                @paidAmount=?,
												@totalAmount=?,
                                                @bookingId =?,
                                                @vehicleHeaderId=?,
                                                @updatedBy=?,
                                                @vehicleStatus=?,
                                                @slotId=?,
                                                @paymentType=?,
                                                @transactionId =?,
                                                @bankName =?,
                                                @bankReferenceNumber =?
                                                """,
                                 (
                                     request.bookingDurationType,
                                     request.toTime,
                                     request.toDate,
                                     request.taxAmount,
                                     request.paidAmount,
                                     request.totalAmount,
                                     request.bookingId,
                                     request.vehicleHeaderId,
                                     request.updatedBy,
                                     request.vehicleStatus,
                                     request.slotId,
                                     request.paymentType,
                                     request.transactionId,
                                     request.bankName,
                                     request.bankReferenceNumber


                                 )
                                 )
            rows = result.fetchall()
            if int(rows[0][1]) == 1 and rows[0][2] == 'P':
                userData = json.loads(rows[0][3])
                print('userData',userData)
                tempData = json.loads(rows[0][4])
                print('tempData',tempData)
                for i in tempData:
                    if i["templateType"] == 'M' and userData[0].get('emailId'):
                        Message_str = i["messageBody"].replace("[Name]", userData[0]['userName']).replace(
                            "[Vehicle type parking]", userData[0]['vehicleTypeName']).replace("[parking name]", userData[0]['parkingName'])
                        Data = {"subject": i["subject"].replace(
                            "[Vehicle type parking]", userData[0]['vehicleTypeName']), "contact": userData[0]['emailId'], "mail_content": Message_str}
                        sendEmail(Data)
                    # elif i["templateType"] == 'S' and userData[0].get('phoneNumber'):
                    #     sendSMS(
                    #         "smart-parking", userData[0]['phoneNumber'], i["messageBody"], i["peid"], i["tpid"])
                return {"statusCode": int(rows[0][1]), "response": rows[0][0]}
            else:
                return {"statusCode": int(rows[0][1]), "response": rows[0][0]}
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":"Server Error"}


@routerPaidAmount.put('')
def putBookingPaidAmount(request: schemas.PutBookingPaidAmount):
    try:
        with engine.connect() as cur:
            result = cur.execute(f"""EXEC [dbo].[putBookingPaidAmount]
                                                @paidAmount=?,
                                                @bookingId =?,
                                                @paymentStatus=?,
                                                @transactionId =?,
												@bankName =?,
												@bankReferenceNumber=?,
												@paymentType =?,
												@updatedBy =?
                                                """,
                                 (
                                     request.paidAmount,
                                     request.bookingId,
                                     request.paymentStatus,
                                     request.transactionId,
                                     request.bankName,
                                     request.bankReferenceNumber,
                                     request.paymentType,
                                     request.updatedBy

                                 )
                                 )
            rows = result.fetchall()
            if int(rows[0][1]) == 1 and rows[0][2] == 'P':
                userData = json.loads(rows[0][3])
                tempData = json.loads(rows[0][4])
                for i in tempData:
                    if i["templateType"] == 'M':
                        Message_str = i["messageBody"].replace("[Name]", userData[0]['userName']).replace(
                            "[Vehicle type parking]", userData[0]['vehicleTypeName']).replace("[parking name]", userData[0]['parkingName'])
                        Data = {"subject": i["subject"].replace(
                            "[Vehicle type parking]", userData[0]['vehicleTypeName']), "contact": userData[0]['emailId'], "mail_content": Message_str}
                        sendEmail(Data)
                    # elif i["templateType"] == 'S':
                    #     sendSMS(
                    #         "smart-parking", userData[0]['phoneNumber'], i["messageBody"], i["peid"], i["tpid"])
                return {"statusCode": int(rows[0][1]), "response": rows[0][0]}
            else:
                return {"statusCode": int(rows[0][1]), "response": rows[0][0]}
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":str(e)}


@routerBasedOnSlotId.get('')
async def getDataBasedOnSlotId(slotId:int):
    try:
        with engine.connect() as cur:
            result = cur.execute('EXEC getDetailsBasedOnSlotId @slotId=?', (slotId))
            row = result.fetchone()
            print('row',row)
            if row[0] != None:
                return {
                    'response':json.loads(row[0]),
                    'statusCode':1
                }
            else:
                return {
                    'response':'No Data Found',
                    'statusCode':0
                }
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":str(e)}

@getDataBasedOnVehicleNumberPhone.get('')
async def getDataBasedOnSlotId(inOutDetails:str, floorId:int):
    try:
        with engine.connect() as cur:
            result = cur.execute('EXEC getDataBasedOnVehicleNumberAndPhone @inOutDetails=?, @floorId=?', (inOutDetails, floorId))
            row = result.fetchone()
            print('row',row)
            if row[0] != None:
                return {
                    'response':json.loads(row[0]),
                    'statusCode':1
                }
            else:
                return {
                    'response':'No Data Found',
                    'statusCode':0
                }
    except Exception as e:
        print("Exception Error",str(e))
        return{"statusCode":0,"response":str(e)}
