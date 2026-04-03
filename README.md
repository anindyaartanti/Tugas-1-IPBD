# Tugas-1-IPBD

Tugas Infrastruktur dan Platform Big Data: “Implementasi Backend Crud Tercontainerisasi Menggunakan Fastapi dan Postgresql”. Sistem backend RESTful API untuk manajemen penjualan (Customer, Product, Sales Order). Dibangun menggunakan **FastAPI**, **SQLAlchemy**, **PostgreSQL**, **Alembic**, dan **Docker Compose** untuk containerisasi.

## Fitur Utama

- **CRUD** untuk Customer, Product, dan Sales Order
- **Migrasi database** dengan Alembic
- **Seeding data awal** – otomatis mengisi 10 customer, 10 produk, dan 10 sales order jika database kosong
- **Containerisasi penuh** dengan Docker Compose
- **PgAdmin** untuk administrasi database (opsional)

## Teknologi yang Digunakan

| Teknologi         | Keterangan                          |
|------------------|--------------------------------------|
| FastAPI          | Framework web modern (Python)        |
| SQLAlchemy       | ORM untuk interaksi database         |
| PostgreSQL 15    | Database relasional                  |
| Alembic          | Version control untuk skema database |
| Pydantic         | Validasi data dan serialisasi        |
| Uvicorn          | ASGI server                          |
| Docker & Compose | Containerisasi dan orchestration     |

## Prasyarat

- **Docker**
- **Docker Compose**

## Cara Menjalankan

1. **Clone repository**

2. **Bangun dan jalankan container**:
   ```bash
   docker-compose up --build

3. **Tunggu hingga semua service aktif (backend, database, pgadmin)**

4. **Akses aplikasi:**
- Swagger UI (dokumentasi & testing API): http://localhost:8000/docs
- ReDoc (dokumentasi alternatif): http://localhost:8000/redoc
- PgAdmin (manajemen database): http://localhost:8080
Email: admin@mail.com
Password: admin123
Server: hostname db, port 5432, username admin, password admin123, database latihan_db

## Struktur Proyek

```markdown
├── main.py              # Entry point FastAPI, endpoint definitions
├── models.py            # SQLAlchemy models (tabel database)
├── schemas.py           # Pydantic schemas (validasi request/response)
├── crud.py              # Fungsi CRUD (operasi database)
├── database.py          # Konfigurasi koneksi database
├── seed.py              # Seeder untuk data awal
├── entrypoint.sh        # Script startup (migrasi + seed + start server)
├── requirements.txt     # Dependencies Python
├── Dockerfile           # Docker image untuk backend
├── docker-compose.yml   # Orchestration semua service
├── alembic/             # Folder migrasi database
│   ├── versions/        # File migrasi (.py)
│   ├── env.py
│   └── script.py.mako
├── alembic.ini          # Konfigurasi Alembic
├── .dockerignore
├── .gitignore
└── README.md

## Seeding Data Awal

- Script seed.py akan mengisi data awal jika tabel customers kosong.
- Data yang diisi: 10 customer, 10 produk (laptop, mouse, dll), dan 10 sales order dengan 1-3 item setiap order.
- Stok produk juga ikut berkurang sesuai order yang di-seed.
