-- ========================================
-- 01: LIST ALL TABLES IN DATABASE
-- ========================================
-- Shows all tables created by Django and your app

SELECT 
    TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;