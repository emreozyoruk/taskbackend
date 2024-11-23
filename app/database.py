import asyncpg
from asyncpg import Pool

# Veritabanı bağlantı URL'si
DATABASE_URL = "postgresql://postgres.anuudbpbitfcspfksblh:9446561216Ym@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"

# Veritabanı bağlantısını almak için havuz fonksiyonu
async def get_db_connection() -> Pool:
    # Asyncpg havuzunu oluşturuyoruz
    pool = await asyncpg.create_pool(
        dsn=DATABASE_URL,          # Veritabanı bağlantı URL'si
        min_size=1,                # En az 1 bağlantı
        max_size=10,               # En fazla 10 bağlantı
        statement_cache_size=0     # Prepared statements ile uyumsuzluk için
    )
    return pool

# Bağlantıyı kullanırken havuzu alıp sorguları bu şekilde çalıştırabilirsiniz
async def fetch_data():
    pool = await get_db_connection()
    async with pool.acquire() as conn:  # Bağlantıyı havuzdan alıyoruz
        # Veritabanı sorgusu burada yapılacak
        result = await conn.fetch("SELECT * FROM some_table")
        return result
