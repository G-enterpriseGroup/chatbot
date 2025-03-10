import streamlit as st
import pandas as pd
from io import StringIO
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.title("Paste Excel Data into Grid")

st.markdown("Copy and paste your Excel data below (tab-separated or CSV format):")

# Text area for pasting data
data_input = st.text_area("Paste your data here:")

if data_input:
    # Try reading as tab-separated, fall back to CSV if necessary
    try:
        df = pd.read_csv(StringIO(data_input), sep="\t")
    except Exception:
        df = pd.read_csv(StringIO(data_input), sep=",")

    st.write("Original Data:")
    st.dataframe(df)

    # Configure the grid for editable data
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, groupable=True)
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        height=300,
        fit_columns_on_grid_load=True,
    )

    updated_df = grid_response["data"]
    st.write("Updated Data:")
    st.dataframe(updated_df)
