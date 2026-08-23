# Clue

## Step 1 - Download Source Code

Download source code aplikasi dari repository berikut:

https://github.com/nitaoktaviani28/python-login-app

Clone repository tersebut menggunakan Git.

```bash
git clone https://github.com/nitaoktaviani28/python-login-app.git
```

Masuk ke directory aplikasi:

```bash
cd python-login-app
```

## Step 2 - Menjalankan Aplikasi Secara Manual

Sebelum membuat Dockerfile, pahami terlebih dahulu kebutuhan aplikasi.

### 1. Gunakan Python 3.11

Pastikan Python yang digunakan adalah versi 3.11.

```bash
python3 --version
```

### 2. Install Package Pendukung

Aplikasi membutuhkan package pendukung PostgreSQL.

```bash
apt-get update && apt-get install -y libpq-dev gcc
```

### 3. Install Python Dependencies

Install dependency yang terdapat pada requirements.txt.

```bash
pip install --no-cache-dir -r requirements.txt
```

### 4. Konfigurasi Database

Aplikasi membutuhkan PostgreSQL sebagai database.

Aplikasi menggunakan environment variable:

```bash
DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:5432/DATABASE
```

Contoh:

```bash
DATABASE_URL=postgresql://admin:password123@localhost:5432/login_db
```

### 5. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi berjalan pada port:

```text
5000
```

## Yang Perlu Diperhatikan

Ketika aplikasi dijalankan menggunakan Docker:

- Aplikasi menggunakan port 5000.
- Aplikasi membutuhkan DATABASE_URL.
- PostgreSQL akan dijalankan sebagai container terpisah.
- Aplikasi dan database harus terhubung melalui Docker network.
- HOST pada DATABASE_URL harus menggunakan nama service PostgreSQL pada Docker Compose.

Contoh format:

```bash
postgresql://USERNAME:PASSWORD@HOST:5432/DATABASE
```

## Clue Dockerfile

Buat file bernama Dockerfile.

Berikut adalah beberapa Dockerfile instruction yang dapat digunakan. Lengkapi bagian yang masih kosong.

```dockerfile
# Base Image Python
FROM ___

# Install package pendukung PostgreSQL
RUN ___

# Working directory
WORKDIR ___

# Copy source code aplikasi
COPY ___

# Install Python dependencies
RUN ___

# Expose port aplikasi
EXPOSE ___

# Jalankan aplikasi
CMD ["___", "___"]
```

## Clue Docker Compose

Buat file bernama compose.yaml.

Docker Compose harus menjalankan aplikasi dan database sebagai dua service.

```yaml
services:

  # Service PostgreSQL
  db:
    image: ___
    container_name: ___

    environment:
      ___
      ___
      ___

    volumes:
      - ___:/var/lib/postgresql/data

    networks:
      - ___

  # Service aplikasi
  aplikasi:
    build: ___
    container_name: ___

    ports:
      - "8098:___"

    environment:
      DATABASE_URL: postgresql://USERNAME_DATABASE:PASSWORD_DATABASE@DNS_DB:5432/NAMA_DATABASE

    networks:
      - ___

networks:
  ___:
    driver: bridge

volumes:
  ___:
```

## Petunjuk

- Gunakan Python 3.11-slim.
- PostgreSQL menggunakan image postgres:15.
- Nama container aplikasi: login-service.
- Nama container database: db.
- Aplikasi menggunakan port container 5000.
- Aplikasi diakses melalui port host 8098.
- PostgreSQL membutuhkan POSTGRES_USER.
- PostgreSQL membutuhkan POSTGRES_PASSWORD.
- PostgreSQL membutuhkan POSTGRES_DB.
- Gunakan network yang sama untuk kedua service.
- Gunakan named volume untuk database.
- Mount volume pada /var/lib/postgresql/data.
- DATABASE_URL menggunakan nama service database sebagai hostname.
