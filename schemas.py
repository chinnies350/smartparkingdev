from pydantic import BaseModel
from datetime import datetime,date,time
from typing import Dict, Optional,List
from fastapi import Query
from xmlrpc.client import boolean
   
class UserMaster(BaseModel):
    parkingOwnerId:Optional[int]=Query(None)
    branchId:Optional[int]=Query(None)
    blockId:Optional[int]=Query(None)
    floorId:Optional[int]=Query(None)
    userName:Optional[str]=Query(None)
    password:Optional[str]=Query(None)
    emailId:Optional[str]=Query(None)
    phoneNumber:Optional[str]=Query(None)
    alternatePhoneNumber:Optional[str]
    mainContactName:Optional[int]=Query(None)
    address : Optional[str]
    city : Optional[str]
    district : Optional[str]
    state : Optional[str]
    pincode : Optional[int]
    imageUrl:Optional[str]
    DOJ:Optional[datetime]
    empType:Optional[int]
    userRole:str
    empDesignation: Optional[int]=Query(None)
    approvalStatus : Optional[str]
    activeStatus : str
    walletAmt:Optional[float]=Query(0)
    loyaltyPoints:Optional[int]=Query(None)
    createdBy : Optional[int]=Query(None)
    shiftId:Optional[int]
    otp: Optional[int]=Query(None)
    registrationToken: Optional[str] = Query(None)

class UpdateRegistrationToken(BaseModel):
    userId:int
    registrationToken:str

class PutUserMaster(BaseModel):
    parkingOwnerId:Optional[int] = Query(None)
    userId:int
    password:Optional[str] = Query(None)
    branchId:Optional[int] = Query(None)
    blockId:Optional[int] = Query(None)
    floorId:Optional[int] = Query(None)
    userName:str
    emailId:Optional[str] = Query(None)
    phoneNumber:Optional[str] = Query(None)
    alternatePhoneNumber:Optional[str] = Query(None)
    address : Optional[str] = Query(None)
    city : Optional[str] = Query(None)
    district : Optional[str] = Query(None)
    state : Optional[str] = Query(None)
    pincode : Optional[int] = Query(None)
    imageUrl:Optional[str] = Query(None)
    DOJ:Optional[datetime] = Query(None)
    empType:Optional[int] = Query(None)
    empDesignation: Optional[int] = Query(None)
    updatedBy : Optional[int] = Query(None)
    walletAmt:Optional[float] = Query(None)
    loyaltyPoints:Optional[int] = Query(None)
    shiftId:Optional[int] = Query(None)
    employeeId:Optional[int] = Query(None)
    addressId:Optional[int] = Query(None)

class ModuleMaster(BaseModel):
    parkingOwnerId:int
    moduleName:str
    imageURL:str
    activeStatus:str
    createdBy:int
    
class PutModuleMaster(BaseModel):
    parkingOwnerId:int
    moduleId:int
    moduleName:str
    imageURL:str
    activeStatus:str
    updatedBy:Optional[int]
    
class MenuOptions(BaseModel):
    parkingOwnerId:Optional[int]
    moduleId:int
    optionName:str
    activeStatus:str
    createdBy:int

class PutMenuOptions(BaseModel):
    parkingOwnerId:int
    moduleId:int
    optionId:int
    optionName:str
    activeStatus:str
    updatedBy:Optional[int]
    
class ModuleAccess(BaseModel):
    parkingOwnerId:int
    userId:int
    moduleId:List[str]
    activeStatus:str
    createdBy:int
    
class PutModuleAccess(BaseModel):
    parkingOwnerId:int
    userId:int
    moduleId:int
    ModuleAccessId:int
    activeStatus:str
    updatedBy:Optional[int]
    
class optionDetail(BaseModel):
    optionId:int
    ViewRights:bool
    AddRights:bool
    EditRights:bool
    DeleteRights:bool
    activeStatus:str
    
class MenuOptionAccess(BaseModel):
    parkingOwnerId:int
    userId:int
    moduleId:int
    optionDetails:Optional[List[optionDetail]] = None
    createdBy:int
    
# class PutMenuOptionAccess(BaseModel):
#     parkingOwnerId:int
#     userId:int
#     moduleId:int
#     MenuOptionAccessId:int
#     optionId:int
#     activeStatus:str
#     updatedBy:Optional[int]
class PutMenuOptionAccess(BaseModel):
    # parkingOwnerId:int
    # userId:int
    # moduleId:int
    MenuOptionAccessId:int
    viewRights:bool
    addRights:bool
    editRights:bool
    deleteRights:bool
    # optionId:int
    activeStatus:str
    updatedBy:Optional[int]

