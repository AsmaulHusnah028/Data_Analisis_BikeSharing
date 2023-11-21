import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency

sns.set(style="dark")

# Load your datasets

df_day = pd.read_csv("df_hour_filtered.csv")


def create_daily_rental_df(df_day):
    daily_rental_df = df_day.resample(rule="D", on="dteday").agg({"cnt": "sum"})
    daily_rental_df = daily_rental_df.reset_index()
    daily_rental_df.rename(
        columns={"dteday": "Rental_day", "cnt": "Rental_count"}, inplace=True
    )

    return daily_rental_df


def create_by_weekday(df_day):
    by_week = df_day.groupby(by="weekday")["cnt"].nunique().reset_index()
    by_week.rename(columns={"cnt": "Jumlah_sewa"}, inplace=True)

    return by_week


def create_by_season(df_day):
    season_df = df_day.groupby("season").agg({"cnt": "sum"}).reset_index()

    season_df.rename(
        columns={
            "cnt": "Rental_count",
        },
        inplace=True,
    )
    return season_df


def create_by_weathersit(df_day):
    weathersit_df = df_day.groupby("weathersit").agg({"cnt": "sum"}).reset_index()

    weathersit_df.rename(
        columns={
            "cnt": "Rental_count",
        },
        inplace=True,
    )
    return weathersit_df


# def create_by_type(df_day):
#     casual_mean = df_day["casual"].mean()
#     registered_mean = df_day["registered"].mean()

#     # Pastikan bahwa casual_mean dan registered_mean adalah nilai tunggal
#     casual_mean = casual_mean if not pd.isna(casual_mean) else 0
#     registered_mean = registered_mean if not pd.isna(registered_mean) else 0

#     mean_users_data = {
#         "User Type": ["Casual", "Registered"],
#         "Mean Rentals": [casual_mean, registered_mean],
#     }

#     df_mean_users = pd.DataFrame(mean_users_data)

#     return df_mean_users


datetime_columns = ["dteday"]
df_day.sort_values(by=["dteday"], inplace=True)
df_day.reset_index(inplace=True)

for column in datetime_columns:
    df_day[column] = pd.to_datetime(df_day[column])

min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()

with st.sidebar:
    

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

main_df = df_day[
    (df_day["dteday"] >= str(start_date)) & (df_day["dteday"] <= str(end_date))
]

daily_rental_df = create_daily_rental_df(main_df)
by_weekday = create_by_weekday(main_df)
by_season = create_by_season(main_df)
by_weathersit = create_by_weathersit(main_df)

st.header("Bike Rental Dashboard :sparkles:")

st.subheader("Daily Rental")

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_rental_df.Rental_count.sum()
    st.metric("Total Sewa", value=total_orders)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rental_df["Rental_day"],
    daily_rental_df["Rental_count"],
    marker="o",
    linewidth=2,
    color="#90CAF9",
)
ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=15)

st.pyplot(fig)

st.subheader("Rental Demographics")

col1, col2 = st.columns(2)

with col1:
    # Code for creating the bar plot
    st.header("Weather Situation Rental Count")

    # Bar plot using Seaborn
    fig_weather_situation = plt.figure(figsize=(12, 8))
    sns.barplot(
        x="weathersit", y="Rental_count", data=by_weathersit, palette="viridis"
    )
    plt.title("Rental Count by Weather Situation", fontsize=18)
    plt.xlabel("Weather Situation")
    plt.ylabel("Rental Count")

    # Show the bar plot in Streamlit
    st.pyplot(fig_weather_situation)


with col2:
    by_season["season"] = by_season["season"].map(
        {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    )

    # Data untuk pie chart
    labels = by_season["season"]
    sizes = by_season["Rental_count"]

    # Warna yang sesuai dengan jumlah musim
    colors = ["lightcoral", "lightblue", "lightgreen", "lightsalmon"]

    # Membuat pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)

    # Menambahkan judul
    ax.set_title("Rental Count by Season")

    # Menampilkan pie chart
    st.pyplot(fig)


fig, ax = plt.subplots(figsize=(20, 10))
# Mapping nilai weekday menjadi nama hari
by_weekday["weekday"] = by_weekday["weekday"].map(
    {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
    }
)


colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Membuat bar chart menggunakan Seaborn
sns.barplot(
    y="weekday",
    x="Jumlah_sewa",
    data=by_weekday.sort_values(by="Jumlah_sewa", ascending=False),
    palette=colors_,
)

plt.title("Number of Customer by Weekday", loc="center", fontsize=35)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis="x", labelsize=25)

st.pyplot(fig)


st.caption("Copyright © Asmaul_husnah")
