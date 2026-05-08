-- ========================================
-- 06A: CHECK MISSING ACTUAL LIFE
-- ========================================

SELECT *
FROM cnc_app_toollifecyclereport
WHERE actual_life IS NULL;



-- ========================================
-- 06B: DUPLICATE CHECK
-- ========================================

SELECT 
    tool_no,
    machine_number,
    batch_no,
    COUNT(*) as count

FROM cnc_app_toollifecyclereport

GROUP BY tool_no, machine_number, batch_no
HAVING COUNT(*) > 1;