class ListPutMenuOptionAccess(BaseModel):
    menuOptionAccessDetails : List[PutMenuOptionAccess]  


class SubscriptionMaster(BaseModel):
    subscriptionName:str
    validity:int
    offerType:str
    offerValue:float
    parkingLimit:Optional[int]=Query(None)
    rules:str
    taxId:int
    # amount:Optional[float]=Query(None)
    # tax:float
    totalAmount:float
    validityFrom:Optional[datetime]=Query(None)
    validityTo:Optional[datetime]=Query(None)
    activeStatus:str
    createdBy:int
    

class PutSubscriptionMaster(BaseModel):
    subscriptionName:str
    validity: int
    offerType:str
    offerValue:float
    parkingLimit:Optional[int]=Query(None)
    rules:str
    # amount:Optional[float]
    # tax:float
    totalAmount:float
    validityFrom:Optional[datetime]=Query(None)
    validityTo:Optional[datetime]=Query(None)
    activeStatus:str
    updatedBy:int
    subscriptionId:int
    taxId:int

class ConfigMaster(BaseModel):
    # parkingOwnerId :Optional[int]=Query(None)
    configTypeId : int
    configName : str
    activeStatus : str
    createdBy : int
    
class PutConfigMaster(BaseModel):
    # parkingOwnerId :Optional[int]=Query(None)
    configTypeId : int
    configId : int
    configName : str
    activeStatus : str
    updatedBy : Optional[int]

class ConfigType(BaseModel):
    typeName : str
    activeStatus : str
    createdBy : int
    
class PutConfigType(BaseModel):
    configTypeId : int
    typeName : str
    activeStatus : str
    updatedBy : Optional[int]

class TaxMaster(BaseModel):
    serviceName:int
    taxName:str
    taxDescription:Optional[str]
    taxPercentage:Optional[float]
    activeStatus:str
    effectiveFrom:date
    effectiveTill:Optional[date]
    createdBy : int
    
class PutTaxMaster(BaseModel):
    serviceName:int
    taxId:int
    taxName:str
    taxDescription:Optional[str]
    taxPercentage:Optional[float]
    activeStatus:str
    effectiveFrom:date
    # effectiveTill:date
    updatedBy : Optional[int]


class FeedBackMaster(BaseModel):
    parkingOwnerId:int
    branchId:int
    bookingId:int
    feedbackRating:Optional[int]
    feedbackComment:Optional[str]
    createdBy : int

class PutFeedBackMaster(BaseModel):
    FeedbackId:int
    parkingOwnerId:int
    branchId:int
    bookingId:int
    feedbackRating:Optional[int]
    feedbackComment:Optional[str]
    updatedBy : int


class vehicleMaster(BaseModel):
    userId:int
    vehicleName:Optional[str]=Query(None)
    vehicleNumber:str
    vehicleType:int
    insuranceValidity:Optional[date]=Query(None)
    vehicleImageUrl:Optional[str]=Query(None)
    documentImageUrl:Optional[str]=Query(None)
    isEV:Optional[boolean]=Query(None)
    chargePinType:Optional[int]=Query(None)


class PutvehicleMaster(BaseModel):
    vehicleId:int
    userId:int
    vehicleName:Optional[str]
    vehicleNumber:str
    vehicleType:int    
    insuranceValidity:Optional[date]
    vehicleImageUrl:Optional[str]
    documentImageUrl:Optional[str]
    isEV:Optional[boolean]
    chargePinType:Optional[int]
   

class userSubscription(BaseModel):
    userId:int
    subscriptionId:int
    validityFrom:date
    validityTo:date
    actualCount:Optional[int]=Query(None)
    remainingCount:Optional[int]=Query(None)
    taxId:int
    amount:Optional[float]=Query(None)
    tax:float
    totalAmount:float
    passType:Optional[str]=Query(None)

class putuserSubscription(BaseModel):
    passId:int
    userId:int
    subscriptionId:int
    validityFrom:date
    validityTo:date
    actualCount:Optional[int]=Query(None)
    remainingCount:Optional[int]=Query(None)
    taxId:int
    amount:Optional[float]=Query(None)
    tax:float
    totalAmount:float
    passType:Optional[str]=Query(None)


class ParkingOwnerMaster(BaseModel):
      parkingName:str
      shortName:str
      founderName:str
      logoUrl:Optional[str]=Query(None)
      websiteUrl:Optional[str]=Query(None)
      gstNumber:Optional[str]=Query(None)
      placeType:Optional[str]=Query(None)
      activeStatus:str
      createdBy:int

class PutParkingOwnerMaster(BaseModel):
      parkingOwnerId:int
      userId:int
      parkingName:str
      shortName:str
      founderName:str
      logoUrl:str
      websiteUrl:str
      gstNumber:str
      placeType:str
      updatedBy:int


