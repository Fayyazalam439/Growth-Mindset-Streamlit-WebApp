import streamlit as st
import pandas as pd
import os
from io import BytesIO

#Set up our app
st.set_page_config(page_title="📀 Data sweeper", layout='wide')

#custom css
st.markdown(
    """
    <style>
    .stApp{
        backgroung-color: black;
        color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
)


st.title("📀 Data sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload you files (CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else: 
            st.error(f"Unsupported file type: {file_ext}")
            continue

        #Display info about the file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

        #Show 5 rows of our df
        st.write("🔎Preview the Head of the Dataframe")
        st.dataframe(df.head())

        #Option for data cleaning
        st.subheader("🔧Data Cleaning Option")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")
            
            with col2:
                if st.button(f"Fill Missing Value for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df [numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Value have been Filled!")

        #Choose specific columns to Keep or Convert
        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #Create Some Visulizations
        st.subheader("🔗 Data Visulization")
        if st.checkbox(f"Show Visulization for{file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        #Convert the File -> CSV to Excel
        st.subheader("🔗 Conversion Options")
        Conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if Conversion_type == "CSV":
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext,".csv")
                mime_type = "text/csv"

            elif Conversion_type == "Excel":
                df.to_excel(buffer,index=False)
                file_name = file.name.replace(file_ext,".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            #Download Button
            st.download_button(
                label=f"Download {file.name} as {Conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type 
            )

st.success("🎉 Files processed successfully! 🎉")                
