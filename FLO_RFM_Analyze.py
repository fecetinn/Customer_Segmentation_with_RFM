################################################
# LIBRARIES
################################################
import pandas as pd
from datetime import date, datetime
from tabulate import tabulate



################################################
# SETTINGS
################################################
pd.set_option("display.max_columns", None)
pd.set_option("display.max_row", 20)
pd.set_option("display.float_format", lambda x: "%.2f" %x)



################################################
# FUNCTIONS
################################################
def load_csv_data(filepath):
    """
    Load a dataset from an Excel file.

    Parameters
    ----------
    filepath : str
        Path to the Excel (.xlsx) file containing the dataset.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the loaded dataset.
    """
    return pd.read_csv(filepath)


def check_df_tabulate(dataframe, head=10):

    print("#" * 84)
    print("#" * 27, " " * 5, "DATAFRAME REPORT", " " * 5, "#" * 27)
    print("#" * 84)


    # 1. Basic Information
    basic_data = [
        ["Number of Rows", dataframe.shape[0]],
        ["Number of Columns", dataframe.shape[1]],
        ["Total Number of Cells", dataframe.shape[0] * dataframe.shape[1]],
        ["Memory (MB)", round(dataframe.memory_usage(deep=True).sum() / 1024 ** 2, 2)]
    ]

    print("\n📊 BASIC INFORMATION")
    print(tabulate(basic_data, headers=["Metric", "Value"], tablefmt="fancy_grid"))


    # 2. Column Information
    column_data = []
    for col in dataframe.columns:
        column_data.append([
            col,
            str(dataframe[col].dtype),
            dataframe[col].nunique(),
            dataframe[col].isnull().sum(),
            f"{round((dataframe[col].isnull().sum() / len(dataframe)) * 100, 2)}%"
        ])

    print("\n📋 COLUMN INFORMATION")
    print(tabulate(column_data,
                   headers=["Column", "Type", "Number of Unique Value", "Number of NaN", "NaN %"],
                   tablefmt="fancy_grid"))


    # 3. Statistics (for Numerical columns)
    numeric_cols = dataframe.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        print("\n📈 STATISTICS OF NUMERICAL COLUMNS")
        stats_data = []
        for col in numeric_cols:
            col_data = dataframe[col]
            stats_data.append([
                col,
                round(col_data.mean(), 2),
                round(col_data.std(), 2),
                col_data.min(),
                round(col_data.quantile(0.01), 2),
                round(col_data.quantile(0.1), 2),
                round(col_data.quantile(0.25), 2),
                round(col_data.median(), 2),
                round(col_data.quantile(0.75), 2),
                round(col_data.quantile(0.9), 2),
                round(col_data.quantile(0.99), 2),
                col_data.max()
            ])

        print(tabulate(stats_data,
                       headers=["Column", "Mean", "Std", "Min","%1", "%10",
                                "Q1", "Median", "Q3", "%90","%99","Max"],
                       tablefmt="fancy_outline"))


    # 4. Head
    print(f"\n🔝 FIRST {head} ROWS")
    print(tabulate(dataframe.head(head), headers='keys', tablefmt="rounded_outline"))


    # 5. Tail
    print(f"\n🔚 LAST {head} ROWS")
    print(tabulate(dataframe.tail(head), headers='keys', tablefmt="rounded_outline"))



################################################
# DATA LOADING
################################################
df_backup = load_csv_data("FLOMusteriSegmentasyonu/flo_data_20k.csv")
df = df_backup.copy()



################################################
# GENERAL OVERVIEW
################################################
check_df_tabulate(df)



################################################
# DATA TYPE ADJUSTMENTS
################################################
df["first_order_date"] = pd.to_datetime(df["first_order_date"])
df["last_order_date"] = pd.to_datetime(df["last_order_date"])
df["last_order_date_online"] = pd.to_datetime(df["last_order_date_online"])
df["last_order_date_offline"] = pd.to_datetime(df["last_order_date_offline"])



