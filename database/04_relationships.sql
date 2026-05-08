-- ========================================
-- 04: JOIN STATIC + DYNAMIC DATA
-- ========================================

SELECT 
    r.serial_no,
    r.tool_no,
    r.stage,
    f.field_name,
    fs.value

FROM cnc_app_toollifecyclereport r

LEFT JOIN cnc_app_formsubmission fs
    ON r.serial_no = fs.report_id

LEFT JOIN cnc_app_dynamicfield f
    ON fs.field_id = f.id

ORDER BY r.serial_no DESC;