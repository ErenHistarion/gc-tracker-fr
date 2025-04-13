import time
import streamlit as st
import pandas as pd
from src.postgresql import select_product_price_availability, select_product_url_monitoring, select_display_product
import plotly.express as px

st.set_page_config(layout="wide")
st.title("GC Tracker - FR")

df = select_display_product()
df_history = pd.DataFrame(df, columns=["product_name", "store_link", "product_price", "last_date", "hour"])
df_history['last_date'] = pd.to_datetime(df_history['last_date'])
df_history['datetime'] = df_history['last_date'] + pd.to_timedelta(df_history['hour'], unit='h')

fig = px.line(
    df_history,
    x='datetime',
    y='product_price',
    color='product_name',
    title="Price History",
    labels={"product_price": "Price (€)", "datetime": "Date and Time"},
    hover_data={"store_link": True, "product_price": False, "datetime": False, "product_name": False}
)
st.plotly_chart(fig, use_container_width=True)


while True:
    data = select_product_price_availability()
    if data:
        st.header("Lower price per product:")
        st.dataframe(
            data,
            use_container_width=True,
            column_config={
                "0": st.column_config.TextColumn("Product name", max_chars=75),
                "1": st.column_config.LinkColumn("Store link"),
                "2": st.column_config.NumberColumn("Price", format="%.2f€"),
                "3": st.column_config.DatetimeColumn("Last seen"),
            },
        )
    else:
        st.write("Aucune donnée disponible.")

    ulrs_monitoring = select_product_url_monitoring()
    if ulrs_monitoring:
        st.header("URLS checked:")
        st.dataframe(
            ulrs_monitoring,
            use_container_width=True,
            column_config={
                "0": st.column_config.TextColumn("Product name", max_chars=75),
                "1": st.column_config.LinkColumn("Store link"),
                "2": st.column_config.CheckboxColumn("Activated"),
            },
        )

    time.sleep(60)
    st.rerun()
