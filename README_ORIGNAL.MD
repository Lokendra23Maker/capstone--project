 # Northwind SQLite3 Data Analytics Project

## Project Overview

This project uses the Northwind SQLite database to perform SQL querying, joins, referential integrity validation, CSV export, and data cleaning using Python (Pandas).

---

# Objectives

- Explore the Northwind SQLite database.
- Execute SQL queries for data retrieval.
- Perform INNER JOIN and LEFT JOIN operations.
- Validate database relationships.
- Export SQL query results into CSV format.
- Clean exported data using Python (Pandas).
- Document the complete workflow.

---

# Task 1 - Database Setup

- Connected to the Northwind SQLite database.
- Verified database schema.
- Enabled foreign key support using:

sql
PRAGMA foreign_keys = ON;


---

# Task 2 - SQL Filtering

Performed SQL queries using:

- WHERE
- NOT IN
- BETWEEN
- ORDER BY ASC

---

# Task 3 - Aggregation

Performed aggregation queries using:

- GROUP BY
- HAVING
- COUNT()

---

# Task 4 - SQL Joins

Implemented the following joins:

### INNER JOIN

Returned only customers who have matching orders.

### LEFT JOIN

Returned all customers including customers without orders.

Exported the JOIN result into:

*task4_join_result.csv*

---

# Task 5 - Referential Integrity Validation

Performed the following validations:

- COUNT(DISTINCT CustomerID)
- GROUP BY CustomerID
- One-to-Many relationship validation
- Orphan record validation using LEFT JOIN

No orphan records were found.

---

# Task 6 - CSV Export

Successfully exported SQL query results into CSV format for further analysis.

---

# Task 7 - Data Cleaning using Pandas

Performed the following cleaning operations:

- Loaded the exported CSV file using Pandas.
- Printed missing value count for every column.
- Printed missing value percentage for every column.
- No numeric columns contained missing values, so no mean/median imputation was required. Missing values were present only in text columns and were filled with "unknown" as instructed.
- Verified that all missing values became zero after cleaning.
- Checked duplicate rows.
- Rows before removing duplicates: *93*
- Rows after removing duplicates: *93*
- No duplicate rows were found.
- Saved the cleaned dataset as:

*task7_cleaned_data.csv*

---

# Task 8 - Outlier Analysis

The exported Task 4 dataset was examined to identify continuous numeric columns for outlier detection.

### Result

- No continuous numeric columns were present in the exported Task 4 dataset.
- Therefore, IQR and Z-score outlier detection could not be applied.

### Reason

The exported dataset contains only text/object columns (CustomerID, CompanyName, OrderID, and OrderDate), so there were no continuous numeric measures available for statistical outlier analysis.

### Comparison

- IQR Method: Not Applicable
- Z-Score Method: Not Applicable

---

# Technologies Used

- SQLite3
- SQL
- Python
- Pandas
- VS Code

---

# Files Included

- part1.queries.sql
- task4_join_result.csv
- task7.py
- task7_cleaned_data.csv
- README.md

---

# Conclusion

This project successfully demonstrates SQL querying, joins, referential integrity validation, CSV export, and data cleaning using Python (Pandas). The exported dataset did not contain continuous numeric columns; therefore, statistical outlier detection methods (IQR and Z-score) were not applicable. All required tasks were completed according to the project requirements.