
# importing pandas for data manipulation
import pandas as pd

# ETL SETUP 
# Getting the raw NHS Talking Therapies data for London
file_path = "/Users/raf/Desktop/data_workbook/london_full_year_MASTER.csv"
output_path = "/Users/raf/Desktop/data_workbook/"

# Loading the CSV and cleaning up headers so they are easy to work with
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# SCHEMA MAPPING
# Translating technical NHS codes into clear labels for dashboard
rename_map = {
    "Count_ReferralsReceived" : "Referrals Received",
    "Count_FirstAssessment" : "First Assessment",
    "Count_FinishedCourseTreatment" : "Finished Course Treatment",
    "Count_FinishedIntegratedReferrals" : "Finished Integrated Referrals",
    "Count_NHSTalkingTherapiesReferrals" : "NHS Talking Therapies Referrals",
    "Count_EndedNotSeen" : "Ended Not Seen",
    "Count_EndedTreatedOnce" : "Ended Treated Once",
    "Count_EndedNotAssessed" : "Ended Not Assessed",
    "Count_EndedBeforeCareProfessionalPlanned" : "Ended Before Planned",
    "Count_EndedDeclined" : "Ended Declined"

}

# Filtering for just the KPIs we need and applying the new names
fact_table = df[df["MEASURE_NAME"].isin(rename_map.keys())].copy()
fact_table["MEASURE_NAME"] = fact_table["MEASURE_NAME"].map(rename_map)

# DATA CLEANING
# Fixing "dirty" data: Turning suppression symbols (*) into 0 so we can do calculations
fact_table["MEASURE_VALUE_SUPPRESSED"] = pd.to_numeric(fact_table["MEASURE_VALUE_SUPPRESSED"], errors='coerce').fillna(0)

# FEATURE ENGINEERING
# Standardizing dates to make sure the jump from 2025 to 2026 stays in order
fact_table["Reporting_Month"] = pd.to_datetime(fact_table["Reporting_Month"], format="%b_%Y")

# Creating a Sort Key so the charts show months chronologically, not alphabetically
fact_table["Month_Sort_Key"] = fact_table["Reporting_Month"].dt.strftime('%Y-%m')
fact_table["Month_Display"] = fact_table["Reporting_Month"].dt.strftime('%b %Y')

# AGREGATION & EXPORT
# Grouping the data data into a clean "Fact Table" ready for Power BI
final_fact_table = fact_table.groupby(["Month_Sort_Key", "Month_Display", "ORG_NAME1", "MEASURE_NAME"])["MEASURE_VALUE_SUPPRESSED"].sum().reset_index()

# Exporting the cleaned and aggregated dataset to a new CSV for Power BI
final_fact_table.to_csv(f"{output_path}nhs_london_table.csv", index=False)

print("Complete")