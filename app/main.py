from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.models import acertificates, add_certificate, get_certificate
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
from fpdf import FPDF

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React frontend adresi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Certificate model
class CertificateCreate(BaseModel):
    certificate_number: str
    candidate_name: str
    candidate_surname: str
    training_name: str
    training_duration: str
    training_date: str

@app.post("/certificates/")
async def create_certificate(cert: CertificateCreate):
    try:
        await add_certificate(
            cert.certificate_number,
            cert.candidate_name,
            cert.candidate_surname,
            cert.training_name,
            cert.training_duration,
            cert.training_date,
        )
        return {"message": "Certificate created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/certificates/")
async def get_all_certificates_endpoint():
    try:
        return await acertificates()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@app.get("/certificates/{certificate_number}")
async def read_certificate(certificate_number: str):
    try:
        return await get_certificate(certificate_number)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@app.get("/certificates/{certificate_number}/pdf")
async def generate_certificate_pdf(certificate_number: str):
    try:
        certificate = await get_certificate(certificate_number)
        if not certificate:
            raise HTTPException(status_code=404, detail="Certificate not found")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Certificate of Completion", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Certificate Number: {certificate['certificate_number']}", ln=True)
        pdf.cell(200, 10, txt=f"Candidate Name: {certificate['candidate_name']} {certificate['candidate_surname']}", ln=True)
        pdf.cell(200, 10, txt=f"Training Name: {certificate['training_name']}", ln=True)
        pdf.cell(200, 10, txt=f"Training Duration: {certificate['training_duration']}", ln=True)
        pdf.cell(200, 10, txt=f"Training Date: {certificate['training_date']}", ln=True)

        pdf_path = f"certificate_{certificate['certificate_number']}.pdf"
        pdf.output(pdf_path)

        return FileResponse(path=pdf_path, media_type="application/pdf", filename=pdf_path)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
