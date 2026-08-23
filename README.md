# Clue Dockerfile

Buat file bernama `Dockerfile`.

Gunakan Dockerfile instruction berikut dan lengkapi bagian yang kosong:

```dockerfile
# Base Image Python
FROM ___

# Install package pendukung PostgreSQL
RUN ___

# Tentukan working directory
WORKDIR /app

# Copy source code aplikasi
COPY ___

# Install Python dependencies
RUN ___

# Expose aplikasi
EXPOSE ___

# Jalankan aplikasi
CMD ["___", "___"]
```

## Petunjuk

- Gunakan Python versi `3.11-slim`.
- Install package `libpq-dev` dan `gcc`.
- Gunakan `requirements.txt` untuk dependency Python.
- Aplikasi berjalan pada port `5000`.
- Aplikasi dijalankan menggunakan `python app.py`.

# Clue Docker Compose

Buat file bernama `compose.yaml`.

Docker Compose harus memiliki **2 services**:

- Aplikasi
- PostgreSQL

Lengkapi bagian yang kosong:

```yaml
services:

  # PostgreSQL Database
  db:
    image: ___
    container_name: ___

    environment:
      POSTGRES_USER: ___
      POSTGRES_PASSWORD: ___
      POSTGRES_DB: ___

    volumes:
      - ___:/var/lib/postgresql/data

    networks:
      - ___

  # Python Application
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

- Gunakan PostgreSQL versi `15`.
- Nama container aplikasi: `login-service`.
- Nama container database: `db`.
- Aplikasi menggunakan port container `5000`.
- Aplikasi dapat diakses melalui port host `8098`.
- Aplikasi dan database harus berada pada network yang sama.
- Gunakan named volume untuk database.
- Mount volume ke `/var/lib/postgresql/data`.
- Gunakan environment variable:
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `DATABASE_URL` harus menggunakan nama service database sebagai hostname.
