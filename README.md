# 🚀 Diabetes Monitoring App — Automated Deployment (CI/CD)

**Kriteria 3: Automated Deployment (CI/CD)**
**Kelas:** Membangun Sistem Machine Learning
**Program:** PIJAK in Collaboration with IBM SkillsBuild and Dicoding
**Username Dicoding:** `ardian_g8`
**Developer:** Ardian Gymnastiar

---

## 📋 Gambaran Proyek

Proyek **Diabetes Monitoring App** adalah submission akhir untuk kriteria **Automated Deployment (CI/CD)** pada submission akhir kelas **"Membangun Sistem Machine Learning"**. Repositori ini merupakan bagian dari pipeline CI/CD yang melakukan otomatisasi *end-to-end* mulai dari *training model* hingga *deployment* ke **Docker Hub**.

Proyek lengkap (termasuk preprocessing, modelling, tuning, dan monitoring) dapat dilihat di repositori utama:
🔗 [Eksperimen_SML_Ardian-Gymnastiar](https://github.com/ardianx0/Eksperimen_SML_Ardian-Gymnastiar)

---

## 🎯 Tujuan CI/CD

Pipeline CI/CD ini mengotomatiskan seluruh siklus hidup model *machine learning*:

1. **Continuous Integration** — Melatih ulang (*retrain*) model secara otomatis setiap ada perubahan kode di branch `main`
2. **Model Packaging** — Membungkus model terlatih ke dalam container Docker menggunakan MLflow
3. **Continuous Deployment** — Mendorong (*push*) image Docker ke **Docker Hub** untuk siap di-*deploy*

---

## 🔧 Teknologi yang Digunakan

| Teknologi | Kegunaan |
|-----------|----------|
| **GitHub Actions** | Platform CI/CD otomatis |
| **MLflow** | *Experiment tracking* & *model packaging* (build-docker) |
| **Docker** | Containerisasi model |
| **Docker Hub** | Registry image Docker |
| **Python 3.12.7** | Runtime environment |
| **Scikit-learn** | Random Forest Classifier |
| **Pandas** | Manipulasi dataset |

---

## 📁 Struktur Repositori

```
Workflow-CI/
├── .github/workflows/
│   └── ci.yml                          # Workflow CI/CD GitHub Actions
├── .dockerignore                       # File exclusion untuk Docker build
├── MLProject/
│   ├── MLProject                       # Definisi MLflow Project
│   ├── conda.yaml                      # Environment dependencies (Conda)
│   ├── modelling.py                    # Script training model (Random Forest)
│   └── diabetes_clean.csv             # Dataset hasil preprocessing
├── Tautan ke Docker Hub.txt            # Link Docker Hub repository
└── README.md                           # Dokumentasi ini
```

---

## ⚙️ Workflow CI/CD — Penjelasan Detail

Pipeline CI/CD didefinisikan dalam `.github/workflows/ci.yml` yang terdiri dari langkah-langkah berikut:

### 🔄 Trigger

Workflow dipicu secara otomatis setiap ada **push ke branch `main`**.

```yaml
on:
  push:
    branches:
      - main
```

### 📌 Langkah-langkah Workflow

| Step | Action | Deskripsi |
|:----:|--------|-----------|
| 1 | `actions/checkout@v4` | Meng-clone repositori ke runner |
| 2 | `actions/setup-python@v5` | Setup **Python 3.12.7** |
| 3 | **Check Env** | Verifikasi versi Python & pip |
| 4 | **Install dependencies** | Install `mlflow`, `pandas`, `scikit-learn`, `dagshub` |
| 5 | **Run MLflow Project** | Menjalankan `mlflow run MLProject/` — melatih model Random Forest dengan dataset diabetes |
| 6 | **Get latest MLflow run_id** | Mendapatkan ID run terbaru dari hasil training |
| 7 | **Build Docker Model** | Mencari file `MLmodel` hasil training, lalu membangun Docker image menggunakan perintah `mlflow models build-docker` |
| 8 | **Upload to GitHub** | Meng-upload artifact model (`mlruns/`) ke GitHub Actions sebagai backup |
| 9 | **Login to Docker Hub** | Autentikasi ke Docker Hub menggunakan *secrets* `DOCKERHUB_USERNAME` & `DOCKERHUB_TOKEN` |
| 10 | **Tag Docker Image** | Memberi tag image dengan format `ardianx0/diabetes-monitoring-app:latest` |
| 11 | **Push Docker Image** | Mendorong image ke Docker Hub |

### 🔐 Secrets yang Diperlukan

Workflow membutuhkan dua *secrets* yang dikonfigurasi di **Settings → Secrets and variables → Actions** pada repositori GitHub:

| Secret | Deskripsi |
|--------|-----------|
| `DOCKERHUB_USERNAME` | Username Docker Hub (contoh: `ardianx0`) |
| `DOCKERHUB_TOKEN` | *Access token* Docker Hub (bukan password) |

---

## 🧠 Model yang Dilatih

Model yang dilatih secara otomatis oleh pipeline ini adalah **Random Forest Classifier** dengan spesifikasi:

- **Dataset:** Pima Indians Diabetes Database (768 sampel, 8 fitur)
- **Parameter default:**
  - `n_estimators`: 100
  - `max_depth`: 8
- **Target:** Prediksi diabetes (1) atau tidak (0)
- **Experiment tracking:** MLflow (disimpan di `mlruns/`)

---

## 🐳 Docker Image

Image Docker yang dihasilkan menggunakan **MLflow's default model serving infrastructure** yang mencakup:

- **Flask** sebagai REST API server
- **MLflow Model Server** untuk serving model secara otomatis
- Environment yang *self-contained* dengan semua dependencies
- Siap di-*deploy* ke berbagai platform (local, cloud, Kubernetes)

**Link Docker Hub:** 🔗 [ardianx0/diabetes-monitoring-app](https://hub.docker.com/r/ardianx0/diabetes-monitoring-app)

### Menjalankan Container

```bash
docker pull ardianx0/diabetes-monitoring-app:latest
docker run -p 5001:8080 ardianx0/diabetes-monitoring-app:latest
```

Model akan tersedia di `http://localhost:5001/invocations` dengan format request JSON.

**Contoh request:**

```bash
curl -X POST http://localhost:5001/invocations \
  -H "Content-Type: application/json" \
  -d '{
    "dataframe_records": [
      {
        "Pregnancies": 6,
        "Glucose": 148,
        "BloodPressure": 72,
        "SkinThickness": 35,
        "Insulin": 0,
        "BMI": 33.6,
        "DiabetesPedigreeFunction": 0.627,
        "Age": 50
      }
    ]
  }'
```

---

## 📦 Artifact & Backup

Setiap kali workflow berhasil dijalankan:
1. **Model artifacts** di-upload ke GitHub Actions sebagai artifact (`model-artifacts`) — dapat di-download dari halaman workflow run
2. **Docker image** dikirim ke Docker Hub dengan tag `latest`

---

## 🔗 Tautan Penting

| Tujuan | Link |
|--------|------|
| Repositori Proyek Lengkap | [Eksperimen_SML_Ardian-Gymnastiar](https://github.com/ardianx0/Eksperimen_SML_Ardian-Gymnastiar) |
| Docker Hub Image | [ardianx0/diabetes-monitoring-app](https://hub.docker.com/r/ardianx0/diabetes-monitoring-app) |
| Sertifikat Dicoding | [NVP7NV93VZR0](https://www.dicoding.com/certificates/NVP7NV93VZR0) |

---


<p align="center">
 Dibuat oleh <strong>Ardian Gymnastiar</strong> — <code>ardian_g8</code>
</p>