class BlockMaster(BaseModel):
    parkingOwnerId:int
    branchId:int
    blockName:str
    # latitude:float
    # longtitude:float
    activeStatus:str
    approvalStatus:str
    createdBy:int


class PutBlockMaster(BaseModel):
    blockId:int
    parkingOwnerId:int
    branchId:int
    blockName:str
    # latitude:float
    # longtitude:float
    approvalStatus:str
    updatedBy:int
   
class BranchWorkingHrsDetails(BaseModel):
    workingDay:Optional[str]
    fromTime:time
    toTime:time
    isHoliday:Optional[boolean]

class BranchImageMasterDetails(BaseModel):
    imageUrl:str
    
class BranchMaster(BaseModel):
    parkingOwnerId:int
    branchName:str
    shortName:str
    latitude:float
    longitude:float
    address1:Optional[str]=Query(None)
    address2:Optional[str]=Query(None)
    district:Optional[str]=Query(None)
    state:Optional[str]=Query(None)
    city:Optional[str]=Query(None)
    pincode:int
    phoneNumber:str
    alternatePhoneNumber:Optional[str]=Query(None)
    emailId:Optional[str]=Query(None)
    licenseNo:str
    licensePeriodFrom:date
    licensePeriodTo:date
    license:str
    document1:Optional[str]=Query(None)
    document2:Optional[str]=Query(None)
    multiBook:str
    activeStatus:str
    approvalStatus:str
    onlineBookingAvailability:str
    isPayBookAvailable:str
    isBookCheckInAvailable:str
    isPayAtCheckoutAvailable:str
    isPayLaterAvaialble:str
    advanceBookingHourOrDayType : Optional[str]=Query(None)
    advanceBookingHourOrDay :Optional[int]=Query(None)
    advanceBookingCharges :Optional[float]=Query(None)
    minHour :Optional[int]=Query(None)
    maxHour :Optional[int]=Query(None)
    minDay :Optional[int]=Query(None)
    maxDay :Optional[int]=Query(None)
    createdBy:int
    branchWorkingHrsDetails:Optional[List[BranchWorkingHrsDetails]] = None
    branchImageMasterDetails:Optional[List[BranchImageMasterDetails]] = None

class PutBranchWorkingHrs(BaseModel):
    uniqueId:int
    branchId:int
    parkingOwnerId:int
    workingDay:str
    fromTime:time
    toTime:time
    isHoliday:boolean
    updatedBy:int

class BranchWorkingHrsDetail(BaseModel):
    uniqueId:int
    workingDay:str
    fromTime:time
    toTime:time
    isHoliday:boolean
class PutBranchImageMaster(BaseModel):
    imageId:int
    imageUrl:str

class PutBranchMaster(BaseModel):
    branchId:int
    parkingOwnerId:int
    branchName:str
    shortName:str
    latitude:float
    longitude:float
    address1:str
    address2:str
    district:str
    state:str
    city:str
    pincode:int
    phoneNumber:str
    alternatePhoneNumber:str
    emailId:str
    licenseNo:str
    licensePeriodFrom:date
    licensePeriodTo:date
    license:str
    document1:str
    document2:str
    multiBook:str
    approvalStatus:str
    onlineBookingAvailability:str
    isPayBookAvailable:str
    isBookCheckInAvailable:str
    isPayAtCheckoutAvailable:str
    isPayLaterAvaialble:str
    advanceBookingHourOrDayType :str
    advanceBookingHourOrDay :int
    advanceBookingCharges :float
    minHour :int
    maxHour :int
    minDay :int
    maxDay :int
    updatedBy:int
    branchWorkingHrs:Optional[List[BranchWorkingHrsDetail]]=Query(None)
    branchImageMasterDetails:Optional[List[PutBranchImageMaster]]=Query(None)


class AddressMaster(BaseModel):
    userId:int
    alternatePhoneNumber:Optional[str]
    address:Optional[str]
    district:Optional[str]
    state:Optional[str]
    city:Optional[str]
    pincode:int
    createdBy:int


class PutAddressMaster(BaseModel):
    addressId:int
    userId:int
    alternatePhoneNumber:Optional[str]
    address:str
    district:str
    state:str
    city:str
    pincode:int
    updatedBy:int


class BranchWorkingHrs(BaseModel):
    branchId:int
    parkingOwnerId:int
    workingDay:str
    fromTime:time
    toTime:time
    isHoliday:boolean
    createdBy:int



class FloorVehicleMasterDetails(BaseModel):
    vehicleType:int
    capacity:int
    length:int
    height:int
    rules:str
    activeStatus:str
    
