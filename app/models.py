from app.database import get_db_connection
from fastapi import HTTPException
from datetime import datetime

# Veritabanı işlemleri için try-except bloğuna daha ayrıntılı loglama ekleyelim
async def add_certificate(certificate_number: str, candidate_name: str, candidate_surname: str, training_name: str, training_duration: str, training_date: str):
    try:
        training_date = datetime.strptime(training_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    conn = await get_db_connection()
    try:
        await conn.execute("""
            INSERT INTO certificates (certificate_number, candidate_name, candidate_surname, training_name, training_duration, training_date)
            VALUES ($1, $2, $3, $4, $5, $6)
        """, certificate_number, candidate_name, candidate_surname, training_name, training_duration, training_date)
    except Exception as e:
        # Burada hata mesajlarını daha net bir şekilde alıp logluyoruz
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    finally:
        await conn.close()

async def get_certificate(certificate_number: str):
    conn = await get_db_connection()
    try:
        result = await conn.fetchrow("SELECT * FROM certificates WHERE certificate_number = $1", certificate_number)
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Certificate not found")
    except Exception as e:
        # Burada da veritabanı hatalarını logluyoruz
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        await conn.close()

async def acertificates():
    conn = await get_db_connection()
    try:
        result = await conn.fetch("SELECT * FROM certificates")
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="No certificates found")
    except Exception as e:
        # Burada da genel veritabanı hatalarını logluyoruz
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        await conn.close()
