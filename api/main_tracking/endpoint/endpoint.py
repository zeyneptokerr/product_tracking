from fastapi import APIRouter
from ..database import db_operations
from ..schemas import SearchedProduct
from ..schemas import UpdateTotalFollowUpDaysRemaining

router = APIRouter()    

@router.post("/create-product-tracking")
def create_product_tracking(data: SearchedProduct):
    is_there_in_products = db_operations.is_there_in_products(data.SearchedProduct, data.WebSiteName)
    if is_there_in_products is None:
        result = db_operations.create_product(data)
        return result
    else:
        return {"Status": "",
                "Message": "Already Exist"}


@router.put("/update-product-follow-up-days")
def update_product_follow_up_days(data: UpdateTotalFollowUpDaysRemaining):
    result = db_operations.update_product_follow_up_days(data.SearchedProduct, data.TotalFollowUpDaysRemaining)
    return result