################################################
# EARLY FEATURE ENGINEERING
################################################
df["total_order_num"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["total_order_value"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]



################################################
# ANALYZES
################################################
channel_analyze = df.groupby("last_order_channel").agg(TOTAL_ORDER_NUM=("total_order_num", "sum"),
                                    TOTAL_ORDER_VAL=("total_order_value", "sum"))

print(channel_analyze)

top10_val = df.sort_values(by="total_order_value", ascending=False).head(10)
print(top10_val)

top10_order_num = df.sort_values(by="total_order_num", ascending=False).head(10)
print(top10_order_num)



################################################
# RFM FEATURE ENGINEERING
################################################
df_rfm = df.groupby("master_id").agg(Last_Order_Date=("last_order_date", "max"),
                                     FREQUENCY=("total_order_num", "sum"),
                                     MONETARY=("total_order_value", "sum")).reset_index()

df_rfm["RECENCY"] = (pd.to_datetime(date.today()) - df_rfm["Last_Order_Date"]).dt.days
df_rfm.drop(["Last_Order_Date"], axis=1, inplace=True)

print(df_rfm)


# Recency score
df_rfm['R'] = pd.qcut(df_rfm["RECENCY"].rank(method='first'), 5, labels=[5, 4, 3, 2, 1]).astype("int")

# Frequancy score
df_rfm['F'] = pd.qcut(df_rfm["FREQUENCY"].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype("int")

# Monetary score
df_rfm['M'] = pd.qcut(df_rfm["MONETARY"].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype("int")

print(df_rfm)


# RFM scores
df_rfm["RFM"] = (df_rfm["R"].astype("str") +
                 df_rfm["F"].astype("str") +
                 df_rfm["M"].astype("str")).astype("int")

# Segmentation scores
df_rfm["RF_Score"] = (df_rfm["R"].astype("str") +
                 df_rfm["F"].astype("str")).astype("int")

print(df_rfm)


# Segment dictionary
segment_map = {r'[1-2][1-2]': 'hibernating',
               r'[1-2][3-4]': 'at_Risk',
               r'[1-2]5': 'cant_loose',
               r'3[1-2]': 'about_to_sleep',
               r'33': 'need_attention',
               r'[3-4][4-5]': 'loyal_customers',
               r'41': 'promising',
               r'51': 'new_customers',
               r'[4-5][2-3]': 'potential_loyalists',
               r'5[4-5]': 'champions'}

# Segmentation
df_rfm['SEGMENTS'] = df_rfm['RF_Score'].astype("str").replace(segment_map, regex=True)

print(df_rfm)



################################################
# RFM ANALYZES
################################################
df_rfm_analyze = df_rfm.groupby("SEGMENTS").agg(Recency_Avg=("RECENCY", "mean"),
                                                R_Avg=("R", "mean"),
                                                Frequency_Avg=("FREQUENCY", "mean"),
                                                F_Avg=("F", "mean"),
                                                Monetary_Avg=("MONETARY", "mean"),
                                                M_Avg=("M", "mean")).reset_index()

print(df_rfm_analyze)


df_all = pd.merge(df, df_rfm, on="master_id")

print(df_all)



################################################
# MARKETING STRATEGIES
################################################
# For new and expensive women shoes
df_all['is_women'] = df_all['interested_in_categories_12'].str.contains(r'\bKADIN\b', na=False, regex=True)

df_marketing1 = df_all[(df_all["SEGMENTS"].isin(["champions", "loyal_customers"])) &
                       (df_all['is_women'] == True)]

print(df_marketing1)


df_marketing1["master_id"].to_csv("marketing_1.csv")


# For discount of children and men products
df_all['is_men'] = df_all['interested_in_categories_12'].str.contains(r'\bERKEK\b', na=False, regex=True)
df_all['is_children'] = df_all['interested_in_categories_12'].str.contains(r'\bCOCUK\b', na=False, regex=True)

df_marketing2 = df_all[(df_all["SEGMENTS"].isin(["cant_loose",
                                                 "hibernating",
                                                 "about_to_sleep",
                                                 "new_customers"])) &
                       (df_all['is_men'] | df_all['is_children'])]

print(df_marketing2)

df_marketing2["master_id"].to_csv("marketing_2.csv")
