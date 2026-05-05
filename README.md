# NYC Yellow Taxi - MongoDB Medallion Architecture

**Course:** Big Data: Tools and Techniques (Spring 2026)
**Database:** MongoDB
**Dataset:** NYC TLC Yellow Taxi Trip Records, January 2024
**Size:** 2,964,624 rows x 19 columns (250,000-row sample loaded into MongoDB)

## Setup

```bash
pip install -r requirements.txt
python download_data.py
jupyter notebook nyc_taxi_mongodb_medallion.ipynb
```

## Medallion Architecture

**Bronze** - Raw parquet data loaded into MongoDB `taxi_bronze` collection with indexes on pickup datetime and location ID.

**Silver** - Cleaned data via MongoDB aggregation pipeline: removes nulls, outliers, invalid dates, and duplicates. Stored in `taxi_silver`.

**Gold** - Five aggregated collections:
- `taxi_gold_by_hour` - Trips and revenue by hour of day
- `taxi_gold_by_dow` - Weekly seasonality
- `taxi_gold_top_pickups` - Top 15 pickup zones by revenue
- `taxi_gold_by_payment` - Payment method distribution
- `taxi_gold_tip_by_pax` - Tip percentage by passenger count

## Visualizations

All plots saved in `visualizations/` directory:
- Trips & Revenue by hour
- Trips by day of week
- Top 15 pickup locations
- Payment type mix
- Tip % vs passenger count

## Key Insights

- Peak demand: 5-7 PM, lowest: 4-5 AM
- Thursday and Friday are busiest days
- Top 15 pickup zones generate disproportionate revenue
- Credit card payments account for 70%+ of trips
- Tip percentage is flat (~15-18%) across passenger counts
