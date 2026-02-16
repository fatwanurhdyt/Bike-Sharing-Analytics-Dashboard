import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Bike Sharing Analytics", page_icon="🚲", layout="wide")
sns.set_theme(style="whitegrid") # Professional plot theme

# 2. Data Caching (Crucial for Dashboard Performance)
@st.cache_data
def load_data():
    # ensure the paths match your directory structure
    day_df = pd.read_csv('dashboard/day_clean.csv')
    hour_df = pd.read_csv('dashboard/hour_clean.csv')
    return day_df, hour_df

day, hour = load_data()

# 3. Sidebar Configuration
st.sidebar.header("📊 Filter Controls")
dataset_option = st.sidebar.selectbox("Select Dataset Granularity:", ["Day", "Hour"])

# determine which dataset is currently active based on selection
data = day if dataset_option == "Day" else hour

# --- season filter ---
if dataset_option == "Day":
    season_option = st.sidebar.multiselect(
        "Select Season:",
        options=data["season"].unique(),
        default=data["season"].unique()
    )
    data = data[data["season"].isin(season_option)]

# --- weather filter ---
weather_option = st.sidebar.multiselect(
    "Select Weather Condition:",
    options=data["weathersit"].unique(),
    default=data["weathersit"].unique()
)
data = data[data["weathersit"].isin(weather_option)]

# --- day type filter (hour dataset) ---
if dataset_option == "Hour":
    day_type = st.sidebar.radio(
        "Select Day Type:",
        options=["Weekday", "Weekend", "All"],
        index=2  # Default to All
    )

    weekday_days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
    weekend_days = ["saturday", "sunday"]

    if day_type == "Weekday":
        data = data[data["weekday"].isin(weekday_days)]
    elif day_type == "Weekend":
        data = data[data["weekday"].isin(weekend_days)]

# --- color palette filter ---
if dataset_option == "Day":
    selected_palette = st.sidebar.selectbox("Select Temperature Color Palette:", ["viridis", "coolwarm"])

# 4. main dashboard ui
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("An interactive dashboard to explore and analyze bike rental trends based on temporal and environmental factors.")

# display data dictionary in an expander to save space
with st.expander("📖 View Data Dictionary"):
    data_dictionary = {
        "Feature": ["instant", "dteday", "season", "hr", "holiday", "weekday", "workingday", "weathersit",
                  "temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"],
        "Description": [
            "Unique index for each record",
            "Date in YYYY-MM-DD format",
            "Season category",
            "Hour of the day (0-23)",
            "Public holiday indicator",
            "Day of the week",
            "Working day indicator",
            "Weather condition category",
            "Normalized actual temperature (0-1)",
            "Normalized feeling temperature (0-1)",
            "Normalized humidity level (0-1)",
            "Normalized wind speed (0-1)",
            "Count of casual (unregistered) users",
            "Count of registered users",
            "Total bike rentals (casual + registered)"
        ]
    }
    st.table(pd.DataFrame(data_dictionary))

st.subheader("Raw Data Preview")
st.dataframe(data.head(100), use_container_width=True) # Displaying top 100 to prevent browser lag

st.divider()

# 5. visualizations & insights



# --- question 1: hourly trends ---
if dataset_option == "Hour":
    st.subheader("⏰ Hourly Bike Rental Trends")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=data, x='hr', y='cnt', estimator='mean', errorbar=None, marker='o', ax=ax, color="#1f77b4")
    
    ax.set_xlabel("Hour of the Day (24H Format)")
    ax.set_ylabel("Average Bike Rentals")
    ax.set_title("Average Bike Usage Throughout the Day")
    ax.set_xticks(range(0, 24))
    st.pyplot(fig)

    st.markdown("""
    #### 💡 Actionable Insights:
    The hourly analysis reveals distinct peak periods for bike utilization:
    - **08:00 AM:** Significant spike aligning with morning commute hours (work/school).
    - **05:00 PM - 06:00 PM (17:00-18:00):** Highest peak corresponding to evening rush hour.
    - *Note:* These commute peaks flatten out during weekends when work/school routines are paused.

    **Recommendation:** Fleet management should ensure **maximum bike availability and logistical rebalancing** at major transit hubs and residential areas right before these peak windows (07:30 AM and 04:30 PM) to meet high user demand.
    """)

# --- question 2: seasonal trends ---
if dataset_option == "Day":
    st.subheader("🌦️ Seasonal Impact on Bike Rentals")
    
    # grouping data
    seasonal_usage = data.groupby('season')['cnt'].sum().reset_index()
    season_order = ['winter', 'spring', 'summer', 'fall']
    seasonal_usage['season'] = pd.Categorical(seasonal_usage['season'], categories=season_order, ordered=True)
    seasonal_usage = seasonal_usage.sort_values('season')
    
    # plotting
    season_colors = ['#1f77b4', '#2ca02c', '#d62728', '#ff7f0e'] # Professional hex colors
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(seasonal_usage['season'], seasonal_usage['cnt'], color=season_colors)
    
    ax.set_title("Total Bike Rentals Across Seasons")
    ax.set_xlabel("Season")
    ax.set_ylabel("Total Rentals (Count)")
    st.pyplot(fig)

    st.markdown("""
    #### 💡 Actionable Insights:
    The visualization clearly indicates a strong correlation between seasons and bike usage:
    - 🌞 **Summer:** Records the absolute highest volume of total rentals.
    - ❄️ **Winter:** Experiences the most significant drop in usage.
    
    The data suggests a strong user preference for warmer, comfortable weather. The summer peak is likely amplified by summer holidays and increased outdoor recreational activities.

    **Recommendation:** Inventory planning and maintenance schedules should be deeply integrated with seasonal forecasting. Winter provides an optimal window for **fleet-wide maintenance and repairs**, while summer requires the entire fleet to be deployed and fully operational.
    """)

    st.divider()

    # --- advanced analysis: temperature impact ---
    # create temperature bins
    bins = [0, 0.3, 0.6, 1] 
    labels = ["Cold", "Moderate", "Hot"]
    # safely assign without settingwithcopywarning by operating on the original 'day' dataframe temporarily
    temp_data = data.copy()
    temp_data["temp_category"] = pd.cut(temp_data["temp"], bins=bins, labels=labels)

    # grouping
    usage_by_temp = temp_data.groupby("temp_category", observed=False)["cnt"].sum().reset_index()

    st.subheader("🌡️ Bike Usage by Temperature Categories")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="temp_category", y="cnt", data=usage_by_temp, palette=selected_palette, ax=ax)
    
    ax.set_title("Total Rentals Segmented by Normalized Temperature")
    ax.set_xlabel("Temperature Category")
    ax.set_ylabel("Total Rentals (Count)")
    st.pyplot(fig)

    st.markdown("""
    #### 💡 Actionable Insights:
    Further segmenting the data by temperature categories yields more granular operational insights:
    - ❄️ **Cold:** Minimal rental activity.
    - 🌤️ **Moderate:** The sweet spot generating the highest rental volume.
    - ☀️ **Hot:** Sustains high usage, though slightly lower than moderate conditions (likely due to extreme heat discomfort).

    **Recommendation:**
    - **Cold Conditions:** Implement dynamic pricing or targeted promotional discounts to incentivize ridership and stabilize revenue during low-demand periods.
    - **Moderate/Hot Conditions:** Suspend discounts and focus on maximizing fleet availability to capture full-price revenue from high organic demand.
    """)