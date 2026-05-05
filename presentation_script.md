# Presentation Script (5-6 minutes)

Use this as a teleprompter when recording the screen-recording. Timestamps are
target durations.

---

## [0:00 - 0:30] Intro
> "Hi, I'm Naman Parmar. For my Big Data final project I built an end-to-end
> pipeline on the **NYC Yellow Taxi** dataset using **MongoDB** as my
> distributed NoSQL database. The dataset is January 2024 from the NYC Taxi &
> Limousine Commission - **2.96 million rows and 19 columns**, well above the
> 50k-row, 8-column requirement. I implemented the full **Medallion
> architecture**: Bronze, Silver, and Gold."

(Show README.md.)

---

## [0:30 - 1:00] Why MongoDB
> "I chose MongoDB for four reasons: (1) the **document model** handles the
> optional fields in the TLC schema like `Airport_fee` without migrations,
> (2) the **Aggregation Pipeline** is a declarative, composable way to build
> the Gold layer, (3) **indexes** on pickup-datetime and pickup-location ID
> make time-series and zonal queries fast, and (4) **sharding** on a hashed
> pickup-datetime key would scale horizontally as new months arrive."

---

## [1:00 - 1:45] Bronze Layer - Raw ingest
(Open notebook. Run cells through Section 3.)
> "I read the 48 MB parquet file with pandas. The full dataset is
> **2,964,624 rows by 19 columns** - I confirm that with `.shape`. To keep the
> demo fast I take a 250k-row random sample and `insert_many` into the
> `taxi_bronze` collection. Then I create indexes on pickup datetime and
> pickup location.
>
> I verify with `count_documents` and `find_one` that Bronze has **250,000
> rows and 19 columns** - so the row/column requirement is satisfied directly
> from MongoDB."

---

## [1:45 - 2:45] Silver Layer - Cleaning
(Run Section 4.)
> "The Silver layer is a single MongoDB **aggregation pipeline** with five
> stages. I drop nulls and non-positive values in critical fields, drop
> outliers above 100 miles or $1000, drop trips where dropoff is before
> pickup, and **deduplicate** with `$group` on the natural key
> (VendorID, pickup, dropoff, locations, amount). Then `$out` persists the
> result to `taxi_silver`.
>
> The pipeline runs on the server side - no data leaves MongoDB. I removed
> about **20,000 records, roughly 8 percent**, mostly zero-fare or
> zero-distance trips."

---

## [2:45 - 4:15] Gold Layer - Aggregations
(Run Section 5 - all five pipelines.)
> "The Gold layer is five aggregations, each persisted to its own collection
> and returned as a pandas DataFrame:
>
> 1. **By hour** - trips, revenue, average fare, tip, distance per hour.
> 2. **By day of week** - using the `$dayOfWeek` operator.
> 3. **Top 15 pickup locations** - `$group` + `$sort` + `$limit`.
> 4. **Payment-type mix** with friendly labels.
> 5. **Tip percentage by passenger count** using the `$percentile` operator
>    for median and P90 - a feature added in MongoDB 7.
>
> Every Gold collection is now a pre-aggregated table that a BI tool like
> Tableau can hit directly without recomputing."

---

## [4:15 - 5:15] Visualizations & Insights
(Run Section 6 - show each plot.)
> "Five Matplotlib charts:
>
> - Trips and revenue peak between **5 and 7 PM**, lowest at 4 AM.
> - **Thursday and Friday** are the busiest days.
> - The **top 15 pickup zones** generate a disproportionate share of revenue.
> - **Credit card** is over 70 percent of trips.
> - **Tip percentage is flat around 15 to 18 percent** regardless of passenger
>   count - so passenger count is a poor predictor of tipping.
>
> These insights immediately suggest actions: fleet rebalancing toward the
> top zones during evening rush, and digital-payment incentives because tips
> are recorded only on card payments."

---

## [5:15 - 5:50] Production-readiness
> "A few notes on making this production-grade:
> - All Gold collections are persisted via `$out`, so dashboards read
>   pre-aggregated data.
> - The notebook is idempotent - re-running it drops and re-creates Bronze,
>   so it doubles as a reproducible ETL job.
> - For the full month, we'd shard on hashed pickup-datetime so each pipeline
>   stage runs in parallel across shards."

---

## [5:50 - 6:00] Wrap up
> "GitHub URL is in the description. Thanks for watching."

---

## Recording Checklist
- [ ] Close all unrelated apps & notifications.
- [ ] Use a **screen recorder** (QuickTime / OBS / Loom) - **no phone**.
- [ ] **Zoom IDE to 130-150%** so code is readable.
- [ ] Test mic levels (-12 dB peak).
- [ ] Final video < **6 minutes**.
- [ ] Upload to YouTube as **Unlisted**.
- [ ] Submit Canvas text entry with: GitHub URL + YouTube URL.
