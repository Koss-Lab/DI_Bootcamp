#ExercisesXP.py


# Exercise 1: Introduction to Data Analysis (Essay)

# What is data analysis?
# Data analysis is the process of inspecting, cleaning,
# transforming, and interpreting data in order to find
# useful information, draw conclusions, and support decisions.

# Why is data analysis important?
# In modern contexts, data analysis is essential because
# organizations and individuals produce huge amounts of data
# every day. Analyzing this data helps to improve efficiency,
# discover trends, and make evidence-based decisions.

# Three applications of data analysis today:
# 1. Healthcare: analyzing patient data to predict diseases
#    and improve treatment effectiveness.
# 2. Finance: detecting fraud and managing investment risks.
# 3. Marketing: understanding customer behavior and
#    personalizing advertising campaigns.


from pathlib import Path
import pandas as pd

# Optional imports guarded where needed
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_DIRS = [BASE_DIR, BASE_DIR / "data"]  # support files in current dir or ./data

# Helpers

def find_file(candidate_stems, exts=(".csv", ".xlsx"), data_dirs=DATA_DIRS):
    """Return first existing Path that matches any stem + any ext in known data dirs."""
    for d in data_dirs:
        for stem in candidate_stems:
            for ext in exts:
                p = (d / f"{stem}{ext}")
                if p.exists():
                    return p
    return None

def read_csv_smart(path: Path):
    """CSV reader that auto-detects delimiter and retries with latin-1 if needed."""
    try:
        return pd.read_csv(path, sep=None, engine="python")
    except UnicodeDecodeError:
        return pd.read_csv(path, sep=None, engine="python", encoding="latin-1")

def read_excel_smart(path: Path):
    """Excel reader that loads the first sheet by default."""
    try:
        return pd.read_excel(path)
    except Exception:
        xls = pd.ExcelFile(path)
        return pd.read_excel(path, sheet_name=xls.sheet_names[0])

def load_by_candidates(candidates):
    """Try CSV then XLSX for given candidate stems."""
    p = find_file(candidates, exts=(".csv",))
    if p:
        return read_csv_smart(p), p.name
    p = find_file(candidates, exts=(".xlsx",))
    if p:
        return read_excel_smart(p), p.name
    return None, None

def data_types_report(df: pd.DataFrame, title: str):
    """Print dtype and qualitative/quantitative classification per column."""
    print(f"\n=== Data Types Report: {title} ===")
    for col in df.columns:
        dtype = df[col].dtype
        # numeric kinds: b=bool, i=int, u=uint, f=float, c=complex
        quantitative = dtype.kind in {"b", "i", "u", "f", "c"}
        qclass = "quantitative" if quantitative else "qualitative"
        print(f"- {col}: {dtype} -> {qclass}")

# Exercise 2: Load datasets (Sleep, Mental Health, Credit Card)

# Sleep dataset
sleep_candidates = [
    "americans_sleep",
    "sleep_data",
    "How_Much_Sleep_Do_Americans_Really_Get",
    "sleep",
]
sleep_df, sleep_name = load_by_candidates(sleep_candidates)
if sleep_df is not None:
    print(f"\n✅ Loaded Sleep dataset: {sleep_name}")
    print(sleep_df.head())
    print(sleep_df.info())
else:
    print("\n❌ Sleep dataset not found. Expected one of:",
          ", ".join([s + ".csv/.xlsx" for s in sleep_candidates]))

# Mental health dataset (you have 'mental_health.csv')
mh_candidates = [
    "mental_health",
    "Global_Trends_in_Mental_Health",
    "global_mental_health",
]
mh_df, mh_name = load_by_candidates(mh_candidates)
if mh_df is not None:
    print(f"\n✅ Loaded Mental Health dataset: {mh_name}")
    print(mh_df.head())
    print(mh_df.info())
else:
    print("\n❌ Mental Health dataset not found. Expected one of:",
          ", ".join([s + ".csv/.xlsx" for s in mh_candidates]))

# Credit card approvals (you have 'creditcard_crx.csv' and 'creditcard_dataset.csv')
cc_candidates = [
    "creditcard_crx",
    "creditcard_dataset",
    "credit_card_approvals",
    "crx",
]
cc_df, cc_name = load_by_candidates(cc_candidates)
if cc_df is not None:
    print(f"\n✅ Loaded Credit Card dataset: {cc_name}")
    print(cc_df.head())
    print(cc_df.info())
else:
    print("\n❌ Credit Card dataset not found. Expected one of:",
          ", ".join([s + ".csv/.xlsx" for s in cc_candidates]))

# Exercise 3: Identify data types (for previous datasets)

if sleep_df is not None:
    data_types_report(sleep_df, f"Sleep ({sleep_name})")

if mh_df is not None:
    data_types_report(mh_df, f"Mental Health ({mh_name})")

