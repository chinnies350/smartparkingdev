from fastapi.routing import APIRouter
from routers.config import engine
import schemas
from routers import Response
from typing import Optional
from fastapi import Query
import json
from routers.services.mail import sendEmail
from routers.services.sms import sendSMS
import ast

router = APIRouter(prefix='/userMaster',tags=['userMaster'])
routerApproval = APIRouter(prefix='/approvalStatus',tags=['approvalStatus'])
routerToken = APIRouter(prefix='/updateRegistrationToken', tags=['updateRegistrationToken'])

@router.get('')
def getUserMaster(parkingOwnerId:Optional[int]=Query(None),userRole:Optional[str]=Query(None),empDesignation:Optional[int]=Query(None),approvalStatus:Optional[str]=Query(None),branchId:Optional[int]=Query(None),mainContactName:Optional[int]=Query(None),activeStatus:Optional[str]=Query(None),blockId:Optional[int]=Query(None),floorId:Optional[int]=Query(None),userId:Optional[int]=Query(None),phoneNumber:Optional[str]=Query(None),emailId:Optional[str]=Query(None),type:Optional[str]=Query(None),userName:Optional[str]=Query(None)):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""EXEC [dbo].[getUserMaster] ?,?,?,?,?,?,?,?,?,?,?,?,?,?""",parkingOwnerId,userRole,empDesignation,approvalStatus,branchId,mainContactName,activeStatus,blockId,floorId,userId,phoneNumber,emailId,type,userName)
            rows=result.fetchone()
            result.close()
            if rows[0]:
                return {"statusCode": 1,"response":json.loads(rows[0]) if rows[0] != None else []}
            
            else:
                return Response("NotFound")      
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.post('')
def postUserMaster(request: schemas.UserMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""
                                EXEC [dbo].[postUsermaster] 
                                @userName =?,
								@password =?,
								@emailId =?,
								@phoneNumber =?,
								@mainContactName =?,
								@approvalStatus =?,
								@activeStatus =?,
								@walletAmt =?,
								@loyaltyPoints =?,
								@createdBy =?,
								@parkingOwnerId =?,
								@branchId =?,
                                @blockId=?,
                                @floorId=?,
                                @imageUrl =?,
								@DOJ =?,
								@empType =?,
								@userRole =?,
								@empDesignation =?,
								@shiftId =?,
								@alternatePhoneNumber =?,
								@address =?,
								@district =?, 
								@state =?,
								@city =?,
								@pincode =?,
                                @registrationToken = ?
                                """,
                                
                        (   request.userName,
                            request.password,
                            request.emailId,
                            request.phoneNumber,
                            request.mainContactName,
                            request.approvalStatus,
                            request.activeStatus,
                            request.walletAmt,
                            request.loyaltyPoints,
                            request.createdBy,
                            request.parkingOwnerId,
                            request.branchId,
                            request.blockId,
                            request.floorId,
                            request.imageUrl,
                            request.DOJ,
                            request.empType,
                            request.userRole,
                            request.empDesignation,
                            request.shiftId,
                            request.alternatePhoneNumber,
                            request.address,
                            request.district,
                            request.state,
                            request.city,
                            request.pincode,
                            request.registrationToken
                            ))
            row=result.fetchall()
            if int(row[0][1])==1 and row[0][3]=='C':
                userData=json.loads(row[0][6])
                for i in userData:
                    if i["templateType"]=='M' and row[0][4]!=None: 
                        Data={"subject":i["subject"],"contact":row[0][4],"mail_content":i["messageBody"]}
                        sendEmail(Data)     
                    # elif i["templateType"]=='S' and row[0][5]!=None:
                    #     sendSMS("smart-parking",row[0][5],i["messageBody"],i["peid"],i["tpid"])
                
                return {"statusCode": int(row[0][1]), "response": row[0][0],"userId":row[0][2]}
            else:
                return {"statusCode": int(row[0][1]), "response": row[0][0],"userId":row[0][2]}
              
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}

