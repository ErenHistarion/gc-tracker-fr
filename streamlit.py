import time
import streamlit as st
from src.postgresql import select_product_price_availability

st.set_page_config(layout="wide")
st.title("GC Tracker - FR")

while True:
    data = select_product_price_availability()
    if data:
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

    time.sleep(60)
    st.rerun()
