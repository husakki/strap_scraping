import json

import pandas as pd
import streamlit as st

st.title("Collection of watch straps")
st.write("This is a collection of watch straps scraped from https://www.watch-tools.de")

with open("../scrapy_output/allstraps.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    
df = pd.DataFrame(data)

st.dataframe(df, column_config={"link": st.column_config.LinkColumn("Link", display_text="Open link", width="small"), "price": st.column_config.NumberColumn("Price", format="%f €", width="small")})