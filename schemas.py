from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class SupplierInquiry(BaseModel):
    company_name: str = Field(..., description="Company legal/trading name")
    contact_name: str = Field(..., description="Primary contact full name")
    email: EmailStr = Field(..., description="Work email")
    phone: Optional[str] = Field(None, description="Phone number")
    website: Optional[str] = Field(None, description="Company website")
    company_type: str = Field(..., description="e.g., Distributor, Brand, 3PL, Retailer")
    product_categories: str = Field(..., description="Categories you handle")
    estimated_monthly_volume: str = Field(..., description="Units or pallets per month")
    message: Optional[str] = Field(None, description="Additional details")
