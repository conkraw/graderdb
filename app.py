import streamlit as st
import pandas as pd
import io

# Function to handle file upload and save it as a CSV
def save_file_as_csv(uploaded_file):
    # Check file extension to determine whether it's a CSV or Excel file
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_extension == "csv":
            # Read the CSV file directly into a Pandas DataFrame
            df = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            # Read the Excel file into a Pandas DataFrame
            df = pd.read_excel(uploaded_file)
        else:
            raise ValueError("File must be CSV or Excel format.")
        
        # Save it as a CSV in memory (this can also be saved to disk if required)
        csv_file = io.StringIO()
        df.to_csv(csv_file, index=False)
        return csv_file.getvalue(), df
    except Exception as e:
        st.error(f"Error processing the file: {e}")
        return None, None

def main():
    # Title and instructions
    st.title("Clinical Assessment of Student Forms")
    st.write("Please upload the Clinical Assessment of Student Forms file (CSV or Excel format).")
    
    # File uploader (accepting both CSV and XLSX formats)
    uploaded_file = st.file_uploader("Upload Clinical Assessment File (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Save and convert to CSV when file is uploaded
        csv_content, df = save_file_as_csv(uploaded_file)
        
        if csv_content:
            # Display the first few rows of the dataframe as a preview
            st.write("Preview of the data:")
            st.dataframe(df.head())  # Show the first 5 rows of the dataframe

            # Button to go to the next screen
            if st.button("Next"):
                # You can now access the CSV content and df in the next screen
                st.session_state.csv_file = csv_content
                st.session_state.df = df
                st.write("Data has been saved and is ready for processing.")

    # Check if data has been stored in session_state from the previous screen
    if "csv_file" in st.session_state:
        st.write("Accessing saved data from previous step:")
        # Display the data from session state (CSV or dataframe)
        st.write(st.session_state.df)
        st.download_button("Download CSV", st.session_state.csv_file, file_name="clinical_assessment.csv")

if __name__ == "__main__":
    main()

