# Presentation Outline

## Intro (30 sec)
- Name and project overview
- Dataset: NYC Yellow Taxi Jan 2024 (2.96M rows, 19 columns)
- MongoDB database with Medallion architecture

## Why MongoDB (30 sec)
- Document model for optional fields
- Aggregation Pipeline for transformations
- Indexes for fast queries
- Scalability via sharding

## Bronze Layer (45 sec)
- Load parquet with pandas
- Show dataset shape
- Sample 250k rows for MongoDB
- Insert into taxi_bronze collection
- Create indexes
- Verify row/column count with MongoDB queries

## Silver Layer (60 sec)
- Aggregation pipeline for cleaning
- Remove nulls, outliers, invalid dates
- Deduplicate records
- Output to taxi_silver
- Show records removed (~8%)

## Gold Layer (90 sec)
- Five aggregation pipelines
- By hour, by day of week, top pickups, payment mix, tip by passenger count
- Each persisted to separate collection
- Show results

## Visualizations (60 sec)
- Show each plot
- Explain key insights
- Peak hours, busiest days, payment types

## Production Notes (30 sec)
- $out for persisted collections
- Notebook as reproducible ETL
- Sharding for full-scale deployment

## Wrap up (10 sec)
- GitHub URL
