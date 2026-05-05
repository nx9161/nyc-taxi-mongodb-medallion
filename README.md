# NYC Yellow Taxi - MongoDB Medallion Architecture

**Course:** Big Data: Tools and Techniques (Spring 2026)
**Database:** MongoDB (NoSQL, document store)
**Dataset:** NYC TLC Yellow Taxi Trip Records, January 2024
**Size:** 2,964,624 rows x 19 columns (250,000-row sample loaded into MongoDB)

A full Big Data pipeline implementing the **Medallion architecture** (Bronze /
Silver / Gold) on top of MongoDB, with native Aggregation Pipelines and
Matplotlib visualizations.

---

## 1. Why MongoDB?

| Reason | Detail |
|--------|--------|
| Document model | Trip records have optional fields (`Airport_fee`, `congestion_surcharge`) - no schema migrations needed when TLC adds columns. |
| Aggregation Pipeline | Declarative, composable Gold-layer transformations (`$match`, `$group`, `$project`, `$out`). |
| Indexing | B-tree indexes on `tpep_pickup_datetime` and `PULocationID` keep time-series and zonal aggregations fast. |
| Scalability | Sharding on a hashed pickup-datetime key distributes monthly ingest evenly across the cluster. |
| Tooling | Native integration with Python (`pymongo`), Charts, and BI connectors (Tableau, Power BI). |

---

## 2. Repository Layout

```
Deliverable/
|-- README.md                              # this file
|-- requirements.txt                       # Python dependencies
|-- download_data.py                       # one-click dataset downloader
|-- nyc_taxi_mongodb_medallion.ipynb       # main notebook (executed, with outputs)
|-- _build_notebook.py                     # generates the notebook (reference only)
|-- presentation_script.md                 # 5-6 minute video walk-through script
|-- data/
|   `-- yellow_tripdata_2024-01.parquet    # ~48 MB raw dataset
`-- visualizations/
    |-- 01_trips_revenue_by_hour.png
    |-- 02_trips_by_dow.png
    |-- 03_top_pickups.png
    |-- 04_payment_mix.png
    `-- 05_tip_by_passengers.png
```

---

## 3. Reproducing the Project

### 3.1 Prerequisites
- macOS / Linux / Windows
- **Python 3.10+**
- **MongoDB 6.0+** running locally on `mongodb://localhost:27017`
  (install via `brew install mongodb-community` and `brew services start mongodb-community`)

### 3.2 Setup

```bash
# clone, then:
pip install -r requirements.txt
python download_data.py            # ~48 MB parquet download
jupyter notebook nyc_taxi_mongodb_medallion.ipynb
```

Run all cells top-to-bottom. End-to-end runtime is roughly **30-60 seconds**
on a modern laptop.

---

## 4. Medallion Architecture

### Bronze (`taxi_bronze`)
Raw parquet -> MongoDB. 250,000 documents inserted as-is. Indexes created on
`tpep_pickup_datetime` and `PULocationID`.

### Silver (`taxi_silver`)
A single MongoDB Aggregation Pipeline that:

1. Filters out null / non-positive `passenger_count`, `trip_distance`,
   `fare_amount`, `total_amount`.
2. Removes outliers (`trip_distance > 100 mi`, `total_amount > $1000`).
3. Filters trips with invalid temporal order
   (`tpep_dropoff_datetime <= tpep_pickup_datetime`).
4. Deduplicates on the natural key
   `(VendorID, pickup_dt, dropoff_dt, PULocationID, DOLocationID, total_amount)`
   via `$group` + `$first`.
5. Persists to `taxi_silver` via `$out`.

### Gold (5 collections)
| Collection | Question Answered | Stages |
|------------|-------------------|--------|
| `taxi_gold_by_hour`     | How does demand & revenue vary by hour of day? | `$project` + `$group` + `$sort` |
| `taxi_gold_by_dow`      | What is the weekly seasonality?                | `$dayOfWeek` |
| `taxi_gold_top_pickups` | Which 15 pickup zones drive the most revenue?  | `$group` + `$sort` + `$limit` |
| `taxi_gold_by_payment`  | What is the payment-method mix?                | `$group` |
| `taxi_gold_tip_by_pax`  | How does tipping vary by passenger count?      | `$percentile` (P50, P90) |

Each Gold collection is also returned as a pandas DataFrame and visualized.

---

## 5. Visualizations

All plots are saved under `visualizations/` and embedded inline in the notebook.

1. **Trips & Revenue by hour** - dual-axis bar+line chart.
2. **Trips by day of week** - bar chart with value labels.
3. **Top 15 pickup locations** - horizontal bar chart.
4. **Payment-type mix** - pie chart.
5. **Tip % vs passenger count** - average / median / P90 lines.

---

## 6. Key Insights

1. Demand peaks **17:00 - 19:00**; lowest **04:00 - 05:00**.
2. **Thursday & Friday** are the busiest days; Saturday late-night also strong.
3. Top 15 pickup zones drive a disproportionate share of revenue
   (long-tail) - useful for fleet rebalancing.
4. **Credit card** dominates (>70% of trips); cash trips usually log $0 tip.
5. **Tip percentage is flat (~15-18%) across passenger counts** - passenger
   count is a poor predictor of tipping.

---

## 7. Author

Naman Parmar - Spring 2026