class FloorImageMasterDetails(BaseModel):
    imageUrl:str
    activeStatus:str
    
class FloorFeaturesDetails(BaseModel):
    parkingOwnerId:int
    branchId:int
    featureName:str
    description:str
    # amount:float
    taxId:int
    # tax:float
    totalAmount:float
    
class FloorMaster(BaseModel):
    parkingOwnerId:int
    branchId:int
    blockId:int
    floorName:int
    floorType:int
    squareFeet:int
    activeStatus:str
    createdBy: int
    floorVehicleMasterDetails:Optional[List[FloorVehicleMasterDetails]] = None
    floorFeaturesDetails:Optional[List[FloorFeaturesDetails]] = None

class PutFloorMaster(BaseModel):
    floorId:int
    floorName:int
    floorType:int
    squareFeet:int
    activeStatus:str
    updatedBy: int

class PriceMaster(BaseModel):
    parkingOwnerId:int
    branchId:int
    floorId:int
    totalAmount:float
    idType:str
    vehicle_accessories:int
    timeType:Optional[str] = Query(None)
    taxId:int
    userMode:str
    graceTime:Optional[int] = Query(None)
    activeStatus:str
    remarks:Optional[str]=Query(None)
    createdBy:int

class PriceMasterDetails(BaseModel):
    totalAmount:float
    timeType:Optional[str] = Query(None)
    taxId:int
    userMode:Optional[str]= Query(None)
    activeStatus:str
    remarks:Optional[str]=Query(None)

class PriceMaster1(BaseModel):
    parkingOwnerId:int
    branchId:int
    floorId:int
    idType:str
    vehicle_accessories:int
    graceTime:Optional[int] = Query(None)
    createdBy:int
    priceDetails : List[PriceMasterDetails] = Query(None)

class PriceMasterDetailsPut(BaseModel):
    priceId:int
    totalAmount:float
    timeType:Optional[str] = Query(None)
    taxId:int
    userMode:Optional[str]= Query(None)
    activeStatus:str
    remarks:Optional[str]=Query(None)

class PutPriceMaster1(BaseModel):
    parkingOwnerId:int
    branchId:int
    floorId:int
    idType:str
    vehicle_accessories:int
    graceTime:Optional[int] = Query(None)
    updatedBy:int
    priceDetails : List[PriceMasterDetailsPut] = Query(None)


    
     
class PutPriceMaster(BaseModel):
    totalAmount:str
    idType:str
    taxId:int
    userMode:str
    graceTime:int
    updatedBy:int
    priceId:int

class TimeSlabRules(BaseModel):
    priceId:int
    fromDate:datetime
    toDate:datetime
    activeStatus:str
    createdBy:int

class shiftMaster(BaseModel):
    parkingOwnerId:int
    branchId:int
    shiftName:int
    startTime:time
    endTime:time
    breakStartTime:Optional[time]=Query(None)
    breakEndTime:Optional[time]=Query(None)
    gracePeriod:Optional[int]=Query(None)
    activeStatus:str
    createdBy:int

class putshiftMaster(BaseModel):
    shiftId:int
    parkingOwnerId:int
    branchId:int
    shiftName:int
    startTime:time
    endTime:time
    breakStartTime:Optional[time]=Query(None)
    breakEndTime:Optional[time]=Query(None)
    gracePeriod:Optional[int]=Query(None)
    activeStatus:str
    updatedBy:int

class ParkingSlotDetails(BaseModel):
    laneNumber:Optional[str]=Query(None)
    slotNumber:str
    rowId:str
    columnId:str
    isChargeUnitAvailable:boolean
    chargePinType:int
    activeStatus:int
    createdBy:int

class parkingSlot(BaseModel):
    branchId:int
    blockId:int
    floorId:int
    parkingOwnerId:int
    typeOfVehicle:int
    noOfRows:int
    noOfColumns:int
    passageLeftAvailable:Optional[boolean]=Query(None)
    passageRightAvailable:Optional[boolean]=Query(None)
    typeOfParking:int
    activeStatus:str
    createdBy:int
    ParkingSlotDetails:List[ParkingSlotDetails]

class postparkingDetailsSlot(BaseModel):
    parkingLotlineDetails:List[parkingSlot]

class putparkingSlotDetails(BaseModel):
    laneNumber:str
    parkingSlotId :int
    parkingLotLineId:int
    slotNumber:str
    rowId:str
    columnId:str
    isChargeUnitAvailable:boolean
    chargePinType:int
    activeStatus:int
    updatedBy:int

