import asyncpg

# Veritabanı bağlantı URL'si
DATABASE_URL = "postgresql://postgres.anuudbpbitfcspfksblh:9446561216Ym@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"

# Veritabanı bağlantısını almak için fonksiyon
async def get_db_connection():
    conn = await asyncpg.connect(DATABASE_URL)
    return conn
