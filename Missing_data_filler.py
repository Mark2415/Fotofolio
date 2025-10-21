import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

# --- Page Configuration ---
st.set_page_config(
    page_title="Data Imputation Tool",
    page_icon="📪",
    layout="wide"
)

# --- Core Function for Imputation ---
def impute_data(df, numeric_method, categorical_method, k_neighbors=5):
    """
    Fills missing values (np.nan) in a DataFrame based on the selected method.
    """
    df_imputed = df.copy()
    
    numeric_cols = df_imputed.select_dtypes(include=np.number).columns
    categorical_cols = df_imputed.select_dtypes(include='object').columns

    # --- Logic for Numeric Method Selection ---
    if numeric_method == "Mean":
        for col in numeric_cols:
            df_imputed[col] = df_imputed[col].fillna(df_imputed[col].mean())
            
    elif numeric_method == "Median":
        for col in numeric_cols:
            df_imputed[col] = df_imputed[col].fillna(df_imputed[col].median())
            
    elif numeric_method == "Mode (Most Frequent Value)":
        for col in numeric_cols:
            if not df_imputed[col].mode().empty:
                df_imputed[col] = df_imputed[col].fillna(df_imputed[col].mode()[0])
                
    elif numeric_method == "KNN Imputer (Most Accurate)":
        if not df_imputed[numeric_cols].empty:
            imputer = KNNImputer(n_neighbors=k_neighbors)
            df_imputed[numeric_cols] = imputer.fit_transform(df_imputed[numeric_cols])
            
    elif numeric_method == "Fill with 0":
        for col in numeric_cols:
            df_imputed[col] = df_imputed[col].fillna(0)

    # --- Logic for Categorical Method Selection ---
    if categorical_method == "Mode (Most Frequent Value)":
        for col in categorical_cols:
            if not df_imputed[col].mode().empty:
                df_imputed[col] = df_imputed[col].fillna(df_imputed[col].mode()[0])
                
    elif categorical_method == "Fill with 'MISSING'":
        for col in categorical_cols:
            df_imputed[col] = df_imputed[col].fillna("MISSING")

    return df_imputed

# --- Streamlit Interface ---
st.title("Statistical Data Imputation App")
st.write("Upload a CSV/Excel file, select a statistical method to fill missing data, and preview the results.")

# 1. File Upload
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "excel"])

# --- ASK USER FOR THE MISSING DATA SYMBOL ---
missing_symbol = st.text_input(
    "What symbol represents empty data in your file?",
    value="(null)", # Default value
    help="Examples: (null), ?, N/A, -, or leave blank if there's no special symbol."
)

# Initialize session state to store data
if 'df_original' not in st.session_state:
    st.session_state.df_original = None
if 'df_imputed' not in st.session_state:
    st.session_state.df_imputed = None

if uploaded_file is not None:
    # Prepare the list of values to be considered NaN
    # We include an empty string '' and the symbol from the user
    na_values_list = ['', missing_symbol]

    try:
        if uploaded_file.name.endswith('.csv'):
            # --- USE 'na_values' PARAMETER ---
            df = pd.read_csv(uploaded_file, na_values=na_values_list)
        else:
            # na_values also works for Excel
            df = pd.read_excel(uploaded_file, na_values=na_values_list)
        
        st.session_state.df_original = df.copy()
        st.session_state.df_imputed = None 
        
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.session_state.df_original = None # Reset on error

# Only display if data has been successfully uploaded
if st.session_state.df_original is not None:
    df_original = st.session_state.df_original
    
    # --- 2. SELECT METHOD (in Sidebar) ---
    st.sidebar.title("🛠️ Method Options")
    
    st.sidebar.header("Numeric Data")
    numeric_method = st.sidebar.selectbox(
        "Select numeric imputation method:",
        ("Mean", "Median", "Mode (Most Frequent Value)", "KNN Imputer (Most Accurate)", "Fill with 0", "Do Not Impute")
    )
    
    k_neighbors = 5
    if numeric_method == "KNN Imputer (Most Accurate)":
        k_neighbors = st.sidebar.slider("Number of neighbors (K)", 1, 15, 5)

    st.sidebar.header("Categorical Data (Text)")
    categorical_method = st.sidebar.selectbox(
        "Select categorical imputation method:",
        ("Mode (Most Frequent Value)", "Fill with 'MISSING'", "Do Not Impute")
    )
    
    if st.sidebar.button("Apply Method", type="primary"):
        with st.spinner("Applying method..."):
            st.session_state.df_imputed = impute_data(
                df_original, 
                numeric_method, 
                categorical_method, 
                k_neighbors
            )
        st.success("Method applied successfully!")

    # --- 3. DISPLAY DATA PREVIEW ---
    st.header("Original Data Preview")
    st.write("Your data before changes (first 10 rows). Pandas will display your empty data as `NaN`.")
    st.dataframe(df_original.head(10), use_container_width=True)
    
    # Display missing data summary
    missing_original = df_original.isnull().sum()
    missing_original = missing_original[missing_original > 0]
    if not missing_original.empty:
        st.subheader("Missing Data Summary (Original)")
        st.write(f"The following columns have `{missing_symbol}` or empty values that have been converted to `NaN`:")
        st.dataframe(missing_original.to_frame(name='Missing Count'), use_container_width=True)
    else:
        st.info("The original dataset has no missing data (`NaN`).")

    # Display results if processed
    if st.session_state.df_imputed is not None:
        df_imputed = st.session_state.df_imputed
        
        st.header("Preview of Imputed Data")
        st.write("Your data after the imputation method has been applied (first 10 rows).")
        st.dataframe(df_imputed.head(10), use_container_width=True)
        
        missing_imputed_count = df_imputed.isnull().sum().sum()
        if missing_imputed_count == 0:
            st.success("All processable data has been filled.")
        else:
            st.warning(f"There are still {missing_imputed_count} missing values. (Perhaps you chose 'Do Not Impute'?)")

        csv = df_imputed.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Imputed Data (CSV)",
            data=csv,
            file_name="imputed_data.csv",
            mime="text/csv",
        )
else:
    st.info("Please upload a CSV or Excel file to begin.")