class putparkingSlot(BaseModel):
    parkingLotLineId:int
    branchId:int
    blockId:int
    floorId:int
    parkingOwnerId:int
    typeOfVehicle:int
    noOfRows:int
    noOfColumns:int
    passageLeftAvailable:Optional[boolean]=Query(None)
    passageRightAvailable:Optional[boolean]=Query(None)
    typeOfParking:int
  
    activeStatus:str
    updatedBy:int
    ParkingSlotDetailsupdate:List[putparkingSlotDetails]

class TimeSlabRules(BaseModel):
    priceId:int
    fromDate:datetime
    toDate:datetime
    activeStatus:str
    createdBy:int

class postparkingSlot(BaseModel):
    ParkingSlotDetail:List[ParkingSlotDetails]

class singleputparkingSlot(BaseModel):
    UpdateparkingSlotDetail:List[putparkingSlotDetails]

class PutfloorImageMaster(BaseModel):
    floorImageMasterDetails:Optional[List[FloorImageMasterDetails]] = None
    floorId:int
    updatedBy:int

class PutfloorFeaures(BaseModel):
    featuresId:int
    featureName:str
    description:str
    taxId:int
    totalAmount:float
    floorId:int
    updatedBy:int
    
class PutfloorVehicleMaster(BaseModel):
    floorId:int
    updatedBy:int
    floorVehicleId:int
    vehicleType:int
    capacity:int
    length:int
    height:int
    rules:str

class VehicleHeader(BaseModel):
    # vehicleNumberType:int
    slotId:Optional[int]=Query(None)
    vehicleType:int
    vehicleNumber:str
    inTime:Optional[datetime]=Query(None)
    outTime:Optional[datetime]=Query(None)
    vehicleStatus:Optional[str]=Query(None)

class ExtraFeatures(BaseModel):
    floorFeaturesId:int
    count:int
    extraDetail:str

class UserSlot(BaseModel):
    slotId:int
    vehicleType:int

class ExtraFees(BaseModel):
    priceId:Optional[int]=Query(None)
    count:int
    extraFee:float
    extraFeesDetails:Optional[str]=Query(None)

class BookingMaster(BaseModel):
    parkingOwnerId: int
    branchId:int
    blockId:int
    floorId:int
    userId:Optional[int]=Query(None)
    phoneNumber:str
    booking:str
    loginType:str
    bookingDurationType:Optional[str]=Query(None)
    fromTime:Optional[time]=Query(None)
    toTime:Optional[time]=Query(None)
    fromDate:Optional[date]=Query(None)
    toDate:Optional[date]=Query(None)
    Dates:Optional[str]=Query(None)
    accessories:str
    bookingType:str
    subscriptionId:Optional[int]=Query(None)
    taxId:Optional[int]=Query(None)
    totalAmount:Optional[float]=Query(None)
    paidAmount:Optional[float]=Query(None)
    paymentStatus:str
    paymentType:Optional[int]=Query(None)
    offerId:Optional[int]=Query(None)
    transactionId:Optional[str]=Query(None)
    bankName:Optional[str]=Query(None)
    bankReferenceNumber:Optional[str]=Query(None)
    pinNo:str
    createdBy:int
    vehicleHeaderDetails:Optional[List[VehicleHeader]]=Query(None)
    extraFeaturesDetails:Optional[List[ExtraFeatures]]=Query(None)
    userSlotDetails:Optional[List[UserSlot]]=Query(None)
    extraFees:Optional[List[ExtraFees]]=Query(None)

class PassVehicleHeader(BaseModel):
    slotId:Optional[int]=Query(None)
    vehicleType:int
    vehicleNumber:str
    inTime:Optional[datetime]=Query(None)
    outTime:Optional[datetime]=Query(None)
    vehicleStatus:Optional[str]=Query(None)
class PassExtraFeatures(BaseModel):
    
    count:int
    floorFeaturesId:int
    extraDetail:str

class PassUserSlot(BaseModel):
    
    slotId:int
    vehicleType:int
class PassExtraFees(BaseModel):
    
    priceId:Optional[int]=Query(None)
    count:int
    extraFee:float
    extraFeesDetails:Optional[str]=Query(None)

class PassBokking(BaseModel):
    passTransactionId:int
    blockId:int
    floorId:int
    totalAmount:Optional[str]=Query(None)
    paymentStatus:Optional[str]=Query(None)
    paymentType:Optional[int]=Query(None)
    transactionId:Optional[str]=Query(None)
    bankName:Optional[str]=Query(None)
    bankReferenceNumber:Optional[str]=Query(None)
    createdBy:int
    vehicleHeaderDetails:List[PassVehicleHeader]
    extraFeaturesDetails:Optional[List[PassExtraFeatures]]=Query(None)
    userSlotDetails:Optional[List[PassUserSlot]]=Query(None)
    extraFeesDetails:Optional[List[PassExtraFees]]=Query(None)

