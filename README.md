# IDX-Exchange-Data-Analyst
Code and documentation from my Data Analyst Internship at IDX Exchange, covering the cleaning, analysis, and visualization of MLS real estate data with Python, pandas, and Tableau. MLS data is confidential, so raw data files and credentials are excluded from this repository.

# Week 0
Week 0 focused on software setup and downloading files from the FTP.

## Files
- `python/crmls_listed.py` extracts MLS listing data.
- `python/crmls_sold.py` extracts MLS sold data.
- Monthly csv file stored in `csv`.

## Week 0 Tasks
- Organized the project files.
- Exported the files: monthly listing and sold datasets.
- Reviewed Trestle Property Metadata.
- Analyzed the data.

# Week 1
Load and concatenate monthly listing and sold datasets for analysis.

## Week 1 Tasks
- Loaded and concatenated monthly listed and sold files from January 2024 until the recently completed month.
- Combined listing into one dataset.
- Combined sold into another dataset.
- Confirmed row counts before and after concatenation.
- Confirmed row counts before and after the Residential filter.

# Week 2
Used EDA to analyze the dataset, and inspected the data to make sure only relevant property records are used.

## Week 2 Tasks
- ***market analysis & metadata, flagged columns that were >90% null, identified number of rows and columns, and decided which columns to drop.
- Produced a numeric distribution summary with the .py script.
- Created visualizations.
- Median and average close prices
    - SOLD (median = $823k. average = $1,193, 864.08)
    - LISTING (median = $850k. average = $1, 203, 601.57)
- Percentage of homes sold above list price: 40.1%
- Percentage of homes sold below list price: 42.5%
