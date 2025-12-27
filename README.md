# Mini Content Management System (CMS) API

A robust REST API built with Django REST Framework and PostgreSQL for managing articles, categories, and users with JWT authentication.

## 🚀 Features

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Admin and Author roles with specific permissions
- **Article Management**: Full CRUD operations with draft/published status
- **Category Management**: Organized content categorization
- **Web Scraping**: Automated article scraping from popular tech blogs
- **Pagination**: Efficient data loading with customizable page sizes
- **Filtering & Search**: Advanced filtering and search capabilities
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **Optimized Queries**: No N+1 query issues with select_related and prefetch_related

## 📋 Requirements

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mini-cms-api.git
cd mini-cms-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database

```bash
# Access PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE mini_cms_db;
CREATE USER cms_user WITH PASSWORD 'cms_password_123';
GRANT ALL PRIVILEGES ON DATABASE mini_cms_db TO cms_user;
\q
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
DB_NAME=mini_cms_db
DB_USER=cms_user
DB_PASSWORD=cms_password_123
DB_HOST=localhost
DB_PORT=5432
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Create Sample Data (Optional)

```bash
python manage.py create_sample_data
```

This creates:
- Admin user: `admin` / `admin123`
- Author 1: `john_doe` / `author123`
- Author 2: `jane_smith` / `author123`
- 5 categories
- 6 sample articles

### 9. Run Development Server

```bash
python manage.py runserver
```

Access the API at `http://127.0.0.1:8000/`

## 📚 API Documentation

### Interactive Documentation

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **Admin Panel**: http://127.0.0.1:8000/admin/

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "author"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}

Response:
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "your-refresh-token"
}
```

#### Get Profile
```http
GET /api/auth/profile/
Authorization: Bearer your-access-token
```

#### Update Profile
```http
PATCH /api/auth/profile/
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "first_name": "Updated",
    "bio": "My updated bio"
}
```

#### Change Password
```http
POST /api/auth/change-password/
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "old_password": "oldpass123",
    "new_password": "newpass123"
}
```

#### Logout
```http
POST /api/auth/logout/
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "refresh_token": "your-refresh-token"
}
```

### Category Endpoints

#### List Categories
```http
GET /api/categories/
```

#### Create Category (Admin only)
```http
POST /api/categories/
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "name": "New Category",
    "description": "Category description"
}
```

#### Get Category Detail
```http
GET /api/categories/{id}/
```

#### Update Category (Admin only)
```http
PUT /api/categories/{id}/
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "name": "Updated Category",
    "description": "Updated description"
}
```

#### Delete Category (Admin only)
```http
DELETE /api/categories/{id}/
Authorization: Bearer your-access-token
```

### Article Endpoints

#### List Articles (Public - only published)
```http
GET /api/articles/

Query Parameters:
- page: Page number
- page_size: Items per page (max 100)
- status: draft or published
- category: Category ID
- author: Author ID
- search: Search in title, description, content
- ordering: -created_at, title, views_count, etc.
```

#### Get Published Articles
```http
GET /api/articles/published/
```

#### Get My Articles (Author)
```http
GET /api/articles/my_articles/
Authorization: Bearer your-access-token
```

#### Get Draft Articles (Author/Admin)
```http
GET /api/articles/drafts/
Authorization: Bearer your-access-token
```

#### Create Article (Authenticated)
```http
POST /api/articles/
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "title": "My New Article",
    "description": "Article description",
    "content": "Full article content...",
    "category": 1,
    "status": "draft"
}
```

#### Get Article Detail
```http
GET /api/articles/{id}/
```

#### Update Article (Author/Admin)
```http
PUT /api/articles/{id}/
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "title": "Updated Title",
    "description": "Updated description",
    "content": "Updated content...",
    "category": 1,
    "status": "published"
}
```

#### Delete Article (Author/Admin)
```http
DELETE /api/articles/{id}/
Authorization: Bearer your-access-token
```

### Scraper Endpoints

#### List Scraped Articles
```http
GET /api/scraper/articles/
```

#### Get Latest Scraped Articles
```http
GET /api/scraper/articles/latest/?limit=10
```

#### Trigger Scraping (Admin only)
```http
POST /api/scraper/articles/scrape/
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "limit": 5
}
```

## 🔧 Management Commands

### Create Sample Data
```bash
python manage.py create_sample_data
```

### Run Web Scraper
```bash
python manage.py scrape_articles --limit 5
```

## 🏗️ Project Structure

```
mini_cms_project/
├── mini_cms/              # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/              # User authentication app
│   ├── models.py         # Custom User model
│   ├── serializers.py    # User serializers
│   ├── views.py          # Auth views
│   └── urls.py
├── articles/              # Articles management app
│   ├── models.py         # Article and Category models
│   ├── serializers.py    # Article serializers
│   ├── views.py          # Article views
│   ├── permissions.py    # Custom permissions
│   ├── filters.py        # Filter classes
│   ├── pagination.py     # Pagination classes
│   └── urls.py
├── scraper/               # Web scraping app
│   ├── models.py         # ScrapedArticle model
│   ├── scraper.py        # Scraping logic
│   ├── views.py          # Scraper views
│   └── urls.py
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 📊 Database Schema

### Users Table
- id (PK)
- username (unique)
- email
- password
- role (admin/author)
- first_name, last_name
- bio
- profile_picture
- created_at, updated_at

### Categories Table
- id (PK)
- name (unique)
- slug (unique)
- description
- created_at, updated_at

### Articles Table
- id (PK)
- title
- slug (unique)
- description
- content
- category_id (FK)
- author_id (FK)
- status (draft/published)
- featured_image
- views_count
- created_at, updated_at

### Scraped Articles Table
- id (PK)
- title
- url (unique)
- source
- scraped_at

## 🔐 Permissions

### Admin
- Full access to all features
- Can create, update, delete categories
- Can create, update, delete any article
- Can trigger web scraping

### Author
- Can create articles
- Can update/delete only their own articles
- Can view all published articles
- Can view their own draft articles

### Public/Unauthenticated
- Can view published articles only
- Can view categories
- Cannot create, update, or delete content

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📝 API Response Format

### Success Response
```json
{
    "id": 1,
    "title": "Article Title",
    "description": "Article description",
    "status": "published",
    "created_at": "2024-01-01T12:00:00Z"
}
```

### Error Response
```json
{
    "detail": "Error message",
    "errors": {
        "field_name": ["Error description"]
    }
}
```

### Paginated Response
```json
{
    "count": 50,
    "next": "http://api.example.com/articles/?page=2",
    "previous": null,
    "results": [...]
}
```

## 🚀 Deployment

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com
DB_NAME=production_db
DB_USER=production_user
DB_PASSWORD=strong-password
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### Run with Gunicorn
```bash
pip install gunicorn
gunicorn mini_cms.wsgi:application --bind 0.0.0.0:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Your Name - [GitHub Profile](https://github.com/yourusername)

## 🙏 Acknowledgments

- Django REST Framework documentation
- PostgreSQL documentation
- BeautifulSoup documentation
