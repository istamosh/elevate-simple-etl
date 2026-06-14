# Microsoft Elevate Program Simple ETL Submission

Proyek ini merupakan submission ETL sederhana yang terdiri dari tiga tahap utama: **extract**, **transform**, dan **load**. Tahap extract mengambil data produk dari situs `fashion-studio.dicoding.dev` dengan pagination hingga halaman 50 dan menyimpannya ke file JSON mentah.[1]  
Tahap transform membersihkan harga, membuang `Unknown Product`, menghapus data duplikat berdasarkan kombinasi `title`, `size`, dan `gender`, lalu mengonversi harga ke IDR, rating ke float, serta merapikan field `size` dan `gender`.[2]  
Tahap load membaca hasil transform dari JSON, menuliskannya ke `final_data.csv`, lalu memverifikasi hasilnya kembali dengan pandas.[3]

## Struktur Proyek

```text
.
├── extract.ipynb
├── transform.ipynb
├── load.ipynb
├── utils/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── extracted_data.json
├── cleaned_data.json
├── transformed_data.json
├── final_data.csv
├── pyproject.toml
├── requirements.txt
└── README.md
```

> File `.py` digunakan agar fungsi pada tiap fase bisa diuji dengan `pytest`, sementara notebook tetap dipakai untuk alur eksplorasi dan eksekusi setiap fase.

## Alur ETL

### 1. Extract

Tahap extract mencakup:
- membangun daftar URL pagination dari halaman utama sampai `page50`.[1]
- melakukan request ke setiap halaman dengan `requests.get(..., timeout=10)`.[1]
- mem-parsing HTML menggunakan BeautifulSoup dan mengambil elemen dengan class `product-details`.[1]
- mengekstrak field `title`, `price`, `rating`, `color`, `size`, dan `gender` dari tiap kartu produk.[1]
- menyimpan hasil ke `extracted_data.json` agar proses scraping tidak perlu diulang jika file sudah tersedia.[1]

### 2. Transform

Tahap transform mencakup:
- validasi harga agar hanya harga valid yang diproses.[2]
- membuang produk dengan title `Unknown Product`.[2]
- menghapus duplikasi berdasarkan `(title, size, gender)`.[2]
- mengubah `price` dari string USD ke integer IDR.[2]
- mengubah `rating` dari string seperti `Rating: ⭐ 4.8 / 5` menjadi `float`.[2]
- membersihkan prefix `Size: ` dan `Gender: `.[2]
- menyimpan hasil akhir ke `transformed_data.json`.[2]

### 3. Load

Tahap load mencakup:
- membaca `transformed_data.json`.[3]
- menulis data ke `final_data.csv` menggunakan `csv.DictWriter`.[3]
- membaca ulang CSV menggunakan pandas untuk verifikasi hasil.[3]
- hasil akhir menunjukkan dataset berisi 867 baris dan 6 kolom: `title`, `price`, `rating`, `color`, `size`, dan `gender`.[3]

## Environment Setup

Proyek ini dibuat menggunakan **uv** dan environment virtual (**venv**). Gunakan salah satu pola berikut.

### Opsi 1: `uv`

Buat virtual environment:

```bash
uv venv
```

Aktifkan environment:

- Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

- Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

- Bash/Git Bash:

```cmd
source .venv\Scripts\activate
```

Install dependency from the provided `pyproject.toml`:

```bash
uv sync
```

### Opsi 2: `venv` bawaan Python

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan environment:

- Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

- Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

- Mac OS/Linux:

```cmd
source .venv/bin/activate
```

Install dependency:

```bash
pip install -r requirements.txt
```

## Menjalankan Notebook

Jalankan pipeline ETL dengan:
`python run_pipeline.py`

## Menjalankan Unit Test

Jalankan test secara verbose:

```bash
python -m pytest -v
```

Untuk melihat coverage:

```bash
python -m pytest --cov=utils --cov-report=term-missing
```

Cakupan pengujian:
- **Extract**: build URL, parsing tiap produk, parsing entri bolong-bolong, dan struktur hasil scraping.[1]
- **Transform**: validasi harga, filter `Unknown Product`, deduplikasi, konversi harga, parsing rating, serta pembersihan `size` dan `gender`.[2]
- **Load**: pembacaan JSON, penulisan CSV, verifikasi header, jumlah baris, serta pembacaan dan penyajian data dengan pandas.[3]

## Output File

File hasil pada tiap tahap:

| Tahap | File Output | Keterangan |
|---|---|---|
| Extract | `extracted_data.json` | Data mentah hasil scraping.[1] |
| Transform (cleaning awal) | `cleaned_data.json` | Data setelah validasi harga, filter title, dan deduplikasi.[2] |
| Transform (final) | `transformed_data.json` | Data yang sudah dikonversi dan dirapikan.[2] |
| Load | `final_data.csv` | Dataset final dalam format CSV.[3] |

## Catatan Implementasi

- Pada tahap extract, jika file JSON sudah ada, proses akan memuat file tersebut dan tidak melakukan scraping ulang.[1]
- Pada tahap transform, nilai rating yang tidak valid diubah menjadi `None` sesuai logika transform saat parsing rating.[2]
- Pada tahap load, pandas membaca kembali file CSV untuk memastikan struktur data akhir sesuai harapan.[3]