from pydantic import BaseModel

class SearchedProduct(BaseModel):
    WebSiteName: str
    SearchedProduct: str
    TotalFollowUpDays: int

class UpdateTotalFollowUpDaysRemaining(BaseModel):
    SearchedProduct: str
    TotalFollowUpDaysRemaining: int

class Trendyol(BaseModel):
    To: str
    Subject: str
    Header: str