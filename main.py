from distutils.command.upload import upload
from fastapi.applications import FastAPI
import uvicorn
from fastapi import status,Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import userMaster,menuOptionAccess,menuOptions,moduleAccess,moduleMaster,configMaster,configType,taxMaster,feedBackMaster,subscriptionMaster, userSubscription,vehicleMaster,login,upload,parkingOwnerMaster,branchMaster,blockMaster,addressMaster,floorMaster,branchWorkingHrs,priceMaster,parkingSlot,shiftMaster,timeSlabRules,postparkingSlot,vehicleHeader,floorImageMaster,floorFeatures,floorVehicleMaster,booking,userSlot,extraFees,extraFeatures,parkingPassConfig,faq,cancellationRules,appSettings,printingInstructionsConfig,userWallet,passTransaction,admin,offerMaster,offerRules,offerMapping,userOffers,passBooking,cancellationupdate,vehicleConfigMaster,verifyOTP,forgotpassword,GetBranchDetails,chargePinConfig,passBookingTransaction,parkingOwnerConfig,paymentUPIDetails,accessoriesPriceMaster,fireBaseNotification,paymentTransactionHistory,addOnService,vehicleSizeConfigMaster
from routers import messageTemplates,signupOtp,employeeMaster, generatePin, parkingSlotTest,sendNotification, vehicleNumber

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "statusCode": "0","response":"Invalid Data"}),
    )


origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(userMaster.router)
app.include_router(userMaster.routerApproval)
app.include_router(moduleMaster.router)
app.include_router(menuOptions.router)
app.include_router(moduleAccess.router)
app.include_router(menuOptionAccess.router)
app.include_router(configMaster.router)
app.include_router(configType.router)
app.include_router(taxMaster.router)
app.include_router(feedBackMaster.router)
app.include_router(subscriptionMaster.router)
app.include_router(vehicleMaster.router)
app.include_router(userSubscription.router)
app.include_router(login.router)
app.include_router(upload.router)
app.include_router(parkingOwnerMaster.router)
app.include_router(branchMaster.router)
app.include_router(blockMaster.router)
app.include_router(addressMaster.router)
app.include_router(floorMaster.router)
app.include_router(branchWorkingHrs.router)
app.include_router(priceMaster.router)
app.include_router(parkingSlot.router)
app.include_router(shiftMaster.router)
app.include_router(timeSlabRules.router)
app.include_router(postparkingSlot.router)
app.include_router(vehicleHeader.router)
app.include_router(extraFeatures.router)
app.include_router(floorImageMaster.router)
app.include_router(floorFeatures.router)
app.include_router(floorVehicleMaster.router)
app.include_router(booking.router)
app.include_router(booking.routerPaidAmount)
app.include_router(booking.routerDateTimeExtend)
app.include_router(userSlot.router)
app.include_router(extraFees.router)
app.include_router(parkingPassConfig.router)
app.include_router(faq.router)
app.include_router(cancellationRules.router)
app.include_router(appSettings.router)
app.include_router(appSettings.router1)
app.include_router(printingInstructionsConfig.router)
app.include_router(userWallet.router)
app.include_router(passTransaction.router)
app.include_router(messageTemplates.router)
app.include_router(admin.router)
app.include_router(offerMaster.router)
app.include_router(offerRules.router)
app.include_router(offerMapping.router)
app.include_router(userOffers.router)
app.include_router(passBooking.router)
app.include_router(cancellationupdate.router)
app.include_router(vehicleConfigMaster.router)
app.include_router(verifyOTP.router)
app.include_router(forgotpassword.router)
app.include_router(GetBranchDetails.router)
app.include_router(signupOtp.router)
app.include_router(chargePinConfig.router)
app.include_router(employeeMaster.router)
app.include_router(generatePin.router)
app.include_router(parkingSlotTest.router)
app.include_router(sendNotification.router)
app.include_router(passBookingTransaction.router)
app.include_router(parkingOwnerConfig.router)
app.include_router(priceMaster.router1)
app.include_router(paymentUPIDetails.router)
app.include_router(vehicleNumber.router)
app.include_router(accessoriesPriceMaster.router)
app.include_router(fireBaseNotification.router)
app.include_router(userMaster.routerToken)
app.include_router(printingInstructionsConfig.router1)
app.include_router(booking.routerBasedOnSlotId)
app.include_router(booking.getDataBasedOnVehicleNumberPhone)
app.include_router(paymentTransactionHistory.router)
app.include_router(addOnService.router)
app.include_router(vehicleSizeConfigMaster.router)

@app.get("/")
def home():
    return {
        "data":"api running successfully"
    }


