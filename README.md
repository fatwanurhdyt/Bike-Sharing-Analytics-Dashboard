# 🚲 Bike Sharing Data Analytics & Dashboard

**Author:** Fatwa Nurhidayat  
**Focus:** Exploratory Data Analysis (EDA), Data Wrangling, and Interactive Dashboarding.

---

## 📊 Project Overview
This repository contains an end-to-end data analytics project focused on the micromobility sector. Utilizing a comprehensive Bike Sharing dataset, this project aims to uncover actionable operational insights regarding user demand, temporal patterns, and environmental influences. 

The project is divided into two main components:
1. **Data Analytics Pipeline (`notebook.ipynb`):** A robust Jupyter Notebook detailing the data wrangling process (handling anomalies via Winsorization), exploratory data analysis (EDA), and advanced feature engineering.
2. **Interactive Dashboard (`dashboard.py`):** A dynamic, user-friendly web application built with **Streamlit** that allows stakeholders to visually explore the data through various filters (Season, Weather, Day Type).

---

## 🌐 Live Dashboard
You can access the interactive dashboard here:  
👉 **[Insert Your Streamlit App URL Here]**

---

## 💡 Key Strategic Insights
Based on the analysis, several key business recommendations were generated:
- **Fleet Rebalancing:** Rental demand spikes heavily at **08:00 AM** and **17:00-18:00 PM** (commuting hours). Fleet operations must ensure maximum availability prior to these windows.
- **Seasonal Maintenance:** Summer drives the absolute highest volume of rentals, while winter sees a massive drop-off. Winter provides the optimal window for fleet-wide mechanical overhauls.
- **Weather-Based Dynamic Pricing:** Ridership plummets in cold conditions but remains highly resilient in hot weather. Dynamic pricing (discounts) is recommended during cold snaps to stabilize revenue.

---

## 📂 Repository Structure
```text
bike-sharing-analytics/
├── data/
│   ├── day.csv             <-- Raw daily dataset
│   └── hour.csv            <-- Raw hourly dataset
├── dashboard/
│   ├── day_clean.csv       <-- Processed daily data for dashboard
│   └── hour_clean.csv      <-- Processed hourly data for dashboard
├── notebook.ipynb          <-- Main analytical pipeline
├── dashboard.py            <-- Streamlit application script
├── requirements.txt        <-- Project dependencies
└── README.md