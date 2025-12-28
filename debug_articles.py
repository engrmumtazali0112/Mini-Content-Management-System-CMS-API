"""
Debug script to test article creation and retrieval
Save as: debug_articles.py
Run: python debug_articles.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:1223"

def test_author_workflow():
    print("=" * 70)
    print("TESTING AUTHOR ARTICLE WORKFLOW")
    print("=" * 70)
    
    # Step 1: Login as author
    print("\n1. Logging in as author...")
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login/",
        json={"username": "john_doe", "password": "author123"}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return
    
    token = login_response.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    print(f"✅ Login successful! Token: {token[:30]}...")
    
    # Step 2: Get categories
    print("\n2. Fetching categories...")
    cat_response = requests.get(f"{BASE_URL}/api/categories/")
    categories = cat_response.json()
    
    if not categories:
        print("❌ No categories found!")
        return
    
    category_id = categories[0]['id']
    print(f"✅ Using category: {categories[0]['name']} (ID: {category_id})")
    
    # Step 3: Create draft article
    print("\n3. Creating draft article...")
    article_data = {
        "title": "Test Draft Article",
        "description": "This is a test draft",
        "content": "Full content of the test article",
        "category": category_id,
        "status": "draft"
    }
    
    create_response = requests.post(
        f"{BASE_URL}/api/articles/",
        json=article_data,
        headers=headers
    )
    
    if create_response.status_code != 201:
        print(f"❌ Article creation failed: {create_response.status_code}")
        print(create_response.text)
        return
    
    article = create_response.json()
    article_id = article['id']
    print(f"✅ Article created successfully!")
    print(f"   ID: {article_id}")
    print(f"   Title: {article.get('title', 'N/A')}")
    print(f"   Status: {article.get('status', 'N/A')}")
    
    # Step 4: Try to retrieve the article
    print(f"\n4. Retrieving article {article_id}...")
    get_response = requests.get(
        f"{BASE_URL}/api/articles/{article_id}/",
        headers=headers
    )
    
    print(f"   Status Code: {get_response.status_code}")
    
    if get_response.status_code == 200:
        article_detail = get_response.json()
        print(f"✅ Article retrieved successfully!")
        print(f"   Title: {article_detail['title']}")
        print(f"   Author: {article_detail['author']['username']}")
        print(f"   Status: {article_detail['status']}")
        print(f"   Views: {article_detail['views_count']}")
    else:
        print(f"❌ Failed to retrieve article!")
        print(f"   Response: {get_response.text}")
    
    # Step 5: Try to update the article
    print(f"\n5. Updating article {article_id}...")
    update_data = {
        "title": "Updated Test Article",
        "description": "Updated description",
        "content": "Updated content",
        "category": category_id,
        "status": "published"
    }
    
    update_response = requests.put(
        f"{BASE_URL}/api/articles/{article_id}/",
        json=update_data,
        headers=headers
    )
    
    print(f"   Status Code: {update_response.status_code}")
    
    if update_response.status_code == 200:
        updated_article = update_response.json()
        print(f"✅ Article updated successfully!")
        print(f"   New Title: {updated_article.get('title', 'N/A')}")
        print(f"   New Status: {updated_article.get('status', 'N/A')}")
    else:
        print(f"❌ Failed to update article!")
        print(f"   Response: {update_response.text}")
    
    # Step 6: List author's articles
    print("\n6. Listing author's articles...")
    my_articles_response = requests.get(
        f"{BASE_URL}/api/articles/my_articles/",
        headers=headers
    )
    
    if my_articles_response.status_code == 200:
        my_articles = my_articles_response.json()
        total = my_articles.get('count', len(my_articles))
        print(f"✅ Found {total} article(s) by this author")
        
        results = my_articles.get('results', my_articles)
        for i, art in enumerate(results[:3], 1):
            print(f"   {i}. {art['title']} (ID: {art['id']}, Status: {art['status']})")
    else:
        print(f"❌ Failed to list articles: {my_articles_response.status_code}")
        print(f"   Response: {my_articles_response.text}")
    
    # Step 7: Cleanup - delete the test article
    print(f"\n7. Cleaning up - deleting article {article_id}...")
    delete_response = requests.delete(
        f"{BASE_URL}/api/articles/{article_id}/",
        headers=headers
    )
    
    print(f"   Status Code: {delete_response.status_code}")
    
    if delete_response.status_code == 204:
        print(f"✅ Article deleted successfully!")
    else:
        print(f"❌ Failed to delete article!")
        print(f"   Response: {delete_response.text}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    try:
        test_author_workflow()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to server")
        print("   Make sure server is running: python manage.py runserver 127.0.0.1:1223")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()