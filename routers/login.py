from fastapi.routing import APIRouter
from routers.config import engine
from routers import Response
import re

router = APIRouter(prefix='/login',tags=['login'])

@router.get('')
def login(user:str,password:str):
    try:
        with engine.connect() as cur:
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
            if Pattern.match(user):
                # print("number called")
                result = cur.execute(f"SELECT userId FROM userMaster WHERE phoneNumber=?",(user))
                row = result.fetchone()
                if row == None:
                    return {
                        'statusCode':0,
                        'response':'check your userName'
                    }
                result=cur.execute(f"""SELECT um.userId,um.userName,um.emailId,um.phoneNumber,um.userRole,(SELECT cm.configName FROM configMaster AS cm WHERE cm.configId=em.empDesignation) AS empDesignationName,em.branchId, ISNULL(em.parkingOwnerId, pom.parkingOwnerId) AS parkingOwnerId,em.floorId
                                        FROM userMaster AS um
                                        LEFT JOIN employeeMaster AS em
                                        ON em.userId=um.userId
                                        LEFT JOIN parkingOwnerMaster AS pom
                                        ON pom.userId = um.userId
                                        WHERE um.phoneNumber=? AND um.password COLLATE Latin1_General_CS_AS =? and um.activeStatus='A'""",(user,password))
                rows = result.fetchall()
            elif re.fullmatch(regex, user):
                # print("email called")
                result = cur.execute(f"SELECT userId FROM userMaster WHERE emailId=?", (user))
                row = result.fetchone()
                if row == None:
                    return {
                        'statusCode':0,
                        'response':'check your userName'
                    }
                result=cur.execute(f"""SELECT um.userId,um.userName,um.emailId,um.phoneNumber,um.userRole,(SELECT cm.configName FROM configMaster AS cm WHERE cm.configId=em.empDesignation) AS empDesignationName, em.branchId, ISNULL(em.parkingOwnerId, pom.parkingOwnerId) AS parkingOwnerId,em.floorId
                                        FROM userMaster AS um
                                        LEFT JOIN employeeMaster AS em
                                        ON em.userId=um.userId
                                        LEFT JOIN parkingOwnerMaster AS pom
                                        ON pom.userId = um.userId
                                        WHERE um.emailId =? AND um.password COLLATE Latin1_General_CS_AS =? and um.activeStatus='A'""",(user,password))
                rows = result.fetchall()
            else:
                # print("else called")
                result = cur.execute(f"SELECT userId FROM userMaster WHERE userName COLLATE Latin1_General_CS_AS=?", (user))
                row = result.fetchone()
                
                if row == None:
                    return {
                        'statusCode':0,
                        'response':'check your userName'
                    }
                result=cur.execute(f"""SELECT um.userId,um.userName,um.emailId,um.phoneNumber,um.userRole,(SELECT cm.configName FROM configMaster AS cm WHERE cm.configId=em.empDesignation) AS empDesignationName, em.branchId, ISNULL(em.parkingOwnerId, pom.parkingOwnerId) AS parkingOwnerId,em.floorId
                                        FROM userMaster AS um
                                        LEFT JOIN employeeMaster AS em
                                        ON em.userId=um.userId
                                        LEFT JOIN parkingOwnerMaster AS pom
                                        ON pom.userId = um.userId
                                        WHERE um.userName COLLATE Latin1_General_CS_AS =? AND um.password COLLATE Latin1_General_CS_AS =? and um.activeStatus='A'""",(user,password))
                rows = result.fetchall()
            
            if len(rows)!=0:
                result.close()
                # print(f'rows {rows}')
                return {"statusCode": 1,"response":[{"userId":rows[0][0],"userName":rows[0][1],"emailId":rows[0][2],"phoneNumber":rows[0][3],"userRole":rows[0][4],"empDesignationName":rows[0][5], 'branchId':rows[0][6], 'parkingOwnerId':rows[0][7],'floorId':rows[0][8]}]}
            else:
                return {
                    'statusCode':0,
                    'response': 'Wrong password. Try again or click ‘Forgot password’ to reset it.'
                }  
    except Exception as e:
        print("Exception Error",str(e))
        return {"statusCode":0,"response":"Server Error"}