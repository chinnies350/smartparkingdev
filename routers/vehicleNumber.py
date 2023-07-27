from fastapi import APIRouter
import requests
import json
from routers.config import db
import json
from routers.config import engine

router = APIRouter(prefix='/vehicleNumber', tags=['vehicleNumber'])

def ckeckVehicleClassInDB(vehicleClass):
    with engine.connect() as cur:
        result = cur.execute("SELECT vehicleConfigId,vehicleKeyName, vehicleName FROM vehicleConfigMaster WHERE vehicleKeyName IS NOT NULL AND activeStatus='A'")
        row = result.fetchall()
        print('row')
        if row:
            for i in row:
                if vehicleClass in i["vehicleKeyName"].split(','):
                    # print(i)
                    return  i['vehicleConfigId'], i["vehicleName"] 
        return ' ', ' '

@router.get('')
async def vehicleNumber(vehicleNumber:str):
    try:
        val = db['smart_parking']['vehicleNumber'].find_one({'vehicleNumber':vehicleNumber})
        if val:
            # print('val', val)
            vehicleConfigId, vehicleType = ckeckVehicleClassInDB(val["result"]["extraction_output"]["vehicle_class"])
            # print("vehicleConfigId, vehicleType", vehicleConfigId, vehicleType)
            return {
            "response": {
                        "noc_valid_upto": val["result"]["extraction_output"]["noc_valid_upto"],
                        "seating_capacity": val["result"]["extraction_output"]["seating_capacity"],
                        "fitness_upto": val["result"]["extraction_output"]["fitness_upto"],
                        "variant": val["result"]["extraction_output"]["variant"],
                        "registration_number": val["result"]["extraction_output"]["registration_number"],
                        "npermit_upto": val["result"]["extraction_output"]["npermit_upto"],
                        "manufacturer_model": val["result"]["extraction_output"]["manufacturer_model"],
                        "standing_capacity": val["result"]["extraction_output"]["standing_capacity"],
                        "status": val["result"]["extraction_output"]["status"],
                        "status_message": val["result"]["extraction_output"]["status_message"],
                        "number_of_cylinder": val["result"]["extraction_output"]["number_of_cylinder"],
                        "colour": val["result"]["extraction_output"]["colour"],
                        "puc_valid_upto": val["result"]["extraction_output"]["puc_valid_upto"],
                        "vehicle_class": val["result"]["extraction_output"]["vehicle_class"],
                        "vehiclConfigId": vehicleConfigId,
                        "vehicleType": vehicleType,
                        "permanent_address": val["result"]["extraction_output"]["permanent_address"],
                        "permit_no": val["result"]["extraction_output"]["permit_no"],
                        "father_name": val["result"]["extraction_output"]["father_name"],
                        "status_verfy_date": val["result"]["extraction_output"]["status_verfy_date"],
                        "m_y_manufacturing": val["result"]["extraction_output"]["m_y_manufacturing"],
                        "registration_date": val["result"]["extraction_output"]["registration_date"],
                        "gross_vehicle_weight": val["result"]["extraction_output"]["gross_vehicle_weight"],
                        "registered_place": val["result"]["extraction_output"]["registered_place"],
                        "permit_validity_upto": val["result"]["extraction_output"]["permit_validity_upto"],
                        "insurance_policy_no": val["result"]["extraction_output"]["insurance_policy_no"],
                        "noc_details": val["result"]["extraction_output"]["noc_details"],
                        "npermit_issued_by": val["result"]["extraction_output"]["npermit_issued_by"],
                        "sleeper_capacity": val["result"]["extraction_output"]["sleeper_capacity"],
                        "current_address": val["result"]["extraction_output"]["current_address"],
                        "status_verification": val["result"]["extraction_output"]["status_verification"],
                        "permit_type": val["result"]["extraction_output"]["permit_type"],
                        "noc_status": val["result"]["extraction_output"]["noc_status"],
                        "masked_name": val["result"]["extraction_output"]["masked_name"],
                        "fuel_type": val["result"]["extraction_output"]["fuel_type"],
                        "permit_validity_from": val["result"]["extraction_output"]["permit_validity_from"],
                        "owner_name": val["result"]["extraction_output"]["owner_name"],
                        "puc_number": val["result"]["extraction_output"]["puc_number"],
                        "owner_mobile_no": val["result"]["extraction_output"]["owner_mobile_no"],
                        "blacklist_status": val["result"]["extraction_output"]["blacklist_status"],
                        "manufacturer": val["result"]["extraction_output"]["manufacturer"],
                        "permit_issue_date": val["result"]["extraction_output"]["permit_issue_date"],
                        "engine_number": val["result"]["extraction_output"]["engine_number"],
                        "chassis_number": val["result"]["extraction_output"]["chassis_number"],
                        "mv_tax_upto": val["result"]["extraction_output"]["mv_tax_upto"],
                        "body_type": val["result"]["extraction_output"]["body_type"],
                        "unladden_weight": val["result"]["extraction_output"]["unladden_weight"],
                        "insurance_name": val["result"]["extraction_output"]["insurance_name"],
                        "owner_serial_number": val["result"]["extraction_output"]["owner_serial_number"],
                        "vehicle_category": val["result"]["extraction_output"]["vehicle_category"],
                        "noc_issue_date": val["result"]["extraction_output"]["noc_issue_date"],
                        "npermit_no": val["result"]["extraction_output"]["npermit_no"],
                        "cubic_capacity": val["result"]["extraction_output"]["cubic_capacity"],
                        "norms_type": val["result"]["extraction_output"]["norms_type"],
                        "state": val["result"]["extraction_output"]["state"],
                        "insurance_validity": val["result"]["extraction_output"]["insurance_validity"],
                        "financer": val["result"]["extraction_output"]["financer"],
                        "wheelbase": val["result"]["extraction_output"]["wheelbase"]
                    },
            "statusCode":1}
            
    #     url = "https://vehicle-rc-verification-advanced.p.rapidapi.com/v3/tasks/sync/verify_with_source/ind_rc_plus"
        else:
            url = 'https://rc-verification.p.rapidapi.com/v3/tasks/sync/verify_with_source/ind_rc_plus'

            payload = {
                    "task_id": "74f4c926-250c-43ca-9c53-453e87ceacd1",
                    "group_id": "8e16424a-58fc-4ba4-ab20-5bc8e7c3c41e",
                    "data": {"rc_number": vehicleNumber}
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key":"f8e6a6a709mshdbf970d34e3391ap191035jsn0555334ef4e5",
                "X-RapidAPI-Host":"rc-verification.p.rapidapi.com"
            }
            # headers = {
            #         "content-type": "application/json",
            #         "X-RapidAPI-Key": "bfe13b9b0bmsh97307a93add890ep15b82fjsnfcbaac5604b2",
            #         "X-RapidAPI-Host": "vehicle-rc-verification-advanced.p.rapidapi.com"
            # }

            response = json.loads(requests.request("POST", url, json=payload, headers=headers).text)
            response['vehicleNumber'] = vehicleNumber
            db['smart_parking']['vehicleNumber'].insert_one(response)
            vehicleConfigId, vehicleType = ckeckVehicleClassInDB(response["result"]["extraction_output"]["vehicle_class"])
            
            # print('response ',response)

            return {
                "response":{
                        "noc_valid_upto": response["result"]["extraction_output"]["noc_valid_upto"],
                        "seating_capacity": response["result"]["extraction_output"]["seating_capacity"],
                        "fitness_upto": response["result"]["extraction_output"]["fitness_upto"],
                        "variant": response["result"]["extraction_output"]["variant"],
                        "registration_number": response["result"]["extraction_output"]["registration_number"],
                        "npermit_upto": response["result"]["extraction_output"]["npermit_upto"],
                        "manufacturer_model": response["result"]["extraction_output"]["manufacturer_model"],
                        "standing_capacity": response["result"]["extraction_output"]["standing_capacity"],
                        "status": response["result"]["extraction_output"]["status"],
                        "status_message": response["result"]["extraction_output"]["status_message"],
                        "number_of_cylinder": response["result"]["extraction_output"]["number_of_cylinder"],
                        "colour": response["result"]["extraction_output"]["colour"],
                        "puc_valid_upto": response["result"]["extraction_output"]["puc_valid_upto"],
                        "vehicle_class": response["result"]["extraction_output"]["vehicle_class"],
                        "vehiclConfigId": vehicleConfigId,
                        "vehicleType": vehicleType,
                        "permanent_address": response["result"]["extraction_output"]["permanent_address"],
                        "permit_no": response["result"]["extraction_output"]["permit_no"],
                        "father_name": response["result"]["extraction_output"]["father_name"],
                        "status_verfy_date": response["result"]["extraction_output"]["status_verfy_date"],
                        "m_y_manufacturing": response["result"]["extraction_output"]["m_y_manufacturing"],
                        "registration_date": response["result"]["extraction_output"]["registration_date"],
                        "gross_vehicle_weight": response["result"]["extraction_output"]["gross_vehicle_weight"],
                        "registered_place": response["result"]["extraction_output"]["registered_place"],
                        "permit_validity_upto": response["result"]["extraction_output"]["permit_validity_upto"],
                        "insurance_policy_no": response["result"]["extraction_output"]["insurance_policy_no"],
                        "noc_details": response["result"]["extraction_output"]["noc_details"],
                        "npermit_issued_by": response["result"]["extraction_output"]["npermit_issued_by"],
                        "sleeper_capacity": response["result"]["extraction_output"]["sleeper_capacity"],
                        "current_address": response["result"]["extraction_output"]["current_address"],
                        "status_verification": response["result"]["extraction_output"]["status_verification"],
                        "permit_type": response["result"]["extraction_output"]["permit_type"],
                        "noc_status": response["result"]["extraction_output"]["noc_status"],
                        "masked_name": response["result"]["extraction_output"]["masked_name"],
                        "fuel_type": response["result"]["extraction_output"]["fuel_type"],
                        "permit_validity_from": response["result"]["extraction_output"]["permit_validity_from"],
                        "owner_name": response["result"]["extraction_output"]["owner_name"],
                        "puc_number": response["result"]["extraction_output"]["puc_number"],
                        "owner_mobile_no": response["result"]["extraction_output"]["owner_mobile_no"],
                        "blacklist_status": response["result"]["extraction_output"]["blacklist_status"],
                        "manufacturer": response["result"]["extraction_output"]["manufacturer"],
                        "permit_issue_date": response["result"]["extraction_output"]["permit_issue_date"],
                        "engine_number": response["result"]["extraction_output"]["engine_number"],
                        "chassis_number": response["result"]["extraction_output"]["chassis_number"],
                        "mv_tax_upto": response["result"]["extraction_output"]["mv_tax_upto"],
                        "body_type": response["result"]["extraction_output"]["body_type"],
                        "unladden_weight": response["result"]["extraction_output"]["unladden_weight"],
                        "insurance_name": response["result"]["extraction_output"]["insurance_name"],
                        "owner_serial_number": response["result"]["extraction_output"]["owner_serial_number"],
                        "vehicle_category": response["result"]["extraction_output"]["vehicle_category"],
                        "noc_issue_date": response["result"]["extraction_output"]["noc_issue_date"],
                        "npermit_no": response["result"]["extraction_output"]["npermit_no"],
                        "cubic_capacity": response["result"]["extraction_output"]["cubic_capacity"],
                        "norms_type": response["result"]["extraction_output"]["norms_type"],
                        "state": response["result"]["extraction_output"]["state"],
                        "insurance_validity": response["result"]["extraction_output"]["insurance_validity"],
                        "financer": response["result"]["extraction_output"]["financer"],
                        "wheelbase": response["result"]["extraction_output"]["wheelbase"]
                    },
                    "statusCode":1
            }
    except Exception as e:
        print("Exception Error",str(e))
        return {
            "statusCode":0,
            "response":"server error"
        }
