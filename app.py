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
            #st.write("Preview of the data:")
            #st.dataframe(df.head())  # Show the first 5 rows of the dataframe

            # Button to go to the next screen
            if st.button("Next"):
                # You can now access the CSV content and df in the next screen
                st.session_state.csv_file = csv_content
                st.session_state.df = df
                st.write("Data has been saved and is ready for processing.")

    # Check if data has been stored in session_state from the previous screen
    if "csv_file" in st.session_state:
        COURSE = "Pediatric Clerkship"
        df = df.loc[df['Course'] == COURSE]
        df = df.loc[:, df.columns != 'Course ID']
        
        df2 = df[['Student Email', 'Evaluator', 'Evaluator Email', '2 Multiple Choice Value', '3 Multiple Choice Value', '4 Multiple Choice Value', '5 Multiple Choice Value', '6 Multiple Choice Value', '8 Answer text', '9 Answer text']]
        
        b1='knowledge_for_practice'
        b2='clinical_reasoning'
        b3='communication_ptsfamilies'
        b4='doc_oral'
        b5='communication_care_team'
        b6='sum'
        
        df2.columns.values[0] = "email"
        df2.columns.values[1] = "evaluator"
        df2.columns.values[2] = "evaluator_email"
        df2.columns.values[3] = b1
        df2.columns.values[4] = b2
        df2.columns.values[5] = b3
        df2.columns.values[6] = b4
        df2.columns.values[7] = b5

        df3 = df2[['email',b1,b2,b3,b4,b5]]

        df3.to_csv('OTFconvert.csv',index=False)
        
        df = pd.read_csv('OTFconvert.csv')
        
        xf = round(df.T.fillna(df.mean(numeric_only=True,axis=1)).T,2)
        
        xf.to_csv('OTFconvert.csv',index=False)
        
        xf = pd.read_csv('OTFconvert.csv')
        
        xf['sum'] = xf.sum(axis=1, numeric_only=True)
        
        xf['sum'] = xf['sum']*4
        
        xf['distinct_count'] = xf.groupby(['email'])['email'].transform('count')
        
        xf.to_csv('OTFconvert.csv',index=False)
        
        xf = pd.read_csv('OTFconvert.csv')
        
        lo = xf[xf['distinct_count'] <4]
        
        hi = xf[xf['distinct_count'] >=4]
        
        #REMOVE BLANK EVALS
        hi = hi.loc[hi['sum'] != 0]
        
        min_value = hi.groupby('email')['sum'].min()
        
        hi = hi.merge(min_value, on='email',suffixes=('', '_min'))
        
        hi['sum1'] = hi['sum'].astype(int)
        
        hi['sum_min1'] = hi['sum_min'].astype(int)
        
        hi['min'] = np.where(hi['sum1'] == hi['sum_min1'], 'min', 'not_min')
        
        minmin = hi.loc[hi['min'] == "min"]
        notmin = hi.loc[hi['min'] != "min"]
        
        minmin.to_csv('minmin.csv',index=False)
        
        minmin = pd.read_csv('minmin.csv')
        
        minmin['distinct_countx'] = minmin.groupby('email').cumcount().add(1)
        
        min_value = minmin.groupby('email')['distinct_countx'].min()
        
        minmin = minmin.merge(min_value, on='email',suffixes=('', '_min'))
        
        minmin['distinct_countx'] = minmin['distinct_countx'].astype(int)
        
        minmin['distinct_countx_min'] = minmin['distinct_countx_min'].astype(int)
        
        minmin['minx'] = np.where(minmin['distinct_countx'] == minmin['distinct_countx_min'], 'minx', 'not_minx')
        
        minmin = minmin.loc[minmin['minx'] == "not_minx"]
        
        minmin = minmin[['email','knowledge_for_practice','clinical_reasoning','communication_ptsfamilies','doc_oral','communication_care_team','sum','distinct_count','sum_min','sum1','sum_min1','min']]
        
        hi = pd.concat([minmin,notmin])
        hi = hi[['email','knowledge_for_practice','clinical_reasoning','communication_ptsfamilies','doc_oral','communication_care_team','sum','distinct_count']]
        
        co = pd.concat([hi,lo])
        
        co.to_csv('OTFconvert.csv',index=False)

        
if __name__ == "__main__":
    main()

