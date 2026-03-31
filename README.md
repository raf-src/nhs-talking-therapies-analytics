# nhs-talking-therapies-analytics
Situation: Managed a large scale dataset of 288,000 NHS London patient records to evaluate regional productivity

Action: Developed a Python(Pandas) ETL pipeline to automate data sanitization

Result: Engineered a Fact Table for GCP storage, driving a 36% Treatment Completion insight in Power BI

Pipeline: Python(Pandas) for data ingestion and automated cleaning

Cloud (GCP): Hosted processed Fact Tables in Google Cloud Storage (GCS) for scalable "Ground Truth"

BI Integration: Established a live GCP-to-Power BI connection for automated executive reporting

Feature Engineering: Engineered Month_Sort_Key and handled suppressed values (*) via pd.to_numeric


