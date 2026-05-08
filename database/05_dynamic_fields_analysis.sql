-- ========================================
-- 05: COUNT VALUES PER DYNAMIC FIELD
-- ========================================

SELECT 
    f.field_name,
    COUNT(fs.id) AS total_entries

FROM cnc_app_dynamicfield f

LEFT JOIN cnc_app_formsubmission fs
    ON f.id = fs.field_id

GROUP BY f.field_name
ORDER BY total_entries DESC;