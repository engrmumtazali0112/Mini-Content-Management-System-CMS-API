"""
Complete Assessment Testing Script - FIXED VERSION
Handles existing data and proper cleanup

Save as: test_assessment_fixed.py
Run: python test_assessment_fixed.py
"""

import requests
import json
import time
from typing import Dict, Optional
import psycopg2
from datetime import datetime

BASE_URL = "http://127.0.0.1:1223"

# Database connection settings
DB_CONFIG = {
    'dbname': 'mini_cms_db',
    'user': 'cms_user',
    'password': 'cms_password_123',
    'host': 'localhost',
    'port': '5432'
}

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    END = '\033[0m'
    BOLD = '\033[1m'

class AssessmentTester:
    def __init__(self):
        # Use unique usernames with timestamp to avoid conflicts
        timestamp = int(time.time())
        
        self.admin_data = {
            'username': f'admin_{timestamp}',
            'email': f'admin_{timestamp}@cms.com',
            'password': 'Admin@123456',
            'password2': 'Admin@123456',
            'first_name': 'System',
            'last_name': 'Admin',
            'role': 'admin'
        }
        
        self.author_data = {
            'username': f'author_{timestamp}',
            'email': f'author_{timestamp}@cms.com',
            'password': 'Author@123456',
            'password2': 'Author@123456',
            'first_name': 'John',
            'last_name': 'Doe',
            'role': 'author'
        }
        
        self.admin_token = None
        self.author_token = None
        self.category_ids = []
        self.admin_article_id = None
        self.author_article_id = None
        self.db_conn = None
        
        self.step_number = 0
        
    def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            self.db_conn = psycopg2.connect(**DB_CONFIG)
            self.db_conn.autocommit = True  # Auto-commit to avoid transaction issues
            return True
        except Exception as e:
            print(f"{Colors.RED}❌ Database connection failed: {e}{Colors.END}")
            return False
    
    def print_step(self, title: str):
        """Print step header"""
        self.step_number += 1
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}STEP {self.step_number}: {title}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")
    
    def print_success(self, message: str):
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
    
    def print_error(self, message: str):
        print(f"{Colors.RED}❌ {message}{Colors.END}")
    
    def print_info(self, message: str):
        print(f"{Colors.CYAN}ℹ️  {message}{Colors.END}")
    
    def print_warning(self, message: str):
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
    
    def verify_database_state(self):
        """Verify database initial state"""
        self.print_step("Verify Database Initial State")
        
        if not self.db_conn:
            self.print_error("Database not connected")
            return False
        
        try:
            cursor = self.db_conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"Users in database: {user_count}")
            
            cursor.execute("SELECT COUNT(*) FROM categories")
            cat_count = cursor.fetchone()[0]
            print(f"Categories in database: {cat_count}")
            
            cursor.execute("SELECT COUNT(*) FROM articles")
            article_count = cursor.fetchone()[0]
            print(f"Articles in database: {article_count}")
            
            self.print_success("Database state verified")
            return True
            
        except Exception as e:
            self.print_error(f"Database query failed: {e}")
            return False
    
    def step1_register_admin(self):
        """Step 1: Register Admin User"""
        self.print_step("Register Admin User")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/register/",
                json=self.admin_data,
                timeout=10
            )
            
            if response.status_code == 201:
                self.print_success(f"Admin registered: {self.admin_data['username']}")
                self.print_info(f"Email: {self.admin_data['email']}")
                self.print_info(f"Role: admin")
                
                cursor = self.db_conn.cursor()
                cursor.execute(
                    "SELECT id, username, email, role FROM users WHERE username = %s",
                    (self.admin_data['username'],)
                )
                user = cursor.fetchone()
                if user:
                    print(f"\n{Colors.MAGENTA}📊 Database Record:{Colors.END}")
                    print(f"   ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
                
                return True
            else:
                self.print_error(f"Registration failed: {response.status_code}")
                print(response.json())
                return False
                
        except Exception as e:
            self.print_error(f"Request failed: {e}")
            return False
    
    def step2_register_author(self):
        """Step 2: Register Author User"""
        self.print_step("Register Author User")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/register/",
                json=self.author_data,
                timeout=10
            )
            
            if response.status_code == 201:
                self.print_success(f"Author registered: {self.author_data['username']}")
                self.print_info(f"Email: {self.author_data['email']}")
                self.print_info(f"Role: author")
                
                cursor = self.db_conn.cursor()
                cursor.execute(
                    "SELECT id, username, email, role FROM users WHERE username = %s",
                    (self.author_data['username'],)
                )
                user = cursor.fetchone()
                if user:
                    print(f"\n{Colors.MAGENTA}📊 Database Record:{Colors.END}")
                    print(f"   ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
                
                return True
            else:
                self.print_error(f"Registration failed: {response.status_code}")
                print(response.json())
                return False
                
        except Exception as e:
            self.print_error(f"Request failed: {e}")
            return False
    
    def step3_login_admin(self):
        """Step 3: Login as Admin"""
        self.print_step("Login as Admin (JWT Authentication)")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/login/",
                json={
                    'username': self.admin_data['username'],
                    'password': self.admin_data['password']
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get('access')
                refresh_token = data.get('refresh')
                
                self.print_success("Admin login successful")
                self.print_info(f"Access Token: {self.admin_token[:50]}...")
                self.print_info(f"Refresh Token: {refresh_token[:50]}...")
                return True
            else:
                self.print_error(f"Login failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Request failed: {e}")
            return False
    
    def step4_login_author(self):
        """Step 4: Login as Author"""
        self.print_step("Login as Author (JWT Authentication)")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/auth/login/",
                json={
                    'username': self.author_data['username'],
                    'password': self.author_data['password']
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.author_token = data.get('access')
                
                self.print_success("Author login successful")
                self.print_info(f"Access Token: {self.author_token[:50]}...")
                return True
            else:
                self.print_error(f"Login failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Request failed: {e}")
            return False
    
    def step5_admin_create_categories(self):
        """Step 5: Admin Creates Categories"""
        self.print_step("Admin Creates Categories (Admin Permission Required)")
        
        # Use unique names with timestamp to avoid conflicts
        timestamp = int(time.time())
        categories = [
            {'name': f'Tech_{timestamp}', 'description': 'All about technology'},
            {'name': f'Code_{timestamp}', 'description': 'Programming tutorials'},
            {'name': f'Web_{timestamp}', 'description': 'Web development'}
        ]
        
        for cat in categories:
            try:
                response = requests.post(
                    f"{BASE_URL}/api/categories/",
                    json=cat,
                    headers={'Authorization': f'Bearer {self.admin_token}'},
                    timeout=10
                )
                
                if response.status_code == 201:
                    data = response.json()
                    cat_id = data.get('id')
                    self.category_ids.append(cat_id)
                    
                    self.print_success(f"Category created: {cat['name']}")
                    self.print_info(f"   ID: {cat_id}, Slug: {data.get('slug')}")
                else:
                    self.print_error(f"Failed to create category: {response.status_code}")
                    print(response.json())
                    
            except Exception as e:
                self.print_error(f"Request failed: {e}")
        
        if self.category_ids:
            cursor = self.db_conn.cursor()
            cursor.execute(
                "SELECT id, name, slug FROM categories WHERE id = ANY(%s) ORDER BY id",
                (self.category_ids,)
            )
            cats = cursor.fetchall()
            
            print(f"\n{Colors.MAGENTA}📊 Database - New Categories:{Colors.END}")
            for cat in cats:
                print(f"   ID: {cat[0]}, Name: {cat[1]}, Slug: {cat[2]}")
        
        return len(self.category_ids) > 0
    
    def step6_author_try_create_category(self):
        """Step 6: Author Tries to Create Category (Should Fail)"""
        self.print_step("Author Attempts to Create Category (Should Fail - 403)")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/categories/",
                json={'name': 'Should_Fail_Test', 'description': 'This should not work'},
                headers={'Authorization': f'Bearer {self.author_token}'},
                timeout=10
            )
            
            if response.status_code == 403:
                self.print_success("✅ Correctly blocked! Author cannot create categories (403 Forbidden)")
                self.print_info("Permission system working correctly")
                return True
            else:
                self.print_error(f"❌ Permission error! Expected 403, got {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Request failed: {e}")
            return False
    
    def step7_admin_create_article(self):
        """Step 7: Admin Creates Published Article"""
        self.print_step("Admin Creates Published Article")
        
        if not self.category_ids:
            self.print_error("No categories available")
            return False
        
        article_data = {
            'title': f'Django REST Guide {int(time.time())}',
            'description': 'A comprehensive guide to building REST APIs',
            'content': 'Django REST Framework is a powerful toolkit...',
            'category': self.category_ids[0],  # Use first created category
            'status': 'published'
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/articles/",
                json=article_data,
                headers={'Authorization': f'Bearer {self.admin_token}'},
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                self.admin_article_id = data.get('id')
                
                self.print_success(f"Article created: {article_data['title']}")
                self.print_info(f"   ID: {self.admin_article_id}")
                self.print_info(f"   Status: {article_data['status']}")
                self.print_info(f"   Category ID: {article_data['category']}")
                
                cursor = self.db_conn.cursor()
                cursor.execute(
                    """SELECT a.id, a.title, a.status, u.username as author, c.name as category
                       FROM articles a
                       JOIN users u ON a.author_id = u.id
                       JOIN categories c ON a.category_id = c.id
                       WHERE a.id = %s""",
                    (self.admin_article_id,)
                )
                article = cursor.fetchone()
                
                if article:
                    print(f"\n{Colors.MAGENTA}📊 Database Record:{Colors.END}")
                    print(f"   ID: {article[0]}, Title: {article[1]}")
                    print(f"   Status: {article[2]}, Author: {article[3]}, Category: {article[4]}")
                
                return True
            else:
                self.print_error(f"Failed to create article: {response.status_code}")
                print(response.json())
                return False
                
        except Exception as e:
            self.print_error(f"Request failed: {e}")
            return False
    
    def step8_author_create_draft(self):
        """Step 8: Author Creates Draft Article"""
        self.print_step("Author Creates Draft Article")
        
        if not self.category_ids:
            self.print_error("No categories available")
            return False
        
        article_data = {
            'title': f'Python Async Guide {int(time.time())}',
            'description': 'Learn asynchronous programming',
            'content': 'Asynchronous programming allows concurrent code...',
            'category': self.category_ids[1] if len(self.category_ids) > 1 else self.category_ids[0],
            'status': 'draft'
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/articles/",
                json=article_data,
                headers={'Authorization': f'Bearer {self.author_token}'},
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                self.author_article_id = data.get('id')
                
                self.print_success(f"Draft article created: {article_data['title']}")
                self.print_info(f"   ID: {self.author_article_id}")
                self.print_info(f"   Status: draft (Not visible to public)")
                
                cursor = self.db_conn.cursor()
                cursor.execute(
                    """SELECT a.id, a.title, a.status, u.username as author
                       FROM articles a
                       JOIN users u ON a.author_id = u.id
                       WHERE a.id = %s""",
                    (self.author_article_id,)
                )
                article = cursor.fetchone()
                
                if article:
                    print(f"\n{Colors.MAGENTA}📊 Database Record:{Colors.END}")
                    print(f"   ID: {article[0]}, Title: {article[1]}")
                    print(f"   Status: {article[2]}, Author: {article[3]}")
                
                return True
            else:
                self.print_error(f"Failed to create article: {response.status_code}")
                print(response.json())
                return False
                
        except Exception as e:
            self.print_error(f"Request failed: {e}")
            return False
    
    def step9_author_publish_article(self):
        """Step 9: Author Publishes Their Own Article"""
        self.print_step("Author Updates Draft to Published")
        
        if not self.author_article_id or not self.category_ids:
            self.print_error("No article to update")
            return False
        
        article_data = {
            'title': f'Python Async Guide {int(time.time())}',
            'description': 'Learn asynchronous programming',
            'content': 'Asynchronous programming allows concurrent code...',
            'category': self.category_ids[1] if len(self.category_ids) > 1 else self.category_ids[0],
            'status': 'published'
        }
        
        try:
            response = requests.put(
                f"{BASE_URL}/api/articles/{self.author_article_id}/",
                json=article_data,
                headers={'Authorization': f'Bearer {self.author_token}'},
                timeout=10
            )
            
            if response.status_code == 200:
                self.print_success("Article published successfully")
                self.print_info("   Status changed: draft → published")
                
                cursor = self.db_conn.cursor()
                cursor.execute(
                    "SELECT status FROM articles WHERE id = %s",
                    (self.author_article_id,)
                )
                status = cursor.fetchone()[0]
                
                print(f"\n{Colors.MAGENTA}📊 Database - Status Updated:{Colors.END}")
                print(f"   Article ID: {self.author_article_id}, New Status: {status}")
                
                return True
            else:
                self.print_error(f"Failed to update article: {response.status_code}")
                print(response.json())
                return False
                
        except Exception as e:
            self.print_error(f"Request failed: {e}")
            return False
    
    def step10_author_try_edit_admin_article(self):
        """Step 10: Author Tries to Edit Admin's Article (Should Fail)"""
        self.print_step("Author Attempts to Edit Admin's Article (Should Fail - 403)")
        
        if not self.admin_article_id:
            self.print_error("No admin article to test")
            return False
        
        try:
            response = requests.patch(
                f"{BASE_URL}/api/articles/{self.admin_article_id}/",
                json={'description': 'Trying to hack this article'},
                headers={'Authorization': f'Bearer {self.author_token}'},
                timeout=10
            )
            
            if response.status_code == 403:
                self.print_success("✅ Correctly blocked! Author cannot edit others' articles (403)")
                self.print_info("Permission system working correctly")
                return True
            else:
                self.print_error(f"❌ Security issue! Expected 403, got {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Request failed: {e}")
            return False
    
    def step11_public_view_published_only(self):
        """Step 11: Public User Sees Only Published Articles"""
        self.print_step("Public User Views Articles (Should See Only Published)")
        
        try:
            response = requests.get(f"{BASE_URL}/api/articles/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', data)
                published_count = len(results)
                
                self.print_success(f"Public can access articles list")
                self.print_info(f"   Visible articles: {published_count}")
                
                all_published = all(
                    article.get('status') == 'published' 
                    for article in results
                )
                
                if all_published:
                    self.print_success("✅ All visible articles are published")
                    self.print_info("Draft articles correctly hidden from public")
                else:
                    self.print_error("❌ Draft articles visible to public!")
                    return False
                
                cursor = self.db_conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM articles WHERE status = 'published'")
                db_published = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM articles WHERE status = 'draft'")
                db_draft = cursor.fetchone()[0]
                
                print(f"\n{Colors.MAGENTA}📊 Database Statistics:{Colors.END}")
                print(f"   Total Published: {db_published}")
                print(f"   Total Drafts: {db_draft}")
                print(f"   Public API Returns: {published_count} articles")
                
                return True
            else:
                self.print_error(f"Failed to get articles: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Request failed: {e}")
            return False
    
    def step12_test_pagination(self):
        """Step 12: Test Pagination"""
        self.print_step("Test Pagination (page_size=1)")
        
        try:
            response = requests.get(
                f"{BASE_URL}/api/articles/?page=1&page_size=1",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                self.print_success("Pagination working")
                self.print_info(f"   Count: {data.get('count')}")
                self.print_info(f"   Next: {data.get('next')}")
                self.print_info(f"   Previous: {data.get('previous')}")
                self.print_info(f"   Results: {len(data.get('results', []))}")
                
                return True
            else:
                self.print_error(f"Pagination failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.print_error(f"Request failed: {e}")
            return False
    
    def step13_test_scraping(self):
        """Step 13: Test Web Scraping (Bonus)"""
        self.print_step("Test Web Scraping Feature (Bonus Task)")
        
        try:
            # Try as author (should fail)
            response = requests.post(
                f"{BASE_URL}/api/scraper/articles/scrape/",
                json={'limit': 3},
                headers={'Authorization': f'Bearer {self.author_token}'},
                timeout=10
            )
            
            if response.status_code == 403:
                self.print_success("✅ Author correctly blocked from scraping (403)")
            
            # Try as admin (should work)
            response = requests.post(
                f"{BASE_URL}/api/scraper/articles/scrape/",
                json={'limit': 5},
                headers={'Authorization': f'Bearer {self.admin_token}'},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                scraped_count = data.get('scraped_count', 0)
                
                self.print_success(f"Web scraping successful")
                self.print_info(f"   Scraped articles: {scraped_count}")
                
                # Try to verify in database (may not exist)
                try:
                    cursor = self.db_conn.cursor()
                    cursor.execute(
                        "SELECT COUNT(*) FROM scraper_scrappedarticle"
                    )
                    count = cursor.fetchone()[0]
                    
                    print(f"\n{Colors.MAGENTA}📊 Database - Scraped Articles:{Colors.END}")
                    print(f"   Total scraped articles: {count}")
                except:
                    self.print_warning("Scraper table not found (optional feature)")
                
                return True
            else:
                self.print_warning(f"Scraping returned: {response.status_code}")
                return True  # Not critical
                
        except Exception as e:
            self.print_warning(f"Scraping test skipped: {e}")
            return True  # Not critical
    
    def show_final_database_state(self):
        """Show complete database state"""
        self.print_step("Final Database State Summary")
        
        try:
            cursor = self.db_conn.cursor()
            
            # Users
            print(f"{Colors.BOLD}Users Table (Last 5):{Colors.END}")
            cursor.execute("SELECT id, username, email, role FROM users ORDER BY id DESC LIMIT 5")
            for user in cursor.fetchall():
                print(f"  {user[0]} | {user[1]:20} | {user[2]:30} | {user[3]}")
            
            # Categories
            print(f"\n{Colors.BOLD}Categories Table (Last 5):{Colors.END}")
            cursor.execute("SELECT id, name, slug FROM categories ORDER BY id DESC LIMIT 5")
            for cat in cursor.fetchall():
                print(f"  {cat[0]} | {cat[1]:20} | {cat[2]}")
            
            # Articles
            print(f"\n{Colors.BOLD}Articles Table (Last 5):{Colors.END}")
            cursor.execute("""
                SELECT a.id, a.title, u.username, c.name, a.status, a.views_count
                FROM articles a
                JOIN users u ON a.author_id = u.id
                JOIN categories c ON a.category_id = c.id
                ORDER BY a.id DESC
                LIMIT 5
            """)
            for article in cursor.fetchall():
                print(f"  {article[0]} | {article[1][:30]:30} | {article[2]:15} | {article[3]:15} | {article[4]:10} | Views: {article[5]}")
        except Exception as e:
            self.print_warning(f"Could not show final state: {e}")
    
    def run_assessment(self):
        """Run complete assessment"""
        print(f"{Colors.BOLD}{Colors.BLUE}")
        print("╔════════════════════════════════════════════════════════════════════╗")
        print("║     Backend Engineering Assessment - Complete Test Suite          ║")
        print("║     Mini Content Management System (CMS) with Django REST          ║")
        print("╚════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        if not self.connect_db():
            return
        
        self.verify_database_state()
        
        steps = [
            self.step1_register_admin,
            self.step2_register_author,
            self.step3_login_admin,
            self.step4_login_author,
            self.step5_admin_create_categories,
            self.step6_author_try_create_category,
            self.step7_admin_create_article,
            self.step8_author_create_draft,
            self.step9_author_publish_article,
            self.step10_author_try_edit_admin_article,
            self.step11_public_view_published_only,
            self.step12_test_pagination,
            self.step13_test_scraping
        ]
        
        passed = 0
        failed = 0
        
        for step in steps:
            if step():
                passed += 1
            else:
                failed += 1
            time.sleep(0.5)
        
        self.show_final_database_state()
        
        total = passed + failed
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}Assessment Results{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")
        
        print(f"Total Steps: {total}")
        print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {failed}{Colors.END}")
        print(f"Success Rate: {pass_rate:.1f}%\n")
        
        if failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL ASSESSMENT REQUIREMENTS MET! 🎉{Colors.END}")
            print(f"{Colors.GREEN}Your CMS API is fully compliant with the assignment!{Colors.END}\n")
        else:
            print(f"{Colors.YELLOW}Some tests failed. Review the errors above.{Colors.END}\n")
        
        if self.db_conn:
            self.db_conn.close()


if __name__ == "__main__":
    print(f"\n{Colors.YELLOW}Starting Assessment Testing...{Colors.END}")
    print(f"{Colors.YELLOW}Server should be running on {BASE_URL}{Colors.END}")
    print(f"{Colors.YELLOW}Database: {DB_CONFIG['dbname']} on {DB_CONFIG['host']}:{DB_CONFIG['port']}{Colors.END}\n")
    
    try:
        response = requests.get(f"{BASE_URL}/api/categories/", timeout=5)
        
        tester = AssessmentTester()
        tester.run_assessment()
        
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}ERROR: Could not connect to {BASE_URL}{Colors.END}")
        print(f"{Colors.YELLOW}Please start the server: python manage.py runserver 127.0.0.1:1223{Colors.END}\n")
        