@router.put('')
def putUserMaster(request: schemas.PutUserMaster):
    try:
        with engine.connect() as cur:
            result=cur.execute(f"""
                                EXEC [dbo].[putUsermaster] 
                                @userName =?,
                                @password = ?,
								@emailId =?,
								@phoneNumber =?,
								@walletAmt =?,
								@loyaltyPoints =?,
								@updatedBy =?,
								@userId =?,
								@parkingOwnerId =?,
								@branchId =?,
                                @blockId=?,
                                @floorId=?,
                                @imageUrl =?,
								@DOJ =?,
								@empType =?,
								@empDesignation =?,
								@shiftId =?,
                                @employeeId=?,
								@alternatePhoneNumber =?,
								@address =?,
								@district =?, 
								@state =?,
								@city =?,
								@pincode =?,
                                @addressId=?
                                """,
                        (
                            request.userName,
                            request.password,
                            request.emailId,
                            request.phoneNumber,
                            request.walletAmt,
                            request.loyaltyPoints,
                            request.updatedBy,
                            request.userId,
                            request.parkingOwnerId,
                            request.branchId,
                            request.blockId,
                            request.floorId,
                            request.imageUrl,
                            request.DOJ,
                            request.empType,
                            request.empDesignation,
                            request.shiftId,
                            request.employeeId,
                            request.alternatePhoneNumber,
                            request.address,
                            request.district,
                            request.state,
                            request.city,
                            request.pincode,
                            request.addressId
                            ))
            row=result.fetchall()
            return {"statusCode": int(row[0][1]), "response": row[0][0]}
                              
        
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"} 

@router.delete('')
def deleteuserMaster(userId: int,activeStatus:str):
    try:
       with engine.connect() as cur:
            result=cur.execute("UPDATE UserMaster SET activeStatus=? WHERE userId=?",activeStatus,userId) 
            result.close()
            if result.rowcount >= 1:
               if activeStatus=='D':
                   return Response("deactiveMsg")
               else:
                   return Response("ActiveMsg")
            else:
                return Response("NotFound")

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"} 

@routerApproval.put('')
def putApprovalStatus(userId:Optional[int]=Query(None),branchId:Optional[int]=Query(None),blockId:Optional[int]=Query(None),approvalStatus:Optional[str]=Query(None),cancellationReason:Optional[str]=Query(None)):
    try:
       with engine.connect() as cur:
            
            result=cur.execute("exec [dbo].[approvalMaster] ?,?,?,?,?",(userId,branchId,blockId,approvalStatus,cancellationReason))
            rows=result.fetchall()
            result.close()
            if rows[0][1]==1:
                if rows[0][5]!=None:
                    tempData=json.loads(rows[0][5])
                    for i in tempData:
                        if approvalStatus!='C':
                            if branchId!=None:
                                subject_str=i["subject"].replace("[Name of branch]",rows[0][6]).replace("[Name of parking]",rows[0][7])
                            elif blockId!=None:
                                subject_str=i["subject"].replace("[Name of block]",rows[0][6]).replace("[Name of branch]",rows[0][8])
                            else:
                                subject_str=i["subject"].replace("[Name of parking]",rows[0][6])
                            message_str=i["messageBody"].replace("[customer name]",rows[0][2])
                            response={"statusCode": 1, "response":rows[0][0]}
                        else:
                            if branchId!=None:
                                message_str=i["messageBody"].replace("[customerName]",rows[0][2]).replace("[Name of Branch]",rows[0][6]).replace("[Name of parking]",rows[0][7]).replace("[reason]",cancellationReason)
                                subject_str=i["subject"]
                                response={"statusCode": 0, "response":"Branch Approval is cancelled"}
                            
                            elif blockId!=None:
                                message_str=i["messageBody"].replace("[customerName]",rows[0][2]).replace("[Name of Block]",rows[0][6]).replace("[Name of Branch]",rows[0][8]).replace("[reason]",cancellationReason)
                                subject_str=i["subject"]
                                response={"statusCode": 0, "response":"Block Approval is cancelled"}
                                
                            else:
                                message_str=i["messageBody"].replace("[customerName]",rows[0][2]).replace("[parkingName]",rows[0][6]).replace("[reason]",cancellationReason)
                                subject_str=i["subject"]
                                response={"statusCode": 0, "response":"Owner Approval is cancelled"}
                        if i["templateType"]=='M':
                            Data={"subject":subject_str,"contact":rows[0][3],"mail_content":message_str}
                            sendEmail(Data)
                            
                        # elif i["templateType"]=='S':
                        #     sendSMS("smart-parking",rows[0][4],i["messageBody"],i["peid"],i["tpid"])
                    return {"statusCode": response["statusCode"], "response":response["response"]}
                return {"statusCode": rows[0][1], "response":rows[0][0]}
                    
            else:
                return {"statusCode": rows[0][1], "response":rows[0][0]}

    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"} 


@routerToken.put('')
def updateRegistrationTokenFun(request: schemas.UpdateRegistrationToken):
    try:
        with engine.connect() as cur:
            result = cur.execute('UPDATE userMaster SET registrationToken=? WHERE userId=?', (request.registrationToken, request.userId))
            if result.rowcount > 0:
                return {
                    "response":"Data Updated Successfully",
                    "statusCode":1
                }
            else:
                return {
                    "response":"Data Not Updated",
                    "statusCode":0
                }
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"} 
 



