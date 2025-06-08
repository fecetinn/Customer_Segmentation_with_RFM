# 👟 FLO Customer RFM Segmentation

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Analytics](https://img.shields.io/badge/Data_Analytics-RFM%20%7C%20Segmentation-brightgreen)

> **Goal:** Identify actionable customer segments using **Recency-Frequency-Monetary (RFM)** analysis and export audience lists for targeted marketing campaigns.

---

## 🌟 Overview
This project was carried out to segment the customer base of FLO, a leading online shoe store, and to develop specific marketing strategies for each segment. Customer behaviors were defined using Recency, Frequency, and Monetary (RFM) analysis, and groups were formed based on these behavioral clusters.

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

### Dataset Story
The dataset consists of information obtained from the past shopping behaviors of customers who made their last purchases from FLO in 2020 - 2021 as OmniChannel (shopping both online and offline).

Dataset Details: 12 Variables, 19,945 Observations, 2.7MB

| Variable Name                 | Description                                                                    |
| :---------------------------- | :----------------------------------------------------------------------------- |
| `master_id`                   | Unique customer ID                                                             |
| `order_channel`               | The channel used for shopping (Android, iOS, Desktop, Mobile)                  |
| `last_order_channel`          | The channel through which the last purchase was made                           |
| `first_order_date`            | The date of the customer's first purchase                                      |
| `last_order_date`             | The date of the customer's last purchase                                       |
| `last_order_date_online`      | The date of the customer's last purchase on an online platform                 |
| `last_order_date_offline`     | The date of the customer's last purchase on an offline platform                |
| `order_num_total_ever_online` | Total number of purchases made by the customer on online platforms             |
| `order_num_total_ever_offline`| Total number of purchases made by the customer on offline platforms            |
| `customer_value_total_ever_offline` | Total amount paid by the customer for offline purchases                    |
| `customer_value_total_ever_online`  | Total amount paid by the customer for online purchases                     |
| `interested_in_categories_12` | List of categories the customer has shopped in during the last 12 months       |

> *The raw CSV is proprietary and therefore **not** committed to the repo.  
> Place `flo_data_20k.csv` under `data/` before running the script.*

### 🧩 **Business Problem**

An online shoe store, FLO, wants to segment its customers and determine marketing strategies based on these segments. To achieve this, customer behaviors will be defined, and groups will be formed based on the clusters in these behaviors.

---

## ⚙️ Rule-Based Classification Steps

1. Cleans & enriches the raw data  
2. Calculates R, F, M scores with quantile binning  
3. Maps combined `RF_Score` values to 11 behavioural segments (e.g. *champions*, *hibernating*)  
4. Generates two CSV target lists  
   * **`marketing_1.csv`** → premium women-shoe push for *champions* & *loyal_customers*  
   * **`marketing_2.csv`** → discount coupon for *cant_loose / hibernating / about_to_sleep / new_customers* interested in men/kids categories  

The script prints a rich console report via **tabulate** so you can sanity-check shape, dtypes, missing values and descriptive stats in one shot.

---

## 🛠 Data Pipeline
### Feature Engineering
| New Column          | Formula                                                                |
|---------------------|------------------------------------------------------------------------|
| `total_order_num`   | `order_num_total_ever_online + order_num_total_ever_offline`           |
| `total_order_value` | `customer_value_total_ever_online + customer_value_total_ever_offline` |

All date columns are converted to `datetime64[ns]` for delta calculations.

### RFM Scoring
- **Recency** = This measures how recently a customer made a purchase. It's calculated as the number of days since their last order, with the current date serving as the reference point. 
- **Frequency** = This represents the total number of purchases a customer has made over their entire history with the store. 
- **Monetary** = This indicates the total amount of money a customer has spent over their entire history with the store. 
- Each metric is binned into quintiles → scores **1–5** (higher = better)

### Segmentation Logic
While RFM traditionally includes Monetary, the segmentation here relies only on Recency and Frequency to prioritize customer activity and engagement. This simplification ensures interpretable segments and aligns better with marketing strategies focused on reactivation and loyalty.

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
    r'5[4-5]'    : 'champions'}
