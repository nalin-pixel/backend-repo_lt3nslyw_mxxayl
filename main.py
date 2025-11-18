from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from database import create_document, db
from schemas import SupplierInquiry as SupplierInquirySchema

app = FastAPI(title="The Blacksmith Market API", version="1.0.0")

# CORS - allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SupplierInquiry(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=200)
    contact_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=40)
    website: Optional[str] = Field(None, max_length=200)
    company_type: str = Field(..., min_length=2, max_length=120)
    product_categories: str = Field(..., min_length=2, max_length=300)
    estimated_monthly_volume: str = Field(..., min_length=1, max_length=100)
    message: Optional[str] = Field(None, max_length=2000)

@app.get("/test")
async def test():
    try:
        ok = db is not None and db.client is not None
        return {"status": "ok", "database": "connected" if ok else "not_configured"}
    except Exception as e:
        return {"status": "ok", "database": f"error: {e}"}

@app.post("/api/supplier-inquiry")
async def supplier_inquiry(payload: SupplierInquiry):
    try:
        # Validate against schema (ensures alignment with DB viewer expectations)
        _ = SupplierInquirySchema(**payload.model_dump())
        inserted_id = create_document("supplierinquiry", payload)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
