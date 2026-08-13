# part 2 - statistical EDA, HYPOTHESIS TESTING & VISUALIXATIO
## Task 1 — Initial Inspection

### Definition
Initial inspection is the process of understanding a dataset's structure, data types, missing values, and basic characteristics before performing further analysis.

### What I Did
- Loaded the Customers table into a Pandas DataFrame.
- Used df.info() to inspect columns, data types, and missing values.
- Used df.describe(include='all') to get an overall statistical summary.

### Key Findings
- The dataset contains *93 customer records* and *11 columns*.
- CustomerID contains *93 unique values*.
- Several columns contain missing values.
- Fax has the highest number of missing values.

### Conclusion
The initial inspection provided an understanding of the dataset structure and data quality, forming the foundation for the statistical EDA performed in the following tasks.\


 ## Task 2 — NumPy Fundamentals

### Definition
NumPy is a Python library used for efficient numerical operations on arrays. 
It supports vectorized calculations and Boolean indexing for fast data analysis.

### What I Did
- Converted the Quantity column into a NumPy array.
- Applied a 10% increase using vectorized arithmetic.
- Used Boolean indexing to filter records where Quantity is between 10 and 30.

### Key Findings
- The Quantity column was successfully converted into a NumPy array.
- A 10% increase was applied to all values using vectorized arithmetic.
- Boolean filtering returned *256,547 rows across 5 columns*.

### Conclusion
NumPy operations were used to efficiently perform vectorized calculations and condition-based filtering on the dataset.

## Task 3 — Descriptive Statistics

### Definition
Descriptive statistics is the process of summarizing and understanding numerical data using measures such as mean, median, standard deviation, variance, and percentiles.

### What I Did
- Converted the Quantity and UnitPrice columns into NumPy arrays.
- Calculated the *mean, median, standard deviation, variance, and 90th percentile* for both numerical columns.
- Used NumPy statistical functions for the calculations.

### Results

| Statistic | Quantity | UnitPrice |
|---|---:|---:|
| Mean | 25.5031 | 28.8508 |
| Median | 25.0 | 19.5 |
| Standard Deviation | 14.4539 | 33.5644 |
| Variance | 208.9161 | 1126.6390 |
| 90th Percentile | 46.0 | 49.3 |

### Key Findings
- The average order quantity is approximately *25.5 units*.
- The median quantity is *25 units*.
- UnitPrice shows considerably higher variability than Quantity.
- 90% of the Quantity values are at or below *46 units*.
- 90% of the UnitPrice values are at or below *49.3*.

### Conclusion
Descriptive statistics provided a clear summary of the distribution and variability of Quantity and UnitPrice, helping identify differences in their central tendency and spread.

## Task 4 — Feature Engineering

### Definition
Feature engineering is the process of creating new meaningful features from existing data to support further analysis and decision-making.

### What I Did
- Created a new TotalValue column.
- Calculated TotalValue using UnitPrice × Quantity.
- Verified the newly created feature using df.head().

### Formula

*TotalValue = UnitPrice × Quantity*

### Example Results

| OrderID | ProductID | UnitPrice | Quantity | TotalValue |
|---:|---:|---:|---:|---:|
| 10248 | 11 | 14.0 | 12 | 168.0 |
| 10248 | 42 | 9.8 | 10 | 98.0 |
| 10248 | 72 | 34.8 | 5 | 174.0 |
| 10249 | 14 | 18.6 | 9 | 167.4 |
| 10249 | 51 | 42.4 | 40 | 1696.0 |

### Key Finding
The newly created TotalValue feature represents the value of each order line based on its unit price and quantity.

### Conclusion
Feature engineering transformed the existing UnitPrice and Quantity variables into a useful TotalValue metric for further grouped analysis and visualization.

## Task 5 — Grouped Analysis

### Definition
Grouped analysis is the process of summarizing data by groups using aggregation functions such as sum, mean, count, minimum, and maximum.

### What I Did
- Created pivot tables using Pandas pivot_table().
- Calculated the total TotalValue for each ProductID.
- Calculated the total Quantity for each OrderID.
- Used groupby().agg() to perform multiple aggregations across numerical columns.

### Pivot Table 1 — Total Value by Product

| ProductID | TotalValue |
|---:|---:|
| 1 | 3,633,663.6 |
| 2 | 3,832,714.2 |
| 3 | 2,021,660.0 |
| 4 | 4,371,430.8 |
| 5 | 4,261,475.3 |

### Pivot Table 2 — Quantity by Order

The second pivot table aggregates the total Quantity for each OrderID.

### Key Findings
- ProductID was used to analyze total sales value.
- OrderID was used to summarize total quantities.
- Pivot tables made it easier to compare groups and identify high-value products.
- Multiple aggregation functions were also applied using groupby().agg().

### Conclusion
Grouped analysis provided a structured way to summarize the dataset at product and order levels, making it easier to compare performance and identify important patterns.

## Task 6 — Bucket Segmentation

### Definition
Bucket segmentation is the process of dividing continuous numerical values into meaningful categories or ranges.

### What I Did
- Created a Python function to classify Quantity into three categories.
- Applied the function to the entire DataFrame using apply().
- Created a new categorical column named QuantityBucket.

### Segmentation Rules

| Quantity Range | Bucket |
|---|---|
| Quantity < 10 | Low |
| 10 ≤ Quantity ≤ 30 | Medium |
| Quantity > 30 | High |

### Example Results

| Quantity | QuantityBucket |
|---:|---|
| 12 | Medium |
| 10 | Medium |
| 5 | Low |
| 9 | Low |
| 40 | High |

## Task 7 — Correlation Analysis

### Definition
Correlation analysis measures the strength and direction of the relationship between numerical variables. Pearson correlation values range from -1 to +1.

### What I Did
- Selected all numerical columns from the dataset.
- Computed the Pearson correlation matrix.
- Excluded the diagonal values to avoid self-correlation.
- Identified the pairs with the highest and lowest absolute correlation.

### Results

| Analysis | Variable Pair | Correlation |
|---|---|---:|
| Highest absolute correlation | UnitPrice & TotalValue | 0.9078 |
| Lowest absolute correlation | Discount & TotalValue | -0.0001 |

### Key Findings
- UnitPrice and TotalValue have a *strong positive correlation (0.9078)*.
- Discount and TotalValue show *almost no linear correlation (-0.0001)*.
- The strong relationship between UnitPrice and TotalValue is expected because TotalValue was derived using UnitPrice × Quantity.

### Conclusion
The correlation analysis identified the strongest and weakest relationships among the numerical variables and helped understand how the variables are related to each other.