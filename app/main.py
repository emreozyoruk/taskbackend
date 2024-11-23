from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # Bu satırı ekleyin
from app.models import acertificates, add_certificate, get_certificate
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
from fpdf import FPDF
import tempfile
import os

app = FastAPI()

# Sertifika bilgilerini PDF formatında oluşturacak fonksiyon
def generate_pdf(certificate_number: str, candidate_name: str, candidate_surname: str, training_name: str, training_duration: str, training_date: str):
    pdf = FPDF()
    pdf.add_page()
    
    # Başlık
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Certificate of Completion", ln=True, align="C")
    
    pdf.ln(10)
    
    # Sertifika bilgilerini yazma
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Certificate Number: {certificate_number}", ln=True)
    pdf.cell(200, 10, f"Candidate Name: {candidate_name} {candidate_surname}", ln=True)
    pdf.cell(200, 10, f"Training Name: {training_name}", ln=True)
    pdf.cell(200, 10, f"Training Duration: {training_duration}", ln=True)
    pdf.cell(200, 10, f"Training Date: {training_date}", ln=True)
    
    # Geçici dosya oluşturma
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_pdf.name)
    
    return temp_pdf.name

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React frontend adresi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sertifika modeli
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
        return {"message": "Sertifika başarıyla oluşturuldu!"}
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
async def get_certificate_pdf(certificate_number: str):
    try:
        # Burada sertifika bilgilerini veritabanından alabilirsiniz
        # Örneğin, aşağıda sertifika bilgileri sabit verilmiştir
        certificate_data = {
            "certificate_number": certificate_number,
            "candidate_name": "John",
            "candidate_surname": "Doe",
            "training_name": "Python Programming",
            "training_duration": "6 weeks",
            "training_date": "2024-11-20"
        }
        
        # PDF oluşturma
        pdf_file_path = generate_pdf(
            certificate_data["certificate_number"],
            certificate_data["candidate_name"],
            certificate_data["candidate_surname"],
            certificate_data["training_name"],
            certificate_data["training_duration"],
            certificate_data["training_date"]
        )
        
        # PDF dosyasını döndürme
        return FileResponse(pdf_file_path, media_type="application/pdf", filename=f"{certificate_number}_certificate.pdf")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")
