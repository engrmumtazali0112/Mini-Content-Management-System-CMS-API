SELECT 
    a.id as article_id,
    a.title,
    a.slug,
    a.description,
    a.content,
    a.status,
    a.views_count,
    a.featured_image,
    u.id as author_id,
    u.username as author_username,
    u.email as author_email,
    u.role as author_role,
    c.id as category_id,
    c.name as category_name,
    c.slug as category_slug,
    a.created_at,
    a.updated_at
FROM articles a
JOIN users u ON a.author_id = u.id
JOIN categories c ON a.category_id = c.id
ORDER BY a.created_at DESC;