if cc_df is not None:
    data_types_report(cc_df, f"Credit Card ({cc_name})")

# Exercise 4: Iris dataset (prefer Kaggle Iris.csv; else sklearn)

iris_df = None
iris_src = None

iris_csv = find_file(["Iris"], exts=(".csv",))
if iris_csv:
    iris_df = read_csv_smart(iris_csv)
    iris_src = iris_csv.name
else:
    try:
        from sklearn.datasets import load_iris
        iris_bunch = load_iris(as_frame=True)
        iris_df = iris_bunch.frame.copy()
        # sklearn returns 'target' numeric; map to names for qualitative column
        iris_df["species"] = iris_df["target"].map(dict(enumerate(iris_bunch.target_names)))
        iris_df.drop(columns=["target"], inplace=True)
        iris_src = "sklearn.load_iris()"
    except Exception as e:
        print("\n❌ Could not load Iris via Kaggle CSV or sklearn:", e)

if iris_df is not None:
    print(f"\n✅ Loaded Iris dataset from: {iris_src}")
    print(iris_df.head())
    print(iris_df.info())

    # Classify columns (qualitative vs quantitative)
    data_types_report(iris_df, f"Iris ({iris_src})")
else:
    print("\n⚠️ Skipping Iris exercises because Iris dataset is unavailable.")

# Exercise 5: Basic analysis on Iris (mean, median, mode + histogram)

if iris_df is not None:
    # Choose a quantitative column that exists in either Kaggle or sklearn schema
    # sklearn: 'sepal length (cm)' ; Kaggle: 'SepalLengthCm'
    quantitative_candidates = [
        "sepal length (cm)",
        "SepalLengthCm",
        "petal length (cm)",
        "PetalLengthCm",
        "sepal width (cm)",
        "SepalWidthCm",
        "petal width (cm)",
        "PetalWidthCm",
    ]
    qcol = next((c for c in quantitative_candidates if c in iris_df.columns), None)
    if qcol is None:
        print("\n❌ No known quantitative column found in Iris to compute stats.")
    else:
        print(f"\n=== Basic stats on Iris column: {qcol} ===")
        series = pd.to_numeric(iris_df[qcol], errors="coerce").dropna()
        if series.empty:
            print("Column has no numeric data after coercion.")
        else:
            mean_val = series.mean()
            median_val = series.median()
            mode_val = series.mode().iloc[0] if not series.mode().empty else None

            print("Mean:", mean_val)
            print("Median:", median_val)
            print("Mode:", mode_val)

            # Histogram visualization
            plt.hist(series, bins=20, edgecolor="black")
            plt.title(f"Distribution of {qcol}")
            plt.xlabel(qcol)
            plt.ylabel("Frequency")
            plt.tight_layout()
            plt.show()
else:
    print("\n⚠️ Skipping Exercise 5 (Iris) because Iris dataset is unavailable.")

# Exercise 6: Observation on Sleep dataset

def pick_columns(df: pd.DataFrame, wanted):
    """Return the first matching column for each logical key in 'wanted'."""
    cols = {k: None for k in wanted}
    lower_cols = {c.lower(): c for c in df.columns}
    for key, patterns in wanted.items():
        for p in patterns:
            # direct match
            if p in df.columns:
                cols[key] = p
                break
            # case-insensitive contains
            for lc, orig in lower_cols.items():
                if p.lower() in lc:
                    cols[key] = orig
                    break
            if cols[key]:
                break
    return cols

if sleep_df is not None:
    # Try to find Age, SleepHours, Gender-ish columns even if names differ
    wanted = {
        "age": ["Age", "age", "AGE"],
        "sleep": ["SleepHours", "sleep", "hours", "sleep_hours", "sleep duration"],
        "gender": ["Gender", "gender", "sex", "Sex"],
    }
    found = pick_columns(sleep_df, wanted)
    print("\n=== Exercise 6: Candidate columns for observations (Sleep) ===")
    print(found)

    chosen = [c for c in found.values() if c]
    if chosen:
        print("\nSuggested analyses:")
        if found["age"] and found["sleep"]:
            print("- Trend/group comparison: Does sleep vary with age?")
        if found["gender"] and found["sleep"]:
            print("- Group comparison: Average sleep hours by gender.")
        # Show a quick group preview if possible (no heavy analysis here)
        if found["gender"] and found["sleep"]:
            preview = (
                sleep_df[[found["gender"], found["sleep"]]]
                .dropna()
                .groupby(found["gender"])
                .agg(avg_sleep=(found["sleep"], "mean"), n=(found["sleep"], "count"))
                .sort_values("avg_sleep", ascending=False)
                .head(10)
            )
            print("\nPreview (avg sleep by gender):")
            print(preview)
    else:
        print("Could not guess suitable columns; please check your headers.")
else:
    print("\n⚠️ Skipping Exercise 6 because Sleep dataset is unavailable.")