class PostfloorVehicleMaster(BaseModel):
    floorId:Optional[int]=Query(None)
    vehicleType:int
    capacity:int
    length:int
    height:int
    rules:str
    activeStatus:str
    createdBy:int
    # branchId:int


class PostExtraFees(BaseModel):
    bookingPassId :int
    bookingIdType:str
    priceId:Optional[int]=Query(None)
    count:int
    extraFee: float
    extraFeesDetails: Optional[str]=Query(None)
    createdBy: int

class PostfloorFeatures(BaseModel):
    parkingOwnerId:int
    branchId:int
    floorId:Optional[int]=Query(None)
    featureName:str
    description:str
    taxId:int
    totalAmount:float
    createdBy:int

class PostExtraFeatures(BaseModel):
    bookingPassId: int
    bookingIdType: str
    floorFeaturesId :int
    count:int
    extraDetail:Optional[str]=Query(None)


class parkingPassConfig(BaseModel):
    parkingOwnerId:int
    branchId:int
    passCategory:str
    passType:str
    noOfDays:int
    parkingLimit:Optional[int]=Query(None)
    totalAmount: float
    taxId:int
    vehicleType:int
    remarks:Optional[str]=Query(None)
    activeStatus:str
    createdBy:int


class putparkingPassConfig(BaseModel):
    
    parkingPassConfigId:int
    parkingOwnerId:int
    branchId:int
    passCategory:str
    passType:str
    noOfDays:int
    parkingLimit:int
    totalAmount:float
    taxId:int
    vehicleType:int
    remarks:str
    activeStatus:str
    updatedBy:int


class Faq(BaseModel):
    offerId:Optional[int]=Query(None)
    question:str
    answer:str
    questionType:str
    activeStatus:str
    createdBy:int

class PutFaq(BaseModel):
    faqId:int
    offerId:Optional[int]=Query(None)
    question:str
    answer:str
    questionType:str
    updatedBy:int

class CancellationRules(BaseModel):
    type:str
    duration:int
    noOfTimesPerUser:int
    cancellationCharges:float
    activeStatus:str
    createdBy:int

class PutCancellationRules(BaseModel):
    type:str
    duration:int
    noOfTimesPerUser:int
    cancellationCharges:float
    updatedBy:int
    uniqueId:int

class AppSettings(BaseModel):
    privacyPolicy:str
    termsAndConditions:str
    appVersion:float
    appType:str
    activeStatus:str
    createdBy:int

class PutAppSettings(BaseModel):
    privacyPolicy:str
    termsAndConditions:str
    appVersion:float
    appType:str
    updatedBy:int
    uniqueId:int

class PrintingInstructionsConfig(BaseModel):
    parkingOwnerId:Optional[int]=Query(None)
    branchId:Optional[int]=Query(None)
    instructionType:str
    instructions:str
    createdBy:int

class PutPrintingInstructionsConfig(BaseModel):
    parkingOwnerId:Optional[int]=Query(None)
    branchId:Optional[int]=Query(None)
    instructionType:str
    instructions:str
    updatedBy:int
    uniqueId:int

class instructionsDetails(BaseModel):
    instructions:str

class PrintingInstructionsConfig1(BaseModel):
    parkingOwnerId:int
    branchId:int
    instructionType:str
    instructionsDetails:List[instructionsDetails]
    createdBy:int

class UserWallet(BaseModel):
    userId:int
    walletAmt:Optional[float]=Query(None)
    loyaltyPoints:Optional[int]=Query(None)
    status:str
    expiryDate:Optional[datetime] = Query(None)
    creditedDate:datetime
    reasonToCredit:str

# class PutUserWallet(BaseModel):
#     userId:int
#     walletAmt:float
#     loyaltyPoints:int
#     # status:str
#     expiryDate:datetime
#     creditedDate:datetime
#     reasonToCredit:str
#     uniqueId:int

class passTransaction(BaseModel):
    passId:int
    parkingOwnerId:int
    branchId:int
    userId:Optional[int]=Query(None)
    phoneNumber:Optional[str]=Query(None)
    vehicleType:int
    totalAmount:float
    taxId:int
    paymentStatus:str
    paymentType:int
    walletCash:Optional[float]=Query(None)
    cancellationStatus:Optional[str]=Query(None)
    refundStatus:Optional[str]=Query(None)
    cancellationCharges:Optional[float]=Query(None)
    refundAmt:Optional[float]=Query(None)
    cancellationReason:Optional[str]=Query(None)
    transactionId:Optional[str]=Query(None)
    bankName:Optional[str]=Query(None)
    bankReferenceNumber:Optional[str]=Query(None)
    # parkingLimit:str
    offerId:Optional[int]=Query(None)
    offerAmount:Optional[float]=Query(None)
    activeStatus:str
    createdBy:int

