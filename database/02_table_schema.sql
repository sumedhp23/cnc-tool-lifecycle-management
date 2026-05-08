-- ========================================
-- 02A: TOOL LIFECYCLE REPORT SCHEMA
-- ========================================

SELECT 
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'cnc_app_toollifecyclereport'
ORDER BY ORDINAL_POSITION;



-- ========================================
-- 02B: DYNAMIC FIELD SCHEMA
-- ========================================

SELECT 
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'cnc_app_dynamicfield';



-- ========================================
-- 02C: FORM SUBMISSION SCHEMA
-- ========================================

SELECT 
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'cnc_app_formsubmission';