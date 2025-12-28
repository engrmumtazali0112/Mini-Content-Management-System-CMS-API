# 🚀 Mini Content Management System (CMS) API

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2.7-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django%20REST-3.14.0-ff1709?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

**A robust, production-ready REST API built with Django REST Framework**

[Features](#-features) • [Quick Start](#-quick-start) • [API Documentation](#-api-endpoints) • [Screenshots](#-screenshots) • [Architecture](#-architecture)

</div>

---


## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [API Endpoints](#-api-endpoints)
- [Assessment Validation](#-assessment-validation)
- [Database Schema](#-database-schema)
- [Authentication](#-authentication)
- [Permissions](#-permissions)
- [Testing](#-testing)
- [Deployment](#-deployment)

---

## 🎯 Overview

Mini CMS is a feature-rich Content Management System API designed for managing articles, categories, and users with role-based access control. Built following Django REST Framework best practices, it provides secure JWT authentication, optimized database queries, and comprehensive API documentation.

### 🎖️ Backend Engineering Assessment

This project fulfills all requirements of the Backend Engineering Test Assignment:
- ✅ JWT-based authentication with Admin/Author roles
- ✅ Complete Category & Article CRUD operations
- ✅ Role-based permissions and access control
- ✅ PostgreSQL database with optimized queries
- ✅ Pagination and filtering capabilities
- ✅ Web scraping bonus feature
- ✅ Clean architecture and error handling
- ✅ Interactive API documentation (Swagger/ReDoc)

---

## ✨ Features

### 🔐 Authentication & Authorization
- **JWT Token-Based Authentication** - Secure access with refresh tokens
- **Role-Based Access Control** - Admin and Author roles with specific permissions
- **User Profile Management** - Update profile, change password, secure logout

### 📝 Article Management
- **Full CRUD Operations** - Create, Read, Update, Delete articles
- **Draft/Published Status** - Control article visibility
- **Author Ownership** - Authors can only edit their own articles
- **View Counter** - Track article popularity
- **Rich Content** - Title, description, content, featured images
- **Advanced Filtering** - Filter by status, category, author, date range
- **Search Functionality** - Full-text search across title, description, content

### 🗂️ Category Management
- **Admin-Only Control** - Secure category management
- **Auto-Generated Slugs** - SEO-friendly URLs
- **Article Counting** - Track published articles per category

### 🌐 Web Scraping (Bonus)
- **Automated Article Scraping** - Fetch latest tech articles from Hacker News
- **Database Integration** - Store scraped content
- **Admin-Only Access** - Secure scraping operations

### 🎨 API Features
- **Pagination** - Efficient data loading with customizable page sizes
- **Ordering** - Sort by date, views, title, etc.
- **Filtering** - Advanced query parameters
- **Swagger Documentation** - Interactive API testing
- **Optimized Queries** - No N+1 issues with select_related/prefetch_related

---



## 📸 Screenshots

<div align="center">

### API Root - Welcome Page
![API Root](https://github.com/engrmumtazali0112/Mini-Content-Management-System-CMS-API/blob/main/Demo/home.JPG?raw=true)
*Clean and organized API navigation with all available endpoints*

### Swagger UI - Complete API Documentation
![Swagger API](https://github.com/engrmumtazali0112/Mini-Content-Management-System-CMS-API/blob/main/Demo/AllApi.JPG?raw=true)
*Interactive Swagger documentation showing all API endpoints with color-coded HTTP methods (GET, POST, PUT, PATCH, DELETE)*

### Admin - All Draft Articles
![Draft Articles](https://github.com/engrmumtazali0112/Mini-Content-Management-System-CMS-API/blob/main/Demo/AdminSeeAllDraps.JPG?raw=true)
*Admin can view all draft articles from all authors with complete metadata*

### Author - Draft Articles Endpoint
![Author Drafts](https://github.com/engrmumtazali0112/Mini-Content-Management-System-CMS-API/blob/main/Demo/AuthorDrapsArticle.JPG?raw=true)
*Authors can view their own draft articles with category and author information*

### Author - My Articles Endpoint
![My Articles](https://github.com/engrmumtazali0112/Mini-Content-Management-System-CMS-API/blob/main/Demo/AuthorMyAllArticle.JPG?raw=true)
*Authors can view and manage all their own articles (drafts and published)*

### Web Scraper - Latest Articles
![Web Scraper](https://github.com/engrmumtazali0112/Mini-Content-Management-System-CMS-API/blob/main/Demo/ScrapLatestArticle.JPG?raw=true)
*Automated web scraping feature fetching latest tech articles from Hacker News*

</div>

---


## 🛠️ Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **Django** | Web Framework | 4.2.7 |
| **Django REST Framework** | API Framework | 3.14.0 |
| **PostgreSQL** | Database | 12+ |
| **SimpleJWT** | JWT Authentication | 5.3.0 |
| **drf-yasg** | API Documentation | 1.21.7 |
| **BeautifulSoup4** | Web Scraping | 4.12.2 |
| **django-filter** | Filtering | 23.3 |
| **Pillow** | Image Processing | 10.1.0 |
| **Gunicorn** | WSGI Server | 21.2.0 |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.8 or higher
- **PostgreSQL** 12 or higher
- **pip** (Python package manager)
- **Git** (for version control)
- **Virtual Environment** support

---

## 🚀 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/mini-cms-api.git
cd mini-cms-api
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup PostgreSQL Database

```bash
# Open PostgreSQL shell
psql -U postgres

# Run these SQL commands
CREATE DATABASE mini_cms_db;
CREATE USER cms_user WITH PASSWORD 'cms_password_123';
GRANT ALL PRIVILEGES ON DATABASE mini_cms_db TO cms_user;

# Connect and grant schema privileges
\c mini_cms_db
GRANT ALL ON SCHEMA public TO cms_user;
\q
```

### Step 5: Configure Environment Variables

Create `.env` file in project root:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
DB_NAME=mini_cms_db
DB_USER=cms_user
DB_PASSWORD=cms_password_123
DB_HOST=localhost
DB_PORT=5432
```

### Step 6: Run Migrations

```bash
python manage.py makemigrations accounts
python manage.py makemigrations articles
python manage.py makemigrations scraper
python manage.py migrate
```

### Step 7: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 8: Run Development Server

```bash
python manage.py runserver 127.0.0.1:1223
```

🎉 **Server is running!** Visit: `http://127.0.0.1:1223/`

---

## 🌐 API Endpoints

### 🏠 Homepage & Documentation

| Endpoint | Description | Access |
|----------|-------------|--------|
| **[http://127.0.0.1:1223/](http://127.0.0.1:1223/)** | API Root - Welcome page with all endpoints | Public |
| **[http://127.0.0.1:1223/swagger/](http://127.0.0.1:1223/swagger/)** | Interactive Swagger UI Documentation | Public |
| **[http://127.0.0.1:1223/redoc/](http://127.0.0.1:1223/redoc/)** | ReDoc API Documentation | Public |
| **[http://127.0.0.1:1223/admin-panal/](http://127.0.0.1:1223/admin-panal/)** | Django Admin Panel | Admin Only |

---

### 🔐 Authentication Endpoints

**Base URL:** `http://127.0.0.1:1223/api/auth/`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/register/` | Register new user (Admin/Author) | ❌ |
| `POST` | `/login/` | Login and get JWT tokens | ❌ |
| `POST` | `/token/refresh/` | Refresh access token | ❌ |
| `GET` | `/profile/` | Get current user profile | ✅ |
| `PATCH` | `/profile/` | Update user profile | ✅ |
| `POST` | `/change-password/` | Change password | ✅ |
| `POST` | `/logout/` | Logout (blacklist refresh token) | ✅ |

#### Example: Register User

```bash
POST http://127.0.0.1:1223/api/auth/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "password2": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "author"
}
```

#### Example: Login

```bash
POST http://127.0.0.1:1223/api/auth/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePass123"
}

# Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 🗂️ Category Endpoints

**Base URL:** `http://127.0.0.1:1223/api/categories/`

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| `GET` | `/` | List all categories | Public |
| `POST` | `/` | Create category | Admin Only |
| `GET` | `/{id}/` | Get category details | Public |
| `PUT` | `/{id}/` | Update category | Admin Only |
| `PATCH` | `/{id}/` | Partial update category | Admin Only |
| `DELETE` | `/{id}/` | Delete category | Admin Only |

#### Example: Create Category

```bash
POST http://127.0.0.1:1223/api/categories/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Technology",
  "description": "All about technology and innovation"
}
```

---

### 📝 Article Endpoints

**Base URL:** `http://127.0.0.1:1223/api/articles/`

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| `GET` | `/` | List published articles | Public |
| `POST` | `/` | Create article | Authenticated |
| `GET` | `/{id}/` | Get article details | Public (if published) |
| `PUT` | `/{id}/` | Update article | Author/Admin |
| `PATCH` | `/{id}/` | Partial update | Author/Admin |
| `DELETE` | `/{id}/` | Delete article | Author/Admin |
| `GET` | `/published/` | Get all published articles | Public |
| `GET` | `/drafts/` | Get draft articles | Author/Admin |
| `GET` | `/my_articles/` | Get user's own articles | Author |

#### Query Parameters

- `?page=1` - Page number
- `?page_size=10` - Items per page (max 100)
- `?status=published` - Filter by status
- `?category=1` - Filter by category ID
- `?author=1` - Filter by author ID
- `?search=django` - Search in title/description/content
- `?ordering=-created_at` - Order by field (prefix `-` for descending)

#### Example: Create Article

```bash
POST http://127.0.0.1:1223/api/articles/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Getting Started with Django",
  "description": "A comprehensive guide to Django",
  "content": "Django is a high-level Python web framework...",
  "category": 1,
  "status": "published"
}
```

#### Example: List Articles with Filters

```bash
GET http://127.0.0.1:1223/api/articles/?status=published&category=1&page=1&page_size=5&ordering=-views_count
```

---

### 🌐 Web Scraper Endpoints (Bonus)

**Base URL:** `http://127.0.0.1:1223/api/scraper/articles/`

| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| `GET` | `/` | List scraped articles | Public |
| `GET` | `/latest/` | Get latest scraped articles | Public |
| `POST` | `/scrape/` | Trigger article scraping | Admin Only |

#### Example: Trigger Scraping

```bash
POST http://127.0.0.1:1223/api/scraper/articles/scrape/
Authorization: Bearer {admin_access_token}
Content-Type: application/json

{
  "limit": 5
}

# Response:
{
  "scraped_count": 5,
  "articles": [...]
}
```

---

## ✅ Assessment Validation

### Automated Testing Script

Run the complete assessment test suite:

```bash
# Start server in one terminal
python manage.py runserver 127.0.0.1:1223

# Run tests in another terminal
python test_assessment.py
```

### What the Test Script Validates

The `test_assessment.py` script comprehensively tests all assignment requirements:

#### ✅ Step 1: User Registration
- Registers Admin user (`admin` / `Admin@123456`)
- Registers Author user (`john_doe` / `Author@123456`)
- Verifies users in database

#### ✅ Step 2: JWT Authentication
- Admin login with JWT tokens
- Author login with JWT tokens
- Token validation

#### ✅ Step 3: Category Management
- Admin creates 3 categories (Technology, Programming, Web Development)
- Verifies categories in database
- **Permission Test:** Author attempts to create category → 403 Forbidden ✅

#### ✅ Step 4: Article Management
- Admin creates published article
- Author creates draft article
- Author publishes their own article
- **Permission Test:** Author attempts to edit admin's article → 403 Forbidden ✅

#### ✅ Step 5: Public Access Control
- Public users see ONLY published articles
- Draft articles hidden from public
- Database verification

#### ✅ Step 6: Pagination
- Tests pagination with page_size parameter
- Verifies next/previous links

#### ✅ Step 7: Web Scraping (Bonus)
- **Permission Test:** Author attempts scraping → 403 Forbidden ✅
- Admin triggers scraping
- Verifies scraped articles in database

### Expected Test Results

```
============================================================
Assessment Results
============================================================

Total Steps: 13
Passed: 13 ✅
Failed: 0
Success Rate: 100.0%

🎉 ALL ASSESSMENT REQUIREMENTS MET! 🎉
Your CMS API is fully compliant with the assignment!
```

### Manual Testing via Swagger UI

Visit **[http://127.0.0.1:1223/swagger/](http://127.0.0.1:1223/swagger/)** for interactive API testing:

1. **Test Authentication**
   - Register user → `/api/auth/register/`
   - Login → `/api/auth/login/` (copy access token)
   - Click "Authorize" button, paste token: `Bearer {your_token}`

2. **Test Category Management**
   - Create category (requires Admin token)
   - List categories
   - Author token should get 403 on POST

3. **Test Article Management**
   - Create article (any authenticated user)
   - List articles (public)
   - Update own article
   - Try updating others' article (should fail)

4. **Test Permissions**
   - Public access → Only published articles
   - Author access → Own articles + published
   - Admin access → All articles

---

## 🗄️ Database Schema

### Users Table (`users`)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    role VARCHAR(10) NOT NULL,  -- 'admin' or 'author'
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    bio TEXT,
    profile_picture VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Categories Table (`categories`)

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Articles Table (`articles`)

```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    content TEXT NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    author_id INTEGER REFERENCES users(id),
    status VARCHAR(10) DEFAULT 'draft',  -- 'draft' or 'published'
    featured_image VARCHAR(100),
    views_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_created_at (created_at DESC),
    INDEX idx_status (status),
    INDEX idx_author (author_id)
);
```

### Scraped Articles Table (`scraper_scrappedarticle`)

```sql
CREATE TABLE scraper_scrappedarticle (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    source_url VARCHAR(500) UNIQUE NOT NULL,
    source VARCHAR(200),
    scraped_at TIMESTAMP DEFAULT NOW()
);
```

### Entity Relationship Diagram

```
┌──────────────┐         ┌──────────────┐
│    Users     │         │  Categories  │
├──────────────┤         ├──────────────┤
│ id (PK)      │         │ id (PK)      │
│ username     │         │ name         │
│ email        │         │ slug         │
│ password     │         │ description  │
│ role         │         │ created_at   │
│ first_name   │         └──────────────┘
│ last_name    │                │
│ bio          │                │
│ created_at   │                │
└──────────────┘                │
       │                        │
       │ 1:N                    │ 1:N
       │                        │
       │    ┌──────────────┐    │
       └───▶│   Articles   │◀───┘
            ├──────────────┤
            │ id (PK)      │
            │ title        │
            │ slug         │
            │ description  │
            │ content      │
            │ category_id  │ (FK)
            │ author_id    │ (FK)
            │ status       │
            │ views_count  │
            │ created_at   │
            └──────────────┘
```

---

## 🔐 Authentication

### JWT Token Flow

```
┌─────────┐                                    ┌─────────┐
│ Client  │                                    │  Server │
└────┬────┘                                    └────┬────┘
     │                                              │
     │  POST /api/auth/login/                      │
     │  { username, password }                     │
     │─────────────────────────────────────────────▶│
     │                                              │
     │                                              │ Validate credentials
     │                                              │
     │  { access, refresh }                        │
     │◀─────────────────────────────────────────────│
     │                                              │
     │  GET /api/articles/                         │
     │  Authorization: Bearer {access}             │
     │─────────────────────────────────────────────▶│
     │                                              │
     │                                              │ Verify token
     │                                              │
     │  { articles: [...] }                        │
     │◀─────────────────────────────────────────────│
     │                                              │
     │  POST /api/auth/token/refresh/              │
     │  { refresh }                                 │
     │─────────────────────────────────────────────▶│
     │                                              │
     │  { access }                                  │
     │◀─────────────────────────────────────────────│
     │                                              │
```

### Token Configuration

- **Access Token Lifetime:** 60 minutes
- **Refresh Token Lifetime:** 7 days
- **Algorithm:** HS256
- **Blacklist:** Enabled for logout

---

## 🛡️ Permissions

### Role-Based Access Control

| Feature | Public | Author | Admin |
|---------|--------|--------|-------|
| **Authentication** |
| Register | ✅ | ✅ | ✅ |
| Login | ✅ | ✅ | ✅ |
| View Profile | ❌ | ✅ | ✅ |
| **Categories** |
| List | ✅ | ✅ | ✅ |
| Create | ❌ | ❌ | ✅ |
| Update | ❌ | ❌ | ✅ |
| Delete | ❌ | ❌ | ✅ |
| **Articles** |
| List Published | ✅ | ✅ | ✅ |
| View Published | ✅ | ✅ | ✅ |
| Create | ❌ | ✅ | ✅ |
| Update Own | ❌ | ✅ | ✅ |
| Update Any | ❌ | ❌ | ✅ |
| Delete Own | ❌ | ✅ | ✅ |
| Delete Any | ❌ | ❌ | ✅ |
| View Drafts | ❌ | Own Only | All |
| **Web Scraping** |
| View Scraped | ✅ | ✅ | ✅ |
| Trigger Scrape | ❌ | ❌ | ✅ |

---

## 🧪 Testing

### Run Unit Tests

```bash
python manage.py test
```

### Test Coverage

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Manual API Testing

Use the provided Postman collection or Swagger UI:

1. Import `postman_collection.json`
2. Set environment variables
3. Run authentication requests
4. Test all endpoints

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use environment variables for secrets
- [ ] Configure allowed hosts
- [ ] Setup HTTPS/SSL certificates
- [ ] Use production database credentials
- [ ] Configure CORS headers
- [ ] Setup logging and monitoring
- [ ] Enable database backups
- [ ] Configure static/media file serving
- [ ] Setup caching (Redis)

### Environment Variables (Production)

```env
SECRET_KEY=your-production-secret-key-min-50-chars
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=production_db
DB_USER=production_user
DB_PASSWORD=strong-production-password
DB_HOST=your-db-host.com
DB_PORT=5432
```

### Deploy with Gunicorn

```bash
pip install gunicorn
gunicorn mini_cms.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## 📊 Performance Optimization

### Database Query Optimization

✅ **No N+1 Queries**
- All article queries use `select_related('author', 'category')`
- Category queries use `prefetch_related('articles')`

✅ **Indexing**
- Indexes on `created_at`, `status`, `author_id`
- Unique indexes on `slug` fields

✅ **Pagination**
- Configurable page sizes
- Efficient offset pagination

---

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
# Services → postgresql  # Windows

# Verify credentials
psql -U cms_user -d mini_cms_db -W
```

#### Port Already in Use
```bash
# Find process
netstat -ano | findstr :1223  # Windows
lsof -i :1223  # Linux/Mac

# Kill process
taskkill /PID <PID> /F  # Windows
kill -9 <PID>  # Linux/Mac
```

#### Migration Errors
```bash
# Reset migrations
python manage.py migrate --fake accounts zero
python manage.py migrate --fake articles zero

# Delete migration files (keep __init__.py)
# Recreate
python manage.py makemigrations
python manage.py migrate
```

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 👨‍💻 Author

<div align="center">

### **Mumtaz Ali**

[![GitHub](https://img.shields.io/badge/GitHub-engrmumtazali0112-181717?style=for-the-badge&logo=github)](https://github.com/engrmumtazali0112)
[![Email](https://img.shields.io/badge/Email-engrmumtazali01@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:engrmumtazali01@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/mumtazali12)

**Full-Stack Developer | Backend Specialist | Open Source Contributor**

</div>

---

## 📄 License

MIT License

Copyright (c) 2025 Mumtaz Ali

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 🙏 Acknowledgments

- Django REST Framework team for excellent documentation
- PostgreSQL community for robust database system
- All contributors and reviewers

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

**Made with ❤️ and ☕ by Mumtaz Ali**

[![GitHub followers](https://img.shields.io/github/followers/engrmumtazali0112?style=social)](https://github.com/engrmumtazali0112)
[![GitHub stars](https://img.shields.io/github/stars/engrmumtazali0112/mini-cms-api?style=social)](https://github.com/engrmumtazali0112/mini-cms-api)

</div>