```

---

## 📈 Exploratory Insights

| SEGMENTS              | Recency_Avg | R_Avg | Frequency_Avg | F_Avg | Monetary_Avg | M_Avg |
|-----------------------|------------:|------:|--------------:|------:|-------------:|------:|
| about_to_sleep        | 1580.73     | 3.00  | 2.41          | 1.51 | 361.87       | 1.87 |
| at_Risk               | 1708.68     | 1.51  | 4.47          | 3.47 | 648.97       | 3.15 |
| cant_loose            | 1701.34     | 1.54  | 10.71         | 5.00 | 1481.15      | 4.56 |
| champions             | 1483.67     | 5.00  | 9.01          | 4.56 | 1415.99      | 4.31 |
| hibernating           | 1714.11     | 1.48  | 2.39          | 1.49 | 362.43       | 1.88 |
| loyal_customers       | 1548.30     | 3.55  | 8.35          | 4.51 | 1217.72      | 4.18 |
| need_attention        | 1579.50     | 3.00  | 3.74          | 3.00 | 551.16       | 2.75 |
| new_customers         | 1484.44     | 5.00  | 2.00          | 1.00 | 346.34       | 1.77 |
| potential_loyalists   | 1503.71     | 4.51  | 3.31          | 2.52 | 534.05       | 2.65 |
| promising             | 1524.77     | 4.00  | 2.00          | 1.00 | 332.65       | 1.72 |

---

## 🎯 Marketing Use-Cases

### Campaign 1: Women’s High-Value Launch
- **Target Segments:** `champions`, `loyal_customers`
- **Category Filter:** Customers interested in **KADIN**
- **Goal:** Promote new premium-priced women's shoes
- **Output File:** `marketing_1.csv`

```python
# Create boolean filters based on interest in categories
df_all['is_women'] = df_all['interested_in_categories_12'].str.contains(r'\bKADIN\b', na=False, regex=True)

# Filter relevant segments and interested categories
df_marketing1 = df_all[(df_all["SEGMENTS"].isin(["champions", "loyal_customers"])) &
                       (df_all['is_women'] == True)]

# Export master IDs for campaign use
df_marketing1["master_id"].to_csv("marketing_1.csv")
```

### Campaign 2: Discount Win-Back for Men & Kids

- **🎯 Target Segments:** `cant_loose`, `hibernating`, `about_to_sleep`, `new_customers`  
- **📦 Category Filter:** Customers interested in **ERKEK** or **COCUK**  
- **🎁 Goal:** Win back inactive or at-risk customers by offering discounts on men's and kids' products  
- **📤 Output File:** `marketing_2.csv`

```python
# Create boolean filters based on interest in categories
df_all['is_men'] = df_all['interested_in_categories_12'].str.contains(r'\bERKEK\b', na=False, regex=True)
df_all['is_children'] = df_all['interested_in_categories_12'].str.contains(r'\bCOCUK\b', na=False, regex=True)

# Filter relevant segments and interested categories
ddf_marketing2 = df_all[(df_all["SEGMENTS"].isin(["cant_loose",
                                                 "hibernating",
                                                 "about_to_sleep",
                                                 "new_customers"])) &
                       (df_all['is_men'] | df_all['is_children'])]

# Export master IDs for campaign use
df_marketing2["master_id"].to_csv("marketing_2.csv")
```

---

## 🛠 Tech Stack

- Python
- Pandas
- RFM Segmentation

---

## 📄 License

MIT License. See `LICENSE` file for details.

Feel free to contribute to this project by submitting issues or pull requests. Your contributions are welcome!

---

## 📫 Contact

Feel free to reach out:

<p align="left">
  <a href="www.linkedin.com/in/fatih-eren-cetin" target="_blank"  rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/LinkedIn-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" height="30" />
  </a>
  
  <a href="https://medium.com/@fecetinn" target="_blank"  rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium" height="30" />
  </a>
  
  <a href="https://www.kaggle.com/fatiherencetin" target="_blank"  rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white" alt="Kaggle" height="30" />
  </a>
</p>

---

## 🔮 Future Work

- 🛠 **Automation**  
  Schedule RFM segmentation jobs using orchestration tools such as **Airflow** or **Prefect** for regular updates.

- 🧠 **Attribution Modeling**  
  Combine RFM segmentation results with web/app analytics data to build **multi-touch attribution** models and gain deeper insights into the customer journey.

- 📊 **Dashboarding**  
  Develop an interactive dashboard using **Streamlit**, **Dash**, or **Tableau** to allow business users to explore RFM segments visually.

- 🎯 **Uplift Modeling**  
  Implement **uplift modeling** (a.k.a. incremental impact models) to measure the causal effect of marketing campaigns on different RFM segments.

- 🧪 **Segment-Level A/B Testing**  
  Run segment-specific **A/B or multivariate tests** to evaluate personalized campaign performance (e.g., champions vs hibernating).
