<div align="center">

# 🚀 AREYBRA PORTFOLIO & KNOWLEDGE BASE
### Production-Grade Django 6 Full-Stack Portfolio & Generative Engine Optimized (GEO) Web Application

[![Django](https://img.shields.io/badge/Django-6.1.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Vercel](https://img.shields.io/badge/Vercel-Serverless-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

**Canonical Owner:** Areta Y. Radjawali *(Also known as Areta Ybei Radjawali / Areybra / AREYBRA Studio)*  
**Roles:** Junior Web Developer, Data Analyst, Cyber Security Enthusiast  
**Locations:** Kabupaten Probolinggo, Jawa Timur & Jakarta, Indonesia  

[✨ Explore Live Demo](https://areybra.vercel.app) • [📖 Technical Documentation](project.md) • [💬 Contact via WhatsApp](https://wa.me/6282142961010)

</div>

---

## 🌟 Overview

**AREYBRA** is a high-performance personal portfolio, case study archive, and engineering blog designed with an editorial aesthetic (Brunelle style). It features rigorous database normalization, zero-storage overhead image handling via external URLs, complete SEO + GEO (Generative Engine Optimization) metadata, dynamic JSON-LD structured data, and responsive interactive JavaScript components.

---

## ✨ Key Features

- **🌐 Comprehensive SEO & GEO Integration:**
  - Full alias coverage for generative AI search engines (`Areta Y. Radjawali`, `Areta Ybei Radjawali`, `Areybra`, `AREYBRA Studio`).
  - Automated JSON-LD schemas (`WebSite`, `Person`, `Organization`, `BreadcrumbList`, `FAQPage`, `CreativeWork`, `BlogPosting`).
  - Native `/sitemap.xml`, `/robots.txt`, `/humans.txt`, and `/llms.txt`.
- **💼 Relational Portfolio & Blog:**
  - Case studies with categories, technology badges, spotlight features, and view counters.
  - Rich technical blog essays with year-based archiving and tagging.
- **💬 Direct WhatsApp Conversion:**
  - Contact form with instant auto-formatting and direct redirect to WhatsApp (`+62 821-4296-1010`).
- **⚡ Modern UI/UX & Animations:**
  - Custom Tailwind design tokens (`#094cb2` primary, `#6d5e00` secondary).
  - Typewriter hero effect (`data-typing`), scroll-reveal animations (`.reveal`), and full-screen mobile hamburger drawer.
- **☁️ Serverless & Cloud Ready:**
  - Optimized for **Vercel** serverless deployment with WhiteNoise static asset serving and **Supabase PostgreSQL** (pooled PgBouncer) integration.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python 3.12, Django 6.1.1, WSGI / WhiteNoise |
| **Database** | SQLite (Local Dev), PostgreSQL Supabase (Production via `dj-database-url`, pooled `6543` + `pgbouncer=true`, `ssl_require=True`) |
| **Frontend** | HTML5, Tailwind CSS, Modern Vanilla JavaScript (ES Modules) |
| **Admin Panel** | Django Jazzmin Custom Theme |
| **Deployment** | Vercel Serverless (`vercel.json`), Git |

---

## ⚙️ Quick Start (Local Development)

### 1. Clone & Setup Environment
```bash
git clone https://github.com/areybra/myweb.git
cd myweb

# Create & activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and configure your settings:
```env
DJANGO_SECRET_KEY=your-secure-secret-key
DJANGO_SETTINGS_MODULE=config.settings.development
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
SITE_URL=http://localhost:8000
WHATSAPP_NUMBER=6282142961010
```

### 3. Run Migrations & Seed Initial Data
```bash
python manage.py migrate
python manage.py loaddata initial_data.json  # (if available) or create superuser
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser.

---

## 📂 Project Structure

```text
areybra-portfolio/
├── api/                # Vercel WSGI entry point
├── apps/               # Modular Django apps
│   ├── core/           # Singleton profile, SEO/GEO engines, sitemaps
│   ├── portfolio/      # Projects, categories, technologies
│   ├── blog/           # Articles, tags, archives
│   └── contact/        # Contact form, FAQs, WhatsApp redirect
├── config/             # Django settings (base, development, production), URLs, WSGI/ASGI
├── static/             # CSS, JavaScript (typing, reveal, hamburger), assets
├── templates/          # HTML templates & modular partials (_navbar, _footer, _seo_head)
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel deployment configuration
├── project.md          # In-depth technical documentation
└── README.md           # Project readme
```

---

## 📜 License & Acknowledgements

Developed with ❤️ by **Areta Y. Radjawali (Areybra)**.  
Inspired by editorial design standards and engineered for maximum web performance.
