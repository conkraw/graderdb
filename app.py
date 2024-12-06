import streamlit as st
import pandas as pd
import numpy as np
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
    import streamlit as st
    import pandas as pd
    import numpy as np
    import io
    st.title("Clinical Assessment of Student Forms")
    st.write("Please upload the Clinical Assessment of Student Forms files (CSV or Excel format).")

    # File uploader for the second file (accepting both CSV and XLSX formats)
    #uploaded_file_1 = st.file_uploader("Upload Record ID Mapper (CSV or Excel)", type=["csv", "xlsx"])
    
    # File uploader for the first file (accepting both CSV and XLSX formats)
    uploaded_file_2 = st.file_uploader("Upload Clinical Assessment File (CSV or Excel)", type=["csv", "xlsx"])

    # File uploader for the first file (accepting both CSV and XLSX formats)
    uploaded_file_3 = st.file_uploader("Upload Clinical Encounters File (CSV or Excel)", type=["csv", "xlsx"])

    # File uploader for the first file (accepting both CSV and XLSX formats)
    uploaded_file_4 = st.file_uploader("Observed Handoff(CSV or Excel)", type=["csv", "xlsx"])

    # File uploader for the first file (accepting both CSV and XLSX formats)
    uploaded_file_5 = st.file_uploader("Observed HP(CSV or Excel)", type=["csv", "xlsx"])
    
    #if uploaded_file_1 is not None and uploaded_file_2 and uploaded_file_3 and uploaded_file_4 and uploaded_file_5 is not None:
    if uploaded_file_2 and uploaded_file_3 and uploaded_file_4 and uploaded_file_5 is not None:
        # Save and convert the first file to CSV when uploaded
        #csv_content_1, df_1 = save_file_as_csv(uploaded_file_1)
        
        csv_content_2, df_2 = save_file_as_csv(uploaded_file_2)

        csv_content_3, df_3 = save_file_as_csv(uploaded_file_3)
        
        csv_content_4, df_4 = save_file_as_csv(uploaded_file_4)
        
        csv_content_5, df_5 = save_file_as_csv(uploaded_file_5)
        
        #if csv_content_1 and csv_content_2 and csv_content_3:
        if csv_content_2 and csv_content_3 and csv_content_4 and csv_content_5:
            # Display the first few rows of each dataframe as a preview
            #st.write("Preview of File 1 Data:")
            #st.dataframe(df_1.head())  # Show the first 5 rows of the first file

            #st.write("Preview of File 2 Data:")
            #st.dataframe(df_2.head())  # Show the first 5 rows of the second file

            #st.write("Preview of File 3 Data:")
            #st.dataframe(df_3.head())  # Show the first 5 rows of the second file
            
            # Button to go to the next screen
            if st.button("Next"):
                # You can now access the CSV content and df of both files in the next screen
                #st.session_state.csv_file_1 = csv_content_1
                #st.session_state.df_1 = df_1
                
                st.session_state.csv_file_2 = csv_content_2
                st.session_state.df_2 = df_2

                st.session_state.csv_file_3 = csv_content_3
                st.session_state.df_3 = df_3

                st.session_state.csv_file_4 = csv_content_4
                st.session_state.df_4 = df_4

                st.session_state.csv_file_5 = csv_content_5
                st.session_state.df_5 = df_5
                
                st.write("Files have been saved and are ready for processing.")
                
    #elif uploaded_file_1 is None or uploaded_file_2 or uploaded_file_3 or uploaded_file_4 or uploaded_file_5 is None:
    elif uploaded_file_2 or uploaded_file_3 or uploaded_file_4 or uploaded_file_5 is None:
        st.warning("Please upload ALL files to proceed.")

    # Check if data has been stored in session_state from the previous screen
    #if "csv_file_1" in st.session_state and "csv_file_2" and "csv_file_3" and "csv_file_4" and "csv_file_5" in st.session_state:
    if "csv_file_2" and "csv_file_3" and "csv_file_4" and "csv_file_5" in st.session_state: 
        data = st.secrets["dataset"]["data"]
        dfx = pd.DataFrame(data)
        dfx.to_csv('recordidmapper.csv', index=False)

        #df_1.to_csv('recordidmapper.csv',index=False)
        df_2.to_csv('00 - originaloasis.csv',index=False)
        df_3.to_csv('00 - export_results.csv',index=False)
        df_4.to_csv('00 - originalhandoff.csv',index=False)
        df_5.to_csv('00 - originalobservedHP.csv',index=False)
        
        observed = df_3.loc[df_3['*Peds Level of Responsibility'] == 'Observed [Please briefly describe the experience to help us determine why students were limited to only observing during this encounter]']
        observed = observed.loc[(observed['Item'] != '*(Peds) Health Systems Encounter')&(observed['Item'] != '*(Peds) Humanities Encounter')]
        observed.to_csv('00 - observed_report.csv',index=False)
        
        COURSE = "Pediatric Clerkship"
        df_2 = df_2.loc[df_2['Course'] == COURSE]
        df_2 = df_2.loc[:, df_2.columns != 'Course ID']
        
        df2 = df_2[['Student Email', 'Evaluator', 'Evaluator Email', '2 Multiple Choice Value', '3 Multiple Choice Value', '4 Multiple Choice Value', '5 Multiple Choice Value', '6 Multiple Choice Value', '8 Answer text', '9 Answer text']]
        
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
        
        import streamlit as st
        import pandas as pd
        import numpy as np
        import io
        
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

        FILETOMAP = "OTFconvert.csv"
        RECORDIDMAPPER = 'recordidmapper.csv'
        COLUMN = 'email'

        import csv
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[2] for rows in reader} 
            
        df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        first_column = df.pop('record_id')
        
        df.insert(0, 'record_id', first_column)
        
        df.to_csv(FILETOMAP,index=False)
        
        df = pd.read_csv('OTFconvert.csv')
        
        t1=df.loc[df[(b1)]!=0]
        t2=df.loc[df[(b2)]!=0]
        t3=df.loc[df[(b3)]!=0]
        t4=df.loc[df[(b4)]!=0]
        t5=df.loc[df[(b5)]!=0]
        t6=df.loc[df[(b6)]!=0]
        
        x1=t1.groupby('record_id').mean(numeric_only=True)[b1].round(2)
        x2=t2.groupby('record_id').mean(numeric_only=True)[b2].round(2)
        x3=t3.groupby('record_id').mean(numeric_only=True)[b3].round(2)
        x4=t4.groupby('record_id').mean(numeric_only=True)[b4].round(2)
        x5=t5.groupby('record_id').mean(numeric_only=True)[b5].round(2)
        x6=t6.groupby('record_id').mean(numeric_only=True)[b6].round(2)
        
        
        x1.to_csv(b1+".csv")
        x2.to_csv(b2+".csv")
        x3.to_csv(b3+".csv")
        x4.to_csv(b4+".csv")
        x5.to_csv(b5+".csv")
        x6.to_csv(b6+".csv")
        
        xx=df[['record_id']]
        
        yy = xx.drop_duplicates(subset=['record_id'])
        
        yy.to_csv('OTF_averages.csv',index=False)
        
        FILETOMAP = "OTF_averages.csv"
        RECORDIDMAPPER = b1+".csv"
        COLUMN = 'record_id'
        
        import pandas as pd
        import numpy as np
        import csv
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df[(b1)] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        df = pd.read_csv(FILETOMAP,dtype=str)
        
        FILETOMAP = "OTF_averages.csv"
        RECORDIDMAPPER = b2+".csv"
        COLUMN = 'record_id'
        
        import pandas as pd
        import numpy as np
        import csv
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df[(b2)] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        df = pd.read_csv(FILETOMAP,dtype=str)
        
        FILETOMAP = "OTF_averages.csv"
        RECORDIDMAPPER = b3+".csv"
        COLUMN = 'record_id'
        
        import pandas as pd
        import numpy as np
        import csv
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df[(b3)] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        df = pd.read_csv(FILETOMAP,dtype=str)
        
        FILETOMAP = "OTF_averages.csv"
        RECORDIDMAPPER = b4+".csv"
        COLUMN = 'record_id'
        
        import pandas as pd
        import numpy as np
        import csv
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df[(b4)] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        df = pd.read_csv(FILETOMAP,dtype=str)
        
        FILETOMAP = "OTF_averages.csv"
        RECORDIDMAPPER = b5+".csv"
        COLUMN = 'record_id'
        
        import pandas as pd
        import numpy as np
        import csv
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df[(b5)] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        df = pd.read_csv(FILETOMAP,dtype=str)
        
        FILETOMAP = "OTF_averages.csv"
        RECORDIDMAPPER = b6+".csv"
        COLUMN = 'record_id'
        
        import pandas as pd
        import numpy as np
        import csv
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df[(b6)] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        df = pd.read_csv('OTFconvert.csv')
        df = df.groupby('record_id')['distinct_count'].min()
        df.to_csv('distinct_count.csv')
        
        FILETOMAP = "OTF_averages.csv"
        RECORDIDMAPPER = 'distinct_count'+".csv"
        COLUMN = 'record_id'
        
        import pandas as pd
        import numpy as np
        import csv
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df[('distinct_count')] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        import pandas as pd
        
        df = pd.read_csv('00 - originaloasis.csv')
        
        df = df.loc[df['Course'] == COURSE]
        
        df = df.loc[:, df.columns != 'Course ID']
        
        
        df = df[['Student Email', '7 Multiple Choice Label']]
        
        df['email'] = df['Student Email'].astype(str)
        df['prof'] = df['7 Multiple Choice Label'].astype(str)
        
        df = df[['email','prof']]
        
        
        x = df.loc[df['prof'] == 'Concern: Exhibited lapse(s) in professional behaviors (honesty, integrity, accountability, reliability, adhering to ethical norms)']
        
        st.dataframe(x)
        
        df.to_csv('prof.csv',index=False)
        
        
        FILETOMAP = "prof.csv"
        RECORDIDMAPPER = 'recordidmapper.csv'
        COLUMN = 'email'
    
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[2] for rows in reader} 
            
        df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        first_column = df.pop('record_id')
        
        df.insert(0, 'record_id', first_column)
        
        df.to_csv(FILETOMAP,index=False)
        
        df = pd.read_csv('prof.csv')
        
        df = df[['record_id','prof']]
        
        meets = df.loc[df['prof'] == 'No Concern: Awareness of ethical norms with a commitment to ethical behavior.   Strives to act with honesty, integrity, accountability, reliability. May have a perceived lapse in professional behavior, which student rapidly corrects.']
        does_not_meet = df.loc[df['prof'] == 'Concern: Exhibited lapse(s) in professional behaviors (honesty, integrity, accountability, reliability, adhering to ethical norms)']
        
        meets.to_csv('meets.csv', index=False)
        meets = pd.read_csv('meets.csv')
        meets['meets'] = meets['prof'].astype(str)
        
        does_not_meet.to_csv('does_not_meet.csv', index=False)
        does_not_meet = pd.read_csv('does_not_meet.csv')
        does_not_meet['does_not_meet'] = does_not_meet['prof'].astype(str)
        
        meets = meets.groupby('record_id')['meets'].count()
        does_not_meet = does_not_meet.groupby('record_id')['does_not_meet'].count()
        
        meets.to_csv('meets.csv')
        does_not_meet.to_csv('does_not_meet.csv')

        df=pd.read_csv('OTF_averages.csv',dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('meets.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df[('meets')] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv('OTF_averages.csv',index=False)
        
        df=pd.read_csv('OTF_averages.csv',dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('does_not_meet.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df[('does_not_meet')] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv('OTF_averages.csv',index=False)
        
        df = pd.read_csv('00 - originaloasis.csv')
        
        df = df.loc[df['Course'] == COURSE]
        
        df = df[['Student Email','8 Answer text','9 Answer text']]
        
        df.to_csv('comments.csv',index=False)
        
        df=pd.read_csv('comments.csv',dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[2] for rows in reader} 
        
        df[('record_id')] = df['Student Email'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df['strengths'] = df['8 Answer text'].astype(str)
        df['weaknesses'] = df['9 Answer text'].astype(str)
        
        df = df[['record_id','strengths','weaknesses']]
        
        df.to_csv('comments.csv',index=False)
        
        df = pd.read_csv('comments.csv')
        
        df['strengths'] = df['strengths'].astype(str)
        
        strengths = df.groupby('record_id', group_keys=False)['strengths'].apply('\n'.join).reset_index()
        
        df['weaknesses'] = df['weaknesses'].astype(str)
        
        weaknesses = df.groupby('record_id', group_keys=False)['weaknesses'].apply('\n'.join).reset_index()
        
        strengths.to_csv('strengths.csv',index=False)
        
        weaknesses.to_csv('weaknesses.csv',index=False)
        
        df=pd.read_csv('OTF_averages.csv',dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('strengths.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df[('strengths')] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv('OTF_averages.csv',index=False)
        
        import pandas as pd
        import numpy as np
        import csv
        df=pd.read_csv('OTF_averages.csv',dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('weaknesses.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df[('weaknesses')] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv('OTF_averages.csv',index=False)
        
        import pandas as pd 
        df = pd.read_csv('OTF_averages.csv')
        df.to_csv('x03 - oasissubmission.csv',index=False)
        
        df = pd.read_csv('00 - originaloasis.csv')
        
        df = df.loc[df['Course'] == "Pediatric Clerkship"]
        
        #df = df.loc[df['Course'] == "Testing for Peds QR Eval"]
        
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
        df = df.loc[(df['knowledge_for_practice'] <= 2)|
                    (df['clinical_reasoning'] <= 2)|
                    (df['communication_ptsfamilies'] <= 2)|
                    (df['doc_oral'] <= 2)|
                    (df['communication_care_team'] <= 2)
                   ]
        df.to_csv("low_evals.csv",index=False)
        
        st.dataframe(df)
        
        df = pd.read_csv('00 - originaloasis.csv')
        
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
        df2.columns.values[8] = "strengths"
        df2.columns.values[9] = "weaknesses"
        
        df = df2
        
        df = df.loc[(df['knowledge_for_practice'] <= 2)|
                    (df['clinical_reasoning'] <= 2)|
                    (df['communication_ptsfamilies'] <= 2)|
                    (df['doc_oral'] <= 2)|
                    (df['communication_care_team'] <= 2)]
        
        df = df[['email','evaluator','strengths','weaknesses']]
        
        st.dataframe(df)
        ##########################################################################CLINICAL_ENCOUNTERS##########################################################################
        import datetime
        import os
        import pandas as pd
        import numpy as np
        import datetime
        
        df = pd.read_csv('00 - export_results.csv') 
        date = '2024-03-11 00:00:00' 
        df['Start Date'] = pd.to_datetime(df["Start Date"])
        df = df[df['Start Date'] >= date]
        df.to_csv('00 - export_results.csv',index=False)
        
        df = df[['Email', 'Start Date', 'Item', '*Peds Level of Responsibility', 'Time entered']]
        
        # List of all items that should appear as columns
        items = [
            '*(Peds) Health Supervision/Well Child Visit',
            '*(Peds) Common Newborn Conditions (Clinical Domains)',
            '*(Peds) Dermatologic Conditions (Clinical Domains)',
            '*(Peds) Gastro-intestinal (Clinical Domains)',
            '*(Peds) Behavior (Clinical Domains)',
            '*(Peds) Upper and Lower Respiratory Tract (Clinical Domains) ', 
            '*(Peds) Acute conditions (Clinical Domains)',
            '*(Peds) Other (Clinical Domains)',
            '*(Peds) Procedure Interpretations',
            '*(Peds) Health Systems Encounter',
            '*(Peds) Humanities Encounter'
        ]
        
        # The mapping for renaming columns
        rename_dict = {
            '*(Peds) Health Supervision/Well Child Visit': 'clindom_well_child',
            '*(Peds) Common Newborn Conditions (Clinical Domains)': 'clindom_commonnb',
            '*(Peds) Dermatologic Conditions (Clinical Domains)': 'clindom_derm',
            '*(Peds) Gastro-intestinal (Clinical Domains)': 'clindom_gi',
            '*(Peds) Behavior (Clinical Domains)': 'clindom_behavior',
            '*(Peds) Upper and Lower Respiratory Tract (Clinical Domains) ': 'clindom_upperandlowerrt',
            '*(Peds) Acute conditions (Clinical Domains)': 'clindom_acuteconditions',
            '*(Peds) Other (Clinical Domains)': 'clindom_other',
            '*(Peds) Procedure Interpretations': 'clindom_testinterpret',
            '*(Peds) Health Systems Encounter': 'clindom_healthsystems',
            '*(Peds) Humanities Encounter': 'clindom_humanities'
        }
        
        # Count occurrences of each unique 'Item' per 'Email' for all encounters
        item_counts = df.groupby(['Email', 'Item']).size().unstack(fill_value=0)
        
        # Reindex the item_counts dataframe to ensure all items appear as columns
        item_counts = item_counts.reindex(columns=items, fill_value=0)
        
        # Rename the columns according to the mapping
        item_counts = item_counts.rename(columns=rename_dict)
        
        # Count the number of "Performed" or "Assisted" encounters
        # Create a "Performed" count column (including "Performed" and "Assisted")
        performed_counts = df[df['*Peds Level of Responsibility'].isin(['Performed', 'Assisted'])].groupby('Email').size()
        
        # Count the number of "Observed" encounters
        observed_counts = df[df['*Peds Level of Responsibility'] == 'Observed [Please briefly describe the experience to help us determine why students were limited to only observing during this encounter]'].groupby('Email').size()
        
        # Merge the counts into the item_counts dataframe
        item_counts['performed'] = item_counts.index.map(performed_counts).fillna(0).astype(int)
        item_counts['observed'] = item_counts.index.map(observed_counts).fillna(0).astype(int)
        
        # Convert 'Time entered' to datetime format
        df['Time entered'] = pd.to_datetime(df['Time entered'], format='%m/%d/%Y %I:%M:%S %p')
        
        # Find the maximum 'Time entered' for each email
        max_time = df.groupby('Email')['Time entered'].max().reset_index()
        
        # Rename the 'Time entered' column to 'max_time_entered'
        max_time = max_time.rename(columns={'Time entered': 'max_time_entered'})
        
        # Merge the 'max_time_entered' back into the item_counts dataframe
        item_counts = pd.merge(item_counts, max_time, on='Email', how='left')
        
        # Create 'submitted_ce' column based on the max 'Time entered' column
        item_counts['submitted_ce'] = item_counts['max_time_entered'].dt.strftime('%m-%d-%Y 23:59')
        
        # Drop the 'max_time_entered' column after creating 'submitted_ce'
        item_counts = item_counts.drop(columns=['max_time_entered'])
        
        # Reset index to match the original DataFrame structure
        item_counts.reset_index(inplace=False)

        item_counts.to_csv('x01 - clinical_domains.csv',index=False)

        FILETOMAP = "x01 - clinical_domains.csv"
        RECORDIDMAPPER = 'recordidmapper.csv'
        COLUMN = 'Email'
        
        import pandas as pd
        import numpy as np
        import csv
        
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[2] for rows in reader} 
            
        df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        first_column = df.pop('record_id')
        
        df.insert(0, 'record_id', first_column)
        
        df = df.loc[df['Email'] != 'x']
        
        df.to_csv(FILETOMAP,index=False)
    
        df = pd.read_csv('00 - export_results.csv') 

        # Select relevant columns
        df = df[['Email', 'Start Date', 'Item', '*Peds Level of Responsibility']]
        
        df = df.loc[(df['Item']!='*(Peds) Health Systems Encounter')&(df['Item']!='*(Peds) Humanities Encounter')]
        
        # Filter rows where *Peds Level of Responsibility is "Observed"
        df_observed = df.loc[df['*Peds Level of Responsibility'] == 
                             "Observed [Please briefly describe the experience to help us determine why students were limited to only observing during this encounter]"]
        
        # Now, find students who have "Assisted" or "Performed" for the same Item
        df_assisted_performed = df.loc[df['*Peds Level of Responsibility'].isin(['Assisted', 'Performed'])]
        
        # Merge the two dataframes on Email and Item to find cases where the same student has both "Observed" and "Assisted"/"Performed"
        merged = pd.merge(df_observed, df_assisted_performed, on=['Email', 'Item'], how='inner')
        
        # Get the Email and Item combinations where we found both "Observed" and "Assisted"/"Performed"
        excluded_items = merged[['Email', 'Item']].drop_duplicates()
        
        # Filter out those combinations from the original observed dataframe
        df_filtered = df_observed[~df_observed[['Email', 'Item']].isin(excluded_items.to_dict('list')).all(axis=1)]
        
        # Save the resulting DataFrame to a new CSV
        df_filtered.to_csv('observed_report_filtered.csv', index=False)
        
        st.dataframe(df_filtered)
        ##############################################OBSERVED HO##############################################
        import pandas as pd
        import numpy as np
        import csv
        df = df_4
        
        df = pd.read_csv('00 - originalhandoff.csv')
        
        df = df.loc[df['Course'] == "Pediatric Clerkship"]
        
        #df = df.loc[df['Course'] == "Testing for Peds QR Eval"]
        
        df = df[['Student Email','1 Multiple Choice Value','2 Multiple Choice Value']]
        
        df.to_csv('ho_lor.csv',index=False)
        
        df['obho_submissions'] = 1
        
        df['email'] = df['Student Email'].astype(str)
        
        df.to_csv('observedho.csv',index=False)
        
        FILETOMAP = "observedho.csv"
        RECORDIDMAPPER = 'recordidmapper.csv'
        COLUMN = 'email'
        
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[2] for rows in reader} 
            
        df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        first_column = df.pop('record_id')
        
        df.insert(0, 'record_id', first_column)
        
        df.to_csv(FILETOMAP,index=False)
        
        df=pd.read_csv(FILETOMAP,dtype=str)
        
        df.dropna(subset=['record_id'], inplace=True)
        
        df.to_csv(FILETOMAP,index=False)
        
        df2 = pd.read_csv(FILETOMAP,dtype=str)
        
        df3 = df2[['record_id','obho_submissions']]
        
        df3.to_csv(FILETOMAP,index=False)
        
        df = pd.read_csv('observedho.csv')
        df2 = df.groupby('record_id')['obho_submissions'].agg(['count'])
        df2.to_csv('observedhocount.csv')
        
        df = pd.read_csv('observedhocount.csv')
        df.rename(columns={df.columns[1]: "obho_submissions" }, inplace = True)
        
        df.to_csv('x07 - observedho.csv',index=False)
        
        df = pd.read_csv('ho_lor.csv')
        
        df2 = df.groupby('Student Email')['2 Multiple Choice Value'].max()
        
        df2.to_csv('ho_lor.csv')
        
        df2 = pd.read_csv('ho_lor.csv')
        
        df2.rename(columns={df2.columns[0]: "email" }, inplace = True)
        df2.rename(columns={df2.columns[1]: "ho_lor" }, inplace = True)
        
        df2.to_csv('ho_lor.csv',index=False)
        
        FILETOMAP = "ho_lor.csv"
        RECORDIDMAPPER = 'recordidmapper.csv'
        COLUMN = 'email'
        
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[2] for rows in reader} 
            
        df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        first_column = df.pop('record_id')
        
        df.insert(0, 'record_id', first_column)
        
        df.to_csv(FILETOMAP,index=False)
        
        df=pd.read_csv(FILETOMAP,dtype=str)
        
        df.dropna(subset=['record_id'], inplace=True)
        
        df.to_csv(FILETOMAP,index=False)
        
        df2 = pd.read_csv(FILETOMAP,dtype=str)
        
        df3 = df2[['record_id','ho_lor']]
        
        df3.to_csv(FILETOMAP,index=False)
        
        FILETOMAP = 'x07 - observedho.csv'
        RECORDIDMAPPER = 'ho_lor.csv'
        COLUMN = 'record_id'
        
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('ho_lor.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df['ho_lor'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)

        ##############################################OBSERVED HP##############################################
        import pandas as pd
        import numpy as np
        import csv
        df = df_5
        
        df = pd.read_csv('00 - originalobservedHP.csv')
        
        df = df.loc[df['Course'] == "Pediatric Clerkship"]
        
        #df = df.loc[df['Course'] == "Testing for Peds QR Eval"]
        
        df = df[['Student Email','1 Multiple Choice Value','2 Multiple Choice Value', '6 Multiple Choice Value']]
        
        hx = df[['Student Email','2 Multiple Choice Value']]
        pe = df[['Student Email','6 Multiple Choice Value']]
        
        hx.to_csv('hx_lor.csv')
        pe.to_csv('pe_lor.csv')
        
        df['obhp_submissions'] = 1
        
        df['email'] = df['Student Email'].astype(str)
        
        df.to_csv('observedhp.csv',index=False)
        
        FILETOMAP = "observedhp.csv"
        RECORDIDMAPPER = 'recordidmapper.csv'
        COLUMN = 'email'
        
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[2] for rows in reader} 
            
        df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        first_column = df.pop('record_id')
        
        df.insert(0, 'record_id', first_column)
        
        df.to_csv(FILETOMAP,index=False)
        
        df=pd.read_csv(FILETOMAP,dtype=str)
        
        df.dropna(subset=['record_id'], inplace=True)
        
        df.to_csv(FILETOMAP,index=False)
        
        df2 = pd.read_csv(FILETOMAP,dtype=str)
        
        df3 = df2[['record_id','obhp_submissions']]
        
        df3.to_csv(FILETOMAP,index=False)
        
        df = pd.read_csv('observedhp.csv')
        df2 = df.groupby('record_id')['obhp_submissions'].agg(['count'])
        df2.to_csv('observedhpcount.csv')
        
        df = pd.read_csv('observedhpcount.csv')
        df.rename(columns={df.columns[1]: "obhp_submissions" }, inplace = True)
        
        df.to_csv('x07 - observedhp.csv',index=False)
        
        
        #######################################################################################################################
        
        df = pd.read_csv('hx_lor.csv')
        
        df2 = df.groupby('Student Email')['2 Multiple Choice Value'].max()
        
        df2.to_csv('hx_lor.csv')
        
        df2 = pd.read_csv('hx_lor.csv')
        
        df2.rename(columns={df2.columns[0]: "email" }, inplace = True)
        df2.rename(columns={df2.columns[1]: "hx_lor" }, inplace = True)
        
        df2.to_csv('hx_lor.csv',index=False)
        
        FILETOMAP = "hx_lor.csv"
        RECORDIDMAPPER = 'recordidmapper.csv'
        COLUMN = 'email'
        
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[2] for rows in reader} 
            
        df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        first_column = df.pop('record_id')
        
        df.insert(0, 'record_id', first_column)
        
        df.to_csv(FILETOMAP,index=False)
        
        df=pd.read_csv(FILETOMAP,dtype=str)
        
        df.dropna(subset=['record_id'], inplace=True)
        
        df.to_csv(FILETOMAP,index=False)
        
        df2 = pd.read_csv(FILETOMAP,dtype=str)
        
        df3 = df2[['record_id','hx_lor']]
        
        df3.to_csv(FILETOMAP,index=False)
        
        
        FILETOMAP = 'x07 - observedhp.csv'
        RECORDIDMAPPER = 'hx_lor.csv'
        COLUMN = 'record_id'
        
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('hx_lor.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df['hx_lor'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        #######################################################################################################################
        
        df = pd.read_csv('pe_lor.csv')
        
        df2 = df.groupby('Student Email')['6 Multiple Choice Value'].max()
        
        df2.to_csv('pe_lor.csv')
        
        df2 = pd.read_csv('pe_lor.csv')
        
        df2.rename(columns={df2.columns[0]: "email" }, inplace = True)
        df2.rename(columns={df2.columns[1]: "pe_lor" }, inplace = True)
        
        df2.to_csv('pe_lor.csv',index=False)
        
        FILETOMAP = "pe_lor.csv"
        RECORDIDMAPPER = 'recordidmapper.csv'
        COLUMN = 'email'
        
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[2] for rows in reader} 
            
        df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        
        first_column = df.pop('record_id')
        
        df.insert(0, 'record_id', first_column)
        
        df.to_csv(FILETOMAP,index=False)
        
        df=pd.read_csv(FILETOMAP,dtype=str)
        
        df.dropna(subset=['record_id'], inplace=True)
        
        df.to_csv(FILETOMAP,index=False)
        
        df2 = pd.read_csv(FILETOMAP,dtype=str)
        
        df3 = df2[['record_id','pe_lor']]
        
        df3.to_csv(FILETOMAP,index=False)
        
        
        FILETOMAP = 'x07 - observedhp.csv'
        RECORDIDMAPPER = 'pe_lor.csv'
        COLUMN = 'record_id'
        
        df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
        
        mydict = {}
        with open('pe_lor.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
        	reader = csv.reader(inp)
        	df1 = {rows[0]:rows[1] for rows in reader} 
            
        df['pe_lor'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
        
        df.to_csv(FILETOMAP,index=False)
        ##############################################OBSERVED HP##############################################
        
if __name__ == "__main__":
    main()

