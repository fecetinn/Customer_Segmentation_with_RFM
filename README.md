# 👟 FLO Customer RFM Segmentation

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Analytics](https://img.shields.io/badge/Data_Analytics-RFM%20%7C%20Segmentation-brightgreen)

> **Goal:** Identify actionable customer segments using **Recency-Frequency-Monetary (RFM)** analysis and export audience lists for targeted marketing campaigns.

---

## 🌟 Overview
FLO is a leading omni-channel footwear retailer in Türkiye.  
This project ingests ~20 K anonymised transactions and:

1. Cleans & enriches the raw data  
2. Calculates R, F, M scores with quantile binning  
3. Maps combined `RF_Score` values to 11 behavioural segments (e.g. *champions*, *hibernating*)  
4. Generates two CSV target lists  
   * **`marketing_1.csv`** → premium women-shoe push for *champions* & *loyal_customers*  
   * **`marketing_2.csv`** → discount coupon for *cant_loose / hibernating / about_to_sleep / new_customers* interested in men/kids categories  

The script prints a rich console report via **tabulate** so you can sanity-check shape, dtypes, missing values and descriptive stats in one shot.

---

## 🗂 Table of Contents
- [🌟 Overview](#-overview)
- [📊 Dataset Description](#-dataset-description)
- [🛠 Data Pipeline](#-data-pipeline)  
  - [Feature Engineering](#feature-engineering)  
  - [RFM Scoring](#rfm-scoring)  
  - [Segmentation Logic](#segmentation-logic)
- [📈 Exploratory Insights](#-exploratory-insights)
- [🎯 Marketing Use-Cases](#-marketing-usecases)
- [🚀 Quick Start](#-quick-start)
- [🔮 Future Work](#-future-work)
- [📄 License](#-license)
- [📫 Contact](#-contact)

---

## 📊 Dataset Description
| **Property** | **Value** |
|--------------|-----------|
| Observations | **19 945** rows |
| Features     | **12** original columns |
| Size         | ~**10 MB** in memory |
| Time Span    | 2013-10-11 → 2021-05-29 |

Key variables include online/offline order counts & spend, order channels, and a 12-month category-interest vector.

> *The raw CSV is proprietary and therefore **not** committed to the repo.  
> Place `flo_data_20k.csv` under `data/` before running the script.*

---

## 🛠 Data Pipeline
### Feature Engineering
| New Column          | Formula                                                                |
|---------------------|------------------------------------------------------------------------|
| `total_order_num`   | `order_num_total_ever_online + order_num_total_ever_offline`           |
| `total_order_value` | `customer_value_total_ever_online + customer_value_total_ever_offline` |

All date columns are converted to `datetime64[ns]` for delta calculations.

### RFM Scoring
- **Recency** = days since each customer’s last purchase (today’s date = script runtime)  
- **Frequency / Monetary** = lifetime totals  
- Each metric is binned into quintiles → scores **1–5** (higher = better)

### Segmentation Logic
```python
segment_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5'    : 'cant_loose',
    r'3[1-2]'    : 'about_to_sleep',
    r'33'        : 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41'        : 'promising',
    r'51'        : 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]'    : 'champions'
}
