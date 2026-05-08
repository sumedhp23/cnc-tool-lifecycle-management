#!/bin/bash
# wait for SQL Server to come up
echo "Waiting for SQL Server to be ready..."
sleep 15

# Run the setup scripts sequentially
echo "Running database initialization scripts..."
/opt/mssql-tools/bin/sqlcmd -S db -U sa -P $SA_PASSWORD -i /scripts/01_tables_overview.sql
/opt/mssql-tools/bin/sqlcmd -S db -U sa -P $SA_PASSWORD -i /scripts/02_table_schema.sql
/opt/mssql-tools/bin/sqlcmd -S db -U sa -P $SA_PASSWORD -i /scripts/03_sample_data.sql
/opt/mssql-tools/bin/sqlcmd -S db -U sa -P $SA_PASSWORD -i /scripts/04_relationships.sql
/opt/mssql-tools/bin/sqlcmd -S db -U sa -P $SA_PASSWORD -i /scripts/05_dynamic_fields_analysis.sql
/opt/mssql-tools/bin/sqlcmd -S db -U sa -P $SA_PASSWORD -i /scripts/06_data_quality_checks.sql
/opt/mssql-tools/bin/sqlcmd -S db -U sa -P $SA_PASSWORD -i /scripts/07_total_reports.sql

echo "Database initialization complete."