class postpassTransaction(BaseModel):
    passTransactionDetails:List[passTransaction]


class PostMessageTemplates(BaseModel):
    messageHeader:str
    subject:str
    messageBody:str
    templateType:str
    peid:Optional[str]=Query(None)
    tpid:Optional[str]=Query(None)
    createdBy:int
    
class PutMessageTemplates(BaseModel):
    uniqueId:int
    messageHeader:str
    subject:str
    messageBody:str
    templateType:str
    peid:str
    tpid:str
    updatedBy:int

class PostAdmin(BaseModel):
    userName:str
    password:str
    emailId:Optional[str]=Query(None)
    phoneNumber:Optional[str]=Query(None)
    imageUrl:Optional[str]=Query(None)
    activeStatus : str
    createdBy:Optional[int]=Query(None)
    parkingName:str
    shortName:str
    founderName:str
    logoUrl:Optional[str]=Query(None)
    websiteUrl:Optional[str]=Query(None)
    gstNumber:Optional[str]=Query(None)
    placeType:Optional[str]=Query(None)

class offerrules(BaseModel):
    offerRule:str
    ruleType:int
    activeStatus:str

class offerMaster(BaseModel):
    offerTypePeriod:str
    offerHeading:str
    offerDescription:str
    offerCode:str
    offerImageUrl:str
    fromDate:date
    toDate:date
    fromTime:time
    toTime:time
    offerType:str
    offerValue:float
    minAmt:float
    maxAmt:float
    noOfTimesPerUser:int
    activeStatus:str
    createdBy:int
    offerRulesDetails:Optional[List[offerrules]] = Query(None)

class Putofferrules(BaseModel):
    offerRuleId:Optional[int] = Query(None)
    offerId:int
    offerRule:str
    ruleType:int
    activeStatus:str

class putofferMaster(BaseModel):
    offerId:int
    offerTypePeriod:str
    offerHeading:str
    offerDescription:str
    offerCode:str
    offerImageUrl:str
    fromDate:date
    toDate:date
    fromTime:time
    toTime:time
    offerType:str
    offerValue:float
    minAmt:float
    maxAmt:float
    noOfTimesPerUser:int
    activeStatus:str
    updatedBy:int
    offerRulesDetails:Optional[List[Putofferrules]]=Query(None)

class postofferRulesDetails(BaseModel):
    offerId:int
    offerRulesDetails:List[offerrules]

class putofferRulesDetails(BaseModel):
    offerRulesDetails:List[Putofferrules]

class offerMapping(BaseModel):
    parkingOwnerId:int
    branchId:int
    offerId:int
    activeStatus:str
    createdBy:int

class userOffers(BaseModel):
    userId:int
    offerId:int
    fromDate:date
    toDate:date
    fromTime:time
    toTime:time
    activeStatus:str


class PostVehicleHeader(BaseModel):
    bookingIdType:str
    bookingPassId:int
    vehicleNumberType:int
    vehicleType:int
    vehicleNumber:str
    inTime:datetime
    vehicleStatus:str
    createdBy:int
class PutVehicleHeader(BaseModel):
    vehicleHeaderId:int
    inTime:Optional[datetime]=Query(None)
    outTime:Optional[datetime]=Query(None)
    slotId: Optional[int]=Query(None)
    updatedBy:int
    vehicleStatus:Optional[str]=Query(None)
    paidAmount:Optional[float]=Query(None)
    paymentType:Optional[int]=Query(None)
    transactionId :Optional[str]=Query(None)
    bankName :Optional[str]=Query(None)
    bankReferenceNumber:Optional[str]=Query(None)

class cancellationupdate(BaseModel):
    bookingId:int
    refundStatus:str
    cancellationCharges:float
    cancellationReason:str
    updatedBy:int

class VehicleConfigMaster(BaseModel):
    vehicleName:str
    vehicleImageUrl:str
    vehiclePlaceHolderImageUrl: str
    vehicleKeyName:Optional[str]=Query(None)
    activeStatus:str
    createdBy:int

class PutVehicleConfigMaster(BaseModel):
    vehicleConfigId:int
    vehicleName:str
    vehicleImageUrl:str
    vehiclePlaceHolderImageUrl: str
    vehicleKeyName:str
    updatedBy:int

class PutPaymentStatus(BaseModel):
    paymentStatus:str
    bookingId:int
    transactionId:str
    bankName:str
    bankReferenceNumber:str

