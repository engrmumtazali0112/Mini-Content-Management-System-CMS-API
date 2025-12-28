-- Users
SELECT 'USERS' as table_name, COUNT(*) as row_count FROM users
UNION ALL
-- Categories
SELECT 'CATEGORIES', COUNT(*) FROM categories
UNION ALL
-- Articles
SELECT 'ARTICLES', COUNT(*) FROM articles
UNION ALL
-- Scraped Articles
SELECT 'SCRAPED_ARTICLES', COUNT(*) FROM scraper_scrapedarticle;