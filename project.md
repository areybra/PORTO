# AREYBRA Portfolio — Technical Documentation & Architecture

> **Canonical Entity:** Areta Y. Radjawali  
> **Alternate Names:** Areta Ybei Radjawali, Areybra, Areta Radjawali, AREYBRA Studio  
> **Role:** Junior Web Developer, Data Analyst, Cyber Security Enthusiast  
> **Base Locations:** Kabupaten Probolinggo, Jawa Timur & Jakarta, Indonesia  

---

## 1. Executive Summary & Architecture Overview

AREYBRA is a production-grade, high-performance portfolio and personal knowledge base built with **Django 6.x**, styled via **Tailwind CSS (CDN/JIT modern styling)** with custom design tokens (`#094cb2` primary, `#6d5e00` secondary, ambient radial glows), backed by **MySQL (Production / Railway)** and **SQLite (Development)**, and engineered for high-availability serverless deployment on **Vercel** via WhiteNoise and WSGI adapters.

### Architectural Pillars
1. **Modular Monolith (4 Core Apps):**
   - `apps.core`: Site singleton profile, traits, skill categories, SEO/GEO metadata engines, sitemaps, robots/humans/llms text generators.
   - `apps.portfolio`: Project studies, categories, technologies (Many-to-Many), spotlight curation, views counter, external image URL handling for lightweight storage.
   - `apps.blog`: Posts, categories, tags, markdown-ready rich text, view counters, archiving by year.
   - `apps.contact`: Contact messages, FAQ items, secure form processing with direct WhatsApp redirect (`wa.me/6282142961010`).
2. **SEO & GEO (Generative Engine Optimization):**
   - Deep support for brand aliases (`Areta Y. Radjawali`, `Areta Ybei Radjawali`, `Areybra`, `AREYBRA Studio`).
   - Automated JSON-LD structured data generation (`WebSite`, `Person`, `Organization`, `BreadcrumbList`, `FAQPage`, `CreativeWork`, `BlogPosting`).
   - Dynamic `/sitemap.xml`, `/robots.txt`, `/humans.txt`, and `/llms.txt` designed for AI crawlers, LLM citation, and search engine indexing.

---

## 2. Database Schema & Models

### Core (`apps.core`)
- **`SiteProfile` (SingletonModel):** Stores hero branding, about copy, resume PDF links, WhatsApp number (`6282142961010`), and profile image URLs.
- **`Trait` & `SkillCategory` / `Skill`:** Structured JSON/relational mapping for skills (Django, Python, Tailwind, MySQL, Linux, Cyber Security, Data Analysis) displayed in interactive matrix components.
- **`FAQ`:** Dynamic FAQ items rendered on contact and landing pages with schema validation.

### Portfolio (`apps.portfolio`)
- **`Category`:** Name, slug, description, ordering.
- **`Technology`:** Name, slug, icon badge.
- **`Project`:** Title, slug, category (FK), technologies (M2M), excerpt, description, `thumbnail_url` (external URL for zero-storage overhead), fallback mock type, year, reference code (e.g. `#KRM-01`), featured status, spotlight flag, views count, status (`published`/`draft`).

### Blog (`apps.blog`)
- **`Category` & `Tag`:** Taxonomy for articles.
- **`Post`:** Title, slug, category, tags (M2M), excerpt, content, `cover_url`, featured flag, spotlight flag, views count, status, timestamps.

### Contact (`apps.contact`)
- **`ContactMessage`:** Name, email, phone, domain/topic, message body, WhatsApp sent flag, timestamp.

---

## 3. UI/UX Design System & JavaScript Interactivity

### Color & Styling System
- Built with a sophisticated color palette avoiding harsh contrasts:
  - Surface container lowest/low with ambient blur effects.
  - Primary blue (`#094cb2`) and warm accent gold (`#6d5e00`) for visual harmony.
- Responsive flex/grid layouts with mobile-first approach.

### JavaScript Behaviors (`static/js/main.js`)
- **Typing Effect (`data-typing`):** Dynamic typewriter animation for hero subheadings.
- **Scroll Reveal (`.reveal`):** Intersection Observer based fade-in animations on scroll.
- **Interactive Hamburger Navigation:** Fullscreen/drawer modal for screens `<1024px` with smooth transition, focus trap, and ESC key close handler.
- **Filter & Search:** Real-time query filtering on Projects and Blog listings.
- **Clipboard Utility:** One-click copy for contact emails and codes.

---

## 4. Deployment & Production Pipeline

### Vercel Serverless Configuration (`vercel.json`)
- Runtime: Python 3.12 (`@vercel/python`).
- Static file management: WhiteNoise middleware for efficient asset delivery.
- WSGI Entry: `api/index.py` wrapping Django application.
- Automated `collectstatic` build hook.

### Database Flexibility
- **Development:** SQLite (`db.sqlite3`).
- **Production:** MySQL on Railway via `dj-database-url` parsing `DATABASE_URL`.
