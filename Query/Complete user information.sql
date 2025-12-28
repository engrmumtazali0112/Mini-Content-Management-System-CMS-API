SELECT current_database(), current_user, inet_server_addr(), inet_server_port();

-- Complete user information
SELECT * FROM users ORDER BY created_at DESC;

SELECT 
    id,
    username,
    email,
    role,
    first_name,
    last_name,
    is_active,
    is_staff,
    is_superuser,
    created_at,
    updated_at
FROM users 
ORDER BY created_at DESC;

SELECT 
    c.id,
    c.name,
    c.slug,
    c.description,
    COUNT(a.id) as total_articles,
    COUNT(CASE WHEN a.status = 'published' THEN 1 END) as published_articles,
    COUNT(CASE WHEN a.status = 'draft' THEN 1 END) as draft_articles,
    c.created_at,
    c.updated_at
FROM categories c
LEFT JOIN articles a ON c.id = a.category_id
GROUP BY c.id, c.name, c.slug, c.description, c.created_at, c.updated_at
ORDER BY total_articles DESC;