class PutBookingDateTimeExtend(BaseModel):
    bookingDurationType:str
    toTime:Optional[time]=Query(None)
    toDate:Optional[date]=Query(None)
    taxAmount:Optional[float]=Query(0)
    paidAmount:Optional[float]=Query(None)
    totalAmount:float
    bookingId:int
    vehicleHeaderId:Optional[int]=Query(None)
    updatedBy:int
    vehicleStatus:Optional[str]=Query(None)
    slotId:Optional[int] = Query(None)
    paymentType:Optional[int]=Query(None)
    transactionId :Optional[str]=Query(None)
    bankName :Optional[str]=Query(None)
    bankReferenceNumber:Optional[str]=Query(None)


class PutBookingPaidAmount(BaseModel):
    paidAmount:float
    bookingId:int
    updatedBy:int
    paymentType:int
    paymentStatus:Optional[str]=Query(None)
    transactionId :Optional[str]=Query(None)
    bankName :Optional[str]=Query(None)
    bankReferenceNumber:Optional[str]=Query(None)

class VerifyOTP(BaseModel):
    username:str

class Forgotpassword(BaseModel):
    password:str
    username:str

class signupOtp(BaseModel):
    username:str

class chargePinConfig(BaseModel):
    chargePinConfig:str
    chargePinImageUrl:str
    activeStatus:str
    createdBy:int

class putchargePinConfig(BaseModel):
    chargePinId:int
    chargePinConfig:str
    chargePinImageUrl:str
    updatedBy:int

class postEmployeeMaster(BaseModel):
    parkingOwnerId :int
    branchId :int
    blockId :int
    floorId :int
    userId :int
    DOJ :datetime
    empType:int
    empDesignation:int
    shiftId:int
    createdBy: int

class PutEmployeeMaster(BaseModel):
    employeeId:int
    branchId :int
    blockId :int
    floorId :int
    empType:int
    DOJ :datetime
    empDesignation:int
    shiftId:int
    updatedBy: int   

class PostParkingOwnerConfig(BaseModel):
    parkingOwnerId:int
    branchId:int
    blockOption:str
    floorOption:str
    squareFeet: Optional[int]=Query(None)
    floorType: Optional[int] = Query(None)
    employeeOption:str
    slotsOption:str
    createdBy:int


class PutParkingOwnerConfig(BaseModel):
    parkingOwnerConfigId:int
    parkingOwnerId:int
    branchId:int
    blockOption:str
    floorOption:str
    squareFeet: Optional[int]=Query(None)
    floorType: Optional[int] = Query(None)
    employeeOption:str
    slotsOption:str
    updatedBy:int

class PaymentUPIDetails(BaseModel):
    name:Optional[str]=Query(None)
    phoneNumber:Optional[str]=Query(None)
    UPIId:str
    branchId :Optional[int]=Query(None)
    merchantId :str
    merchantCode :str
    mode: Optional[str] = Query(None)
    orgId: Optional[str] = Query(None)
    sign : Optional[str] = Query(None)
    url: Optional[str]= Query(None)
    activeStatus:str
    createdBy :int

class PutPaymentUPIDetails(BaseModel):
    name:str
    phoneNumber:str
    UPIId:str
    branchId:int
    merchantId:str
    merchantCode:str
    mode: Optional[str] = Query(None)
    orgId: Optional[str] = Query(None)
    sign : Optional[str] = Query(None)
    url: Optional[str]= Query(None)
    updatedBy:int
    paymentUPIDetailsId:int


class AccessoriesPriceMaster(BaseModel):
    parkingOwnerId:int
    branchId:int
    floorId:int
    amount:float
    tax:float
    totalAmount:float
    vehicleType:int
    accessories:int
    taxId:int
    activeStatus:str
    remarks:Optional[str]=Query(None)
    createdBy:int

class PutAccessoriesPriceMaster(BaseModel):
    parkingOwnerId:int
    branchId:int
    floorId:int
    amount:float
    tax:float
    totalAmount:float
    vehicleType:int
    accessories:int
    taxId:int
    remarks:Optional[str]=Query(None)
    updatedBy:int
    priceId:int


class FireBaseNotification(BaseModel):
    title:str
    body:str
    userId:str

class SendNotification(BaseModel):
    type: Optional[str] = Query(None)
    emailId: Optional[str] = Query(None)
    mobileNo:Optional[str]=Query(None)
    link:Optional[str]=Query(None)


class VehicleSizeConfigMaster(BaseModel):
    vehicleConfigId:int
    modelName:str
    length:Optional[str] = Query(None)
    height:Optional[str] = Query(None)
    activeStatus:str
    createdBy :int

class PutVehicleSizeConfigMaster(BaseModel):
    vehiclesizeConfigId:int
    modelName:str
    length:str
    height:str 
    updatedBy:int