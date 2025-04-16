import streamlit as st
import pandas as pd
import numpy as np
import io
import openpyxl
import re
import os

# Function to handle Canvas Quiz filename extraction based on week number
def get_canvas_quiz_filename(filename):
    match = re.search(r"Week (\d+)\s*-", filename)  # Search for "Week X -"
    if match:
        week_number = int(match.group(1))  # Extract the week number (1, 2, 3, ...)
        # Map the week number to the Canvas Quiz file name
        if week_number == 1:
            return "00 - canvasquiz1.csv"
        elif week_number == 2:
            return "00 - canvasquiz2.csv"
        elif week_number == 3:
            return "00 - canvasquiz3.csv"
        elif week_number == 4:
            return "00 - canvasquiz4.csv"
    return None

# Function to save uploaded files as CSVs
def save_file_as_csv(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()
    try:
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file, engine='openpyxl', sheet_name='GradeBook')
        else:
            raise ValueError("File must be CSV or Excel format.")
        
        csv_file = io.StringIO()
        df.to_csv(csv_file, index=False)
        return csv_file.getvalue(), df
    except Exception as e:
        st.error(f"Error processing the file: {e}")
        return None, None

def main():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import io
    import openpyxl 
    
    st.title("Grader Database Uploader")

    st.markdown("""
- [Clinical Assessment Form](https://oasis.hersheymed.net/admin/course/e_manage/student_performance/setup_analysis_report.html)
- [Clinical Encounters](https://oasis.hersheymed.net/admin/course/experience_requirement/view_distribution_setup.html)
- [Procedure Encounters](https://oasis.hersheymed.net/admin/course/experience_requirement/view_distribution_setup.html)
- [Observed Handoff](https://oasis.hersheymed.net/admin/course/e_manage/student_performance/setup_analysis_report.html)
- [Observed History & Physical](https://oasis.hersheymed.net/admin/course/e_manage/student_performance/setup_analysis_report.html)
- [Developmental Assessment Report - Download Labels](https://redcap.ctsi.psu.edu/redcap_v14.5.43/DataExport/index.php?pid=17354&report_id=ALL)
- [Social Drivers of Health Report - Download Labels](https://redcap.ctsi.psu.edu/redcap_v14.5.43/DataExport/index.php?pid=17086&report_id=ALL)
- [NBME Exam](https://oasis.hersheymed.net/admin/course/gradebook/)
- [CANVAS Quiz 1](https://psu.instructure.com/courses/2391216/quizzes/5215346/statistics)
- [CANVAS Quiz 2](https://psu.instructure.com/courses/2391216/quizzes/5215347/statistics)
- [CANVAS Quiz 3](https://psu.instructure.com/courses/2391216/quizzes/5215343/statistics)
- [CANVAS Quiz 4](https://psu.instructure.com/courses/2391216/quizzes/5215345/statistics)
- [Preceptor Tracker](https://oasis.hersheymed.net/admin/course/e_manage/manage_evaluators.html)
""")

    uploaded_files = st.file_uploader("Upload Files (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

    file_data = {}

    # Mapping of categories to desired file names
    file_name_mapping = {
        "Clinical Assessment Form": '00 - originaloasis.csv',
        "Clinical Encounter": '00 - export_results.csv',
        "Observed Handoff": '00 - originalhandoff.csv',
        "Observed HP": '00 - originalobservedHP.csv',
        "Developmental Assessment": '00 - originaldevass.csv',
        "NBME Exam": '00 - NBME_results.csv',
        "Canvas Quiz 1": '00 - canvasquiz1.csv',
        "Canvas Quiz 2": '00 - canvasquiz2.csv',
        "Canvas Quiz 3": '00 - canvasquiz3.csv',
        "Canvas Quiz 4": '00 - canvasquiz4.csv',
        "Preceptor Tracker": '00 - ptrackero.csv', 
        "Social Drivers of Health": "00 - originalsdoh.csv"
    }

    column_value_mapping = {
        "Clinical Assessment Form": {"column": "Evaluation", "value": "*Clinical Assessment of Student"},
        "Clinical Encounter": {"column": "Checklist", "value": "Pediatrics Case Logs"},
        "Procedure Encounter": {"column": "Checklist", "value": "Pediatrics Procedure Logs"},
        "Observed Handoff": {"column": "Evaluation", "value": "*PEDS Handoff"},
        "Observed HP": {"column": "Evaluation", "value": "*PEDS History Taking & Physical Exam"},
        "Developmental Assessment": {"column": "SOCIAL/EMOTIONAL MILESTONES (choice=Calms down when spoken to or picked up)", "value": "Unchecked"},
        "NBME Exam": {"column": "Student Level", "value": "MS 3"},
        "Preceptor Tracker": {"column": "Manual Evaluations", "value": "Mid-Cycle Feedback"},
        "Social Drivers of Health": {"column": "Domain (choice=Housing instability (e.g. homelessness, unsafe living conditions))", "value": "Unchecked"}
    }

    if uploaded_files:
        # Process the uploaded files
        for uploaded_file in uploaded_files:
            csv_content, df = save_file_as_csv(uploaded_file)
            if csv_content and df is not None:
                # Assign to specific categories based on column value mapping
                for category, mapping in column_value_mapping.items():
                    if mapping["column"] in df.columns:
                        if mapping["value"] in df[mapping["column"]].values:
                            file_data[category] = df
                            st.write(f"File '{uploaded_file.name}' assigned to category: {category}")
                            break

                # Check if the file corresponds to a Canvas Quiz and extract the correct quiz category
                quiz_value = get_canvas_quiz_filename(uploaded_file.name)
                if quiz_value:
                    # Ensure that Canvas Quiz 1, 2, 3, or 4 are uniquely handled and not overwritten
                    if quiz_value not in file_data:
                        file_data[quiz_value] = df
                        st.write(f"File '{uploaded_file.name}' assigned to category: {quiz_value}")
                    else:
                        st.warning(f"File '{uploaded_file.name}' for {quiz_value} already processed.")

        # After processing, check if all required categories are assigned DataFrames
        if all(value is not None for value in file_data.values()):
            if st.button("Next"):
                data = st.secrets["dataset"]["data"]
                dfx = pd.DataFrame(data)
                dfx.to_csv('recordidmapper.csv', index=False)
    
                #df_2 = pd.read_csv('00 - originaloasis.csv')
                #df_3 = pd.read_csv('00 - export_results.csv')
                #df_4 = pd.read_csv('00 - originalhandoff.csv')
                #df_5 = pd.read_csv('00 - originalobservedHP.csv')
                #df_6 = pd.read_csv('00 - originaldevass.csv')
                #df_7 = pd.read_csv('00 - NBME_results.csv')
                #df_8 = pd.read_csv('00 - canvasquiz1.csv')
                #df_9 = pd.read_csv('00 - canvasquiz2.csv')
                #df_10 = pd.read_csv('00 - canvasquiz3.csv')
                #df_11 = pd.read_csv('00 - canvasquiz4.csv')
                #df_12 = pd.read_csv('00 - ptrackero.csv')

                df_2 = file_data.get("Clinical Assessment Form", None)
                df_3 = file_data.get("Clinical Encounter", None)
                df_3a = file_data.get("Procedure Encounter", None)
                df_3 = pd.concat([df_3,df_3a])
                df_4 = file_data.get("Observed Handoff", None)
                df_5 = file_data.get("Observed HP", None)
                df_6 = file_data.get("Developmental Assessment", None)
                df_7 = file_data.get("NBME Exam", None)
                df_8 = file_data.get("00 - canvasquiz1.csv", None)
                df_9 = file_data.get("00 - canvasquiz2.csv", None)
                df_10 = file_data.get("00 - canvasquiz3.csv", None)
                df_11 = file_data.get("00 - canvasquiz4.csv", None)
                df_12 = file_data.get("Preceptor Tracker", None)
                df_13 = file_data.get("Social Drivers of Health", None)

                df_2.to_csv('00 - originaloasis.csv', index=False)
                df_3.to_csv('00 - export_results.csv', index=False)
                df_4.to_csv('00 - originalhandoff.csv', index=False)
                df_5.to_csv('00 - originalobservedHP.csv', index=False)
                df_6.to_csv('00 - originaldevass.csv', index=False)
                df_7.to_csv('00 - NBME_results.csv', index=False)
                df_8.to_csv('00 - canvasquiz1.csv', index=False)
                df_9.to_csv('00 - canvasquiz2.csv', index=False)
                df_10.to_csv('00 - canvasquiz3.csv', index=False)
                df_11.to_csv('00 - canvasquiz4.csv', index=False)
                df_12.to_csv('00 - ptrackero.csv', index=False)
                df_13.to_csv('00 - originalsdoh.csv', index=False)

                #Observing: Shadowing
                #Performing with indirect preceptor supervision: Data Collection and Medical Decision
                #Performing with indirect preceptor supervision: Data Collection and Medical Decision Making
                #Performing with direct preceptor supervision: Data Collection and Medical Decision Making
                #Assisting: Data Collection" 

                mapping = {"Observing: Shadowing": "Observed",
                           "Performing with indirect preceptor supervision: Data Collection and Medical Decision Making": "Performed",
                           "Performing with direct preceptor supervision: Data Collection and Medical Decision Making": "Performed",
                           "Assisting: Data Collection": "Assisted"
                          }

                def determine_peds_level(row):
                    # Check which column has a value (they are mutually exclusive)
                    if pd.notnull(row['*Assisted or Above']):
                        value = row['*Assisted or Above']
                    elif pd.notnull(row['*Observed or Above']):
                        value = row['*Observed or Above']
                    else:
                        return np.nan  # or another placeholder for missing data
                    
                    # Return the mapped value or the original if not found in the mapping dictionary
                    return mapping.get(value, value)

                df_3["*Peds Level of Responsibility"] = df_3.apply(determine_peds_level, axis=1)
                
                st.dataframe(df_3)
                
                df_3.to_csv('00 - export_results.csv',index=False)                 
                
                observed = df_3.loc[df_3['*Peds Level of Responsibility'] == 'Observed']
                observed = observed.loc[(observed['Item'] != '[Ped] Health Systems Issue')&(observed['Item'] != '[Ped] Humanities Issue')]
                observed.to_csv('00 - observed_report.csv',index=False)

                st.dataframe(observed)
                
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
                date = '2025-03-17 00:00:00' 
                df['Start Date'] = pd.to_datetime(df["Start Date"])
                df = df[df['Start Date'] >= date]
                df.to_csv('00 - export_results.csv',index=False)
                
                df = df[['Email', 'Start Date', 'Item', '*Peds Level of Responsibility', 'Time entered']]
                
                # List of all items that should appear as columns
                items = [
                    '[Ped] Health Supervision (Well Child Visit)',
                    '[Ped] Common Newborn Conditions e.g. Jaundice, Rash, Colic/Crying, Spit-up/Vomitting/Reflux, Poor Weight Gain',
                    '[Ped] Dermatologic System e.g. Rash, Pallor',
                    '[Ped] Gastrointestinal Tract',
                    '[Ped] Behavior e.g. Temper tantrums/aggressive behavior, ADHD, Developmental Delay, Autism Spectrum',
                    '[Ped] Upper and Lower Respiratory Tract e.g. Dental Caries, Sore Throat, Cough, Shortness of breath, Wheezing', 
                    '[Ped] Acute Conditions e.g. Abdominal Pain, Fever, Seizure, Shortness of breath, Wheezing',
                    '[Ped] Other e.g. Obesity/ Metabolic Syndrome',
                    '[PED Procedure] Test Interpretation', 
                    '[Ped] Health Systems Issue',
                    '[Ped] Humanities Issue'
                ]
                
                # The mapping for renaming columns
                rename_dict = {
                    '[Ped] Health Supervision (Well Child Visit)': 'clindom_well_child',
                    '[Ped] Common Newborn Conditions e.g. Jaundice, Rash, Colic/Crying, Spit-up/Vomitting/Reflux, Poor Weight Gain': 'clindom_commonnb',
                    '[Ped] Dermatologic System e.g. Rash, Pallor': 'clindom_derm',
                    '[Ped] Gastrointestinal Tract': 'clindom_gi',
                    '[Ped] Behavior e.g. Temper tantrums/aggressive behavior, ADHD, Developmental Delay, Autism Spectrum': 'clindom_behavior',
                    '[Ped] Upper and Lower Respiratory Tract e.g. Dental Caries, Sore Throat, Cough, Shortness of breath, Wheezing': 'clindom_upperandlowerrt',
                    '[Ped] Acute Conditions e.g. Abdominal Pain, Fever, Seizure, Shortness of breath, Wheezing': 'clindom_acuteconditions',
                    '[Ped] Other e.g. Obesity/ Metabolic Syndrome': 'clindom_other',
                    '[PED Procedure] Test Interpretation': 'clindom_testinterpret',
                    '[Ped] Health Systems Issue': 'clindom_healthsystems',
                    '[Ped] Humanities Issue': 'clindom_humanities'
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
                #df['Time entered'] = pd.to_datetime(df['Time entered'], format='%m/%d/%Y %I:%M:%S %p')
                
                #df['Time entered'] = pd.to_datetime(df['Time entered'], format="%m/%d/%Y %H:%M")
                try:
                    df['Time entered'] = pd.to_datetime(df['Time entered'], format='%m/%d/%Y %I:%M:%S %p')
                except Exception as e:
                    print(f"Error with format '%m/%d/%Y %I:%M:%S %p': {e}")
                    # If the first conversion fails, fall back to the 24-hour format without seconds
                    df['Time entered'] = pd.to_datetime(df['Time entered'], format="%m/%d/%Y %H:%M")
                
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

                df_comments = df[['Student Email','4 Multiple Choice Label', '5 Answer text']]

                df_comments["ho_comments"] = df_comments["4 Multiple Choice Label"] + ": " + df_comments["5 Answer text"]
                
                df_comments = df_comments[['Student Email', 'ho_comments']]

                df_comments.to_csv('ho_comments.csv',index=False)
                
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

                FILETOMAP = 'ho_comments.csv'
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = 'Student Email'
                
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[2] for rows in reader} 
                    
                df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                # Drop "Student Email" column after mapping
                df = df.drop(columns=[COLUMN])
                
                # Keep only "record_id" and "ho_comments"
                df = df[["record_id", "ho_comments"]]
                
                # Save the updated dataset
                df.to_csv(FILETOMAP, index=False)
        
                FILETOMAP = 'x07 - observedho.csv'
                RECORDIDMAPPER = 'ho_comments.csv'
                COLUMN = 'record_id'
                
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df['ho_comments'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                df.to_csv(FILETOMAP,index=False)
                ##############################################OBSERVED HP##############################################
                import pandas as pd
                import numpy as np
                import csv
                df = df_5
                
                df = pd.read_csv('00 - originalobservedHP.csv')
                
                df = df.loc[df['Course'] == "Pediatric Clerkship"]
                
                #df = df.loc[df['Course'] == "Testing for Peds QR Eval"]
                
                df = df[['Student Email','1 Multiple Choice Value','2 Multiple Choice Value', '6 Multiple Choice Value','4 Multiple Choice Label','5 Answer text','8 Multiple Choice Label','9 Answer text']]
                
                hx = df[['Student Email','2 Multiple Choice Value']]
                pe = df[['Student Email','6 Multiple Choice Value']]

                hx_c = df[['Student Email','4 Multiple Choice Label','5 Answer text']]
                pe_c = df[['Student Email','8 Multiple Choice Label','9 Answer text']]
                
                hx.to_csv('hx_lor.csv')
                pe.to_csv('pe_lor.csv')
                
                df['obhp_submissions'] = 1
                
                df['email'] = df['Student Email'].astype(str)
                
                df.to_csv('observedhp.csv',index=False)

                # Select relevant columns and rename them while merging
                hx_c = df[['Student Email', '4 Multiple Choice Label', '5 Answer text']].copy()
                hx_c['4 Multiple Choice Label'] = hx_c['4 Multiple Choice Label'].fillna('').astype(str)
                hx_c['5 Answer text'] = hx_c['5 Answer text'].fillna('').astype(str)
                hx_c["hx_comments"] = hx_c["4 Multiple Choice Label"] + "; " + hx_c["5 Answer text"]
                hx_c = hx_c[['Student Email', 'hx_comments']]
        
                pe_c = df[['Student Email', '8 Multiple Choice Label', '9 Answer text']].copy()
                pe_c[['8 Multiple Choice Label', '9 Answer text']] = pe_c[['8 Multiple Choice Label', '9 Answer text']].fillna('').astype(str)
                pe_c["pe_comments"] = pe_c["8 Multiple Choice Label"] + "; " + pe_c["9 Answer text"]
                pe_c = pe_c[['Student Email', 'pe_comments']]
                                
                # Merge both dataframes on "Student Email"
                merged_df = pd.merge(hx_c, pe_c, on="Student Email", how="outer")
                
                merged_df = merged_df.drop_duplicates()
                
                # Group by "Student Email" and combine hx_comments and pe_comments into lists
                grouped_df = merged_df.groupby("Student Email").agg({"hx_comments": lambda x: "; ".join(x.dropna().unique()),"pe_comments": lambda x: "; ".join(x.dropna().unique())}).reset_index()
                
                # Save the grouped dataset
                grouped_df.to_csv('hx_pe_comments.csv', index=False)
                
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

                FILETOMAP = "hx_pe_comments.csv"
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = "Student Email"

                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
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

                FILETOMAP = "x07 - observedhp.csv"
                RECORDIDMAPPER = 'hx_pe_comments.csv'
                COLUMN = 'record_id'
                
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[2] for rows in reader} 
                    
                df['hx_comments'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 

                mydict = {}
                with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[3] for rows in reader} 
                    
                df['pe_comments'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 

                df.to_csv(FILETOMAP,index=False)
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
                
                df.to_csv(FILETOMAP,index=False); st.dataframe(df)
                ###################################################DEVELOPMENTAL ASSESSMENTS#########################################################
                df = pd.read_csv('00 - originaldevass.csv')
        
                df.rename(columns={df.columns[3]: "email" }, inplace = True)
                df.rename(columns={df.columns[2]: "submitted_dev" }, inplace = True)
                
                df['devass'] = '1'
                
                df.to_csv('devass.csv',index=False)
                
                FILETOMAP = "devass.csv"
                RECORDIDMAPPER ='recordidmapper.csv'
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
                
                df3 = df2[['record_id','devass','submitted_dev']]
                
                df3 = df3.loc[df3['submitted_dev'] != '[not completed]']
                
                df3.to_csv(FILETOMAP,index=False)
                
                #df = pd.read_csv('devass.csv')
                
                df3['submitted_dev'] = df3['submitted_dev'].astype('datetime64[ns]')
                df3['submitted_dev'] = df3['submitted_dev'].dt.strftime('%m-%d-%Y')
                
                df3.to_csv('x08 - devass.csv',index=False)

                ###################################################SDOH#########################################################
                df = pd.read_csv('00 - originalsdoh.csv')
        
                df.rename(columns={df.columns[3]: "email" }, inplace = True)
                df.rename(columns={df.columns[2]: "submitted_sdoh" }, inplace = True)
                
                df['sdohass'] = '1'
                
                df.to_csv('sdohass.csv',index=False)
                
                FILETOMAP = "sdohass.csv"
                RECORDIDMAPPER ='recordidmapper.csv'
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
                
                df3 = df2[['record_id','sdohass','submitted_sdoh']]
                
                df3 = df3.loc[df3['submitted_sdoh'] != '[not completed]']
                
                df3.to_csv(FILETOMAP,index=False)
                
                #df = pd.read_csv('devass.csv')
                
                df3['submitted_sdoh'] = df3['submitted_sdoh'].astype('datetime64[ns]')
                df3['submitted_sdoh'] = df3['submitted_sdoh'].dt.strftime('%m-%d-%Y')
                
                df3.to_csv('x13 - sdoh.csv',index=False)
                
                #####################################################NBME###################################################################
                import pandas as pd
                df = pd.read_csv('00 - NBME_results.csv')
                
                A = 'Email'
                a = 'email'
                
                B = 'NBME Exam - Percentage Score'
                b = 'nbme'
                
                C = 'Final Course Grade'
                c = 'finalgrade'
                
                df2 = df.rename(columns={A: a,
                                         B: b,
                                         C:c})
                
                df3 = df2[['email','nbme','finalgrade']]
                df3.to_csv('nbme.csv',index=False)
                
                FILETOMAP = "nbme.csv"
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = 'email'
                
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
                
                df.to_csv(FILETOMAP,index=False)
                
                df=pd.read_csv(FILETOMAP,dtype=str)
                
                df.dropna(subset=['record_id'], inplace=True)
                
                df.to_csv(FILETOMAP,index=False)
                
                df2 = pd.read_csv(FILETOMAP,dtype=str)
                
                df3 = df2[['record_id','nbme']]
                
                df3.to_csv(FILETOMAP,index=False)
                
                df = pd.read_csv(FILETOMAP)
                df.to_csv('x09 - nbme.csv',index=False)
        
                import pandas as pd
                import numpy as np 
                df = pd.read_csv('00 - canvasquiz1.csv')
                
                df.rename(columns={df.columns[2]: "email_2" }, inplace = True)
                
                df = df[['email_2',"score"]]
                
                df['quiz1'] = round((df['score'].astype(int)/20)*100,1)
                
                df=df.groupby('email_2').agg({'quiz1':max})
                
                df.to_csv('x10 - canvasquiz1.csv')
                
                FILETOMAP = "x10 - canvasquiz1.csv"
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = 'email_2'
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[1]:rows[2] for rows in reader} 
                    
                df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                df.to_csv(FILETOMAP,index=False)
                
                first_column = df.pop('record_id')
                
                df.insert(0, 'record_id', first_column)
                
                df.to_csv(FILETOMAP,index=False)
                
                df=pd.read_csv(FILETOMAP,dtype=str)
                
                df.dropna(subset=['record_id'], inplace=True)
                
                df.to_csv(FILETOMAP,index=False)
                
                df2 = pd.read_csv(FILETOMAP,dtype=str)
                
                df3 = df2[['record_id','quiz1']]
                
                df3.to_csv(FILETOMAP,index=False)
                
                #################################################
                df = pd.read_csv('00 - canvasquiz1.csv')
                
                df = df[['sis_id','submitted']]
                
                df.to_csv('1x.csv',index=False)
                
                FILETOMAP = "1x.csv"
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = 'sis_id'
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[1]:rows[2] for rows in reader} 
                    
                df['record_id'] = df[(COLUMN)].map(df1)     
                
                df = df[['record_id','submitted']]
                df.to_csv('1x.csv',index=False)
                
                FILETOMAP = "x10 - canvasquiz1.csv"
                RECORDIDMAPPER = '1x.csv'
                COLUMN = 'record_id'
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df['quiz_1_late'] = df[(COLUMN)].map(df1)     
                
                #df['quiz_1_late'] = df['quiz_1_late'].astype('datetime64[ns]')
                
                import pytz
                df['quiz_1_late'] = pd.to_datetime(df['quiz_1_late'])
                
                # Check if the datetime column is timezone-naive or timezone-aware
                if df['quiz_1_late'].dt.tz is None:
                    # Localize the datetime if it's naive, then convert to the desired timezone
                    df['quiz_1_late'] = df['quiz_1_late'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
                else:
                    # Just convert if it's already timezone-aware
                    df['quiz_1_late'] = df['quiz_1_late'].dt.tz_convert('US/Eastern')
                    
                #df['quiz_1_late'] = pd.to_datetime(df['quiz_1_late']).dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
                
                df['quiz_1_late'] = df['quiz_1_late'].dt.strftime('%m-%d-%Y 23:59')
                
                df.to_csv(FILETOMAP,index=False)
                
                import pandas as pd
                import numpy as np
                import csv
                
                df = pd.read_csv('00 - canvasquiz2.csv')
                df.rename(columns={df.columns[2]: "email_2" }, inplace = True)
                
                df = df[['email_2',"score"]]
                
                df['quiz2'] = round((df['score'].astype(int)/20)*100,1)
                
                df=df.groupby('email_2').agg({'quiz2':max})
                
                df.to_csv('x10 - canvasquiz2.csv')
                
                FILETOMAP = "x10 - canvasquiz2.csv"
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = 'email_2'
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[1]:rows[2] for rows in reader} 
                    
                df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                df.to_csv(FILETOMAP,index=False)
                
                first_column = df.pop('record_id')
                
                df.insert(0, 'record_id', first_column)
                
                df.to_csv(FILETOMAP,index=False)
                
                df=pd.read_csv(FILETOMAP,dtype=str)
                
                df.dropna(subset=['record_id'], inplace=True)
                
                df.to_csv(FILETOMAP,index=False)
                
                df2 = pd.read_csv(FILETOMAP,dtype=str)
                
                df3 = df2[['record_id','quiz2']]
                
                df3.to_csv(FILETOMAP,index=False)
                
                #################################################
                df = pd.read_csv('00 - canvasquiz2.csv')
                
                df = df[['sis_id','submitted']]
                
                df.to_csv('1x.csv',index=False)
                
                FILETOMAP = "1x.csv"
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = 'sis_id'
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[1]:rows[2] for rows in reader} 
                    
                df['record_id'] = df[(COLUMN)].map(df1)     
                
                df = df[['record_id','submitted']]
                df.to_csv('1x.csv',index=False)
                
                FILETOMAP = "x10 - canvasquiz2.csv"
                RECORDIDMAPPER = '1x.csv'
                COLUMN = 'record_id'
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df['quiz_2_late'] = df[(COLUMN)].map(df1)     
                
                #df['quiz_2_late'] = df['quiz_2_late'].astype('datetime64[ns]')
                df['quiz_2_late'] = pd.to_datetime(df['quiz_2_late'])
        
                import pytz
                
                #df['quiz_2_late'] = pd.to_datetime(df['quiz_2_late']).dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
        
                if df['quiz_2_late'].dt.tz is None:
                    # Localize the datetime if it's naive, then convert to the desired timezone
                    df['quiz_2_late'] = df['quiz_2_late'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
                else:
                    # Just convert if it's already timezone-aware
                    df['quiz_2_late'] = df['quiz_2_late'].dt.tz_convert('US/Eastern')
        
                df['quiz_2_late'] = df['quiz_2_late'].dt.strftime('%m-%d-%Y 23:59')
                
                df.to_csv(FILETOMAP,index=False)
                
                import pandas as pd
                import numpy as np
                import csv
                
                df = pd.read_csv('00 - canvasquiz3.csv') ###############
                df.rename(columns={df.columns[2]: "email_2" }, inplace = True)
                
                df = df[['email_2',"score"]]
                
                df['quiz3'] = round((df['score'].astype(int)/20)*100,1) ###############
                
                df=df.groupby('email_2').agg({'quiz3':max}) ###############
                
                df.to_csv('x10 - canvasquiz3.csv') ###############
                
                FILETOMAP = "x10 - canvasquiz3.csv" ###############
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = 'email_2'
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[1]:rows[2] for rows in reader} 
                    
                df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                df.to_csv(FILETOMAP,index=False)
                
                first_column = df.pop('record_id')
                
                df.insert(0, 'record_id', first_column)
                
                df.to_csv(FILETOMAP,index=False)
                
                df=pd.read_csv(FILETOMAP,dtype=str)
                
                df.dropna(subset=['record_id'], inplace=True)
                
                df.to_csv(FILETOMAP,index=False)
                
                df2 = pd.read_csv(FILETOMAP,dtype=str)
                
                df3 = df2[['record_id','quiz3']]         ###############
                
                df3.to_csv(FILETOMAP,index=False)
                
                #################################################
                df = pd.read_csv('00 - canvasquiz3.csv')
                
                df = df[['sis_id','submitted']]
                
                df.to_csv('1x.csv',index=False)
                
                FILETOMAP = "1x.csv"
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = 'sis_id'
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[1]:rows[2] for rows in reader} 
                    
                df['record_id'] = df[(COLUMN)].map(df1)     
                
                df = df[['record_id','submitted']]
                df.to_csv('1x.csv',index=False)
                
                FILETOMAP = "x10 - canvasquiz3.csv"
                RECORDIDMAPPER = '1x.csv'
                COLUMN = 'record_id'
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df['quiz_3_late'] = df[(COLUMN)].map(df1)     
                
                #df['quiz_3_late'] = df['quiz_3_late'].astype('datetime64[ns]')
        
                df['quiz_3_late'] = pd.to_datetime(df['quiz_3_late'])
        
                import pytz
                if df['quiz_3_late'].dt.tz is None:
                    # Localize the datetime if it's naive, then convert to the desired timezone
                    df['quiz_3_late'] = df['quiz_3_late'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
                else:
                    # Just convert if it's already timezone-aware
                    df['quiz_3_late'] = df['quiz_3_late'].dt.tz_convert('US/Eastern')
        
                #df['quiz_3_late'] = pd.to_datetime(df['quiz_3_late']).dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
                
                df['quiz_3_late'] = df['quiz_3_late'].dt.strftime('%m-%d-%Y 23:59')
                
                df.to_csv(FILETOMAP,index=False)
                
                import pandas as pd
                import numpy as np
                import csv
                
                df = pd.read_csv('00 - canvasquiz4.csv') ###############
                df.rename(columns={df.columns[2]: "email_2" }, inplace = True)
                
                df = df[['email_2',"score"]]
                
                df['quiz4'] = round((df['score'].astype(int)/20)*100,1) ###############
                
                df=df.groupby('email_2').agg({'quiz4':max}) ###############
                
                df.to_csv('x10 - canvasquiz4.csv') ###############
                
                FILETOMAP = "x10 - canvasquiz4.csv" ###############
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = 'email_2'
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[1]:rows[2] for rows in reader} 
                    
                df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                df.to_csv(FILETOMAP,index=False)
                
                first_column = df.pop('record_id')
                
                df.insert(0, 'record_id', first_column)
                
                df.to_csv(FILETOMAP,index=False)
                
                df=pd.read_csv(FILETOMAP,dtype=str)
                
                df.dropna(subset=['record_id'], inplace=True)
                
                df.to_csv(FILETOMAP,index=False)
                
                df2 = pd.read_csv(FILETOMAP,dtype=str)
                
                df3 = df2[['record_id','quiz4']]         ###############
                
                df3.to_csv(FILETOMAP,index=False)
                
                #################################################
                df = pd.read_csv('00 - canvasquiz4.csv')
                
                df = df[['sis_id','submitted']]
                
                df.to_csv('1x.csv',index=False)
                
                FILETOMAP = "1x.csv"
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = 'sis_id'
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('recordidmapper.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[1]:rows[2] for rows in reader} 
                    
                df['record_id'] = df[(COLUMN)].map(df1)     
                
                df = df[['record_id','submitted']]
                df.to_csv('1x.csv',index=False)
                
                FILETOMAP = "x10 - canvasquiz4.csv"
                RECORDIDMAPPER = '1x.csv'
                COLUMN = 'record_id'
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df['quiz_4_late'] = df[(COLUMN)].map(df1)     
                
                #df['quiz_4_late'] = df['quiz_4_late'].astype('datetime64[ns]')
        
                
                df['quiz_4_late'] = pd.to_datetime(df['quiz_4_late'])
        
                import pytz
                if df['quiz_4_late'].dt.tz is None:
                    # Localize the datetime if it's naive, then convert to the desired timezone
                    df['quiz_4_late'] = df['quiz_4_late'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
                else:
                    # Just convert if it's already timezone-aware
                    df['quiz_4_late'] = df['quiz_4_late'].dt.tz_convert('US/Eastern')
                
                #df['quiz_4_late'] = pd.to_datetime(df['quiz_4_late']).dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
                
                df['quiz_4_late'] = df['quiz_4_late'].dt.strftime('%m-%d-%Y 23:59')
                
                df.to_csv(FILETOMAP,index=False)
                ################################
                df = pd.read_csv('00 - ptrackero.csv')
                df['email'] = df['Student Email'].astype(str)
                
                df.to_csv('ptracker.csv',index=False)
                
                FILETOMAP = "ptracker.csv"
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
                #df = df.loc[(df['Manual Evaluations'] != "Mid-Cycle Feedback")&(df['Manual Evaluations'] != "*Mid-Cycle Feedback")]
                
                df.to_csv(FILETOMAP,index=False)
                
                df = df[['record_id','Faculty Name','Manual Evaluations']]
                
                x1 = pd.DataFrame(df['Manual Evaluations'].apply(lambda x: str(x).split('|')).apply(lambda x: [0]*(9-len(x)) + x).to_list(), columns=list("ABCDEFGHI"))
                
                df.to_csv('1x.csv',index=False)
                x1.to_csv('2x.csv',index=False)
                
                y1 = pd.read_csv('1x.csv')
                y2 = pd.read_csv('2x.csv')
                
                df = pd.concat([y1,y2],axis=1)
                
                df.to_csv('ptracker.csv',index=False)
                
                df = pd.read_csv('ptracker.csv')
                
                A = df[['record_id','Faculty Name', 'A']]
                A.columns.values[2] = "x"
                
                B = df[['record_id','Faculty Name', 'B']]
                B.columns.values[2] = "x"
                
                C = df[['record_id','Faculty Name', 'C']]
                C.columns.values[2] = "x"
                
                D = df[['record_id','Faculty Name', 'D']]
                D.columns.values[2] = "x"
                
                E = df[['record_id','Faculty Name', 'E']]
                E.columns.values[2] = "x"
                
                F = df[['record_id','Faculty Name', 'F']]
                F.columns.values[2] = "x"
                
                G = df[['record_id','Faculty Name', 'G']]
                G.columns.values[2] = "x"
                
                H = df[['record_id','Faculty Name', 'H']]
                H.columns.values[2] = "x"
                
                I = df[['record_id','Faculty Name', 'I']]
                I.columns.values[2] = "x"
                
                df = pd.concat([A,B,C,D,E,F,G,H,I])
                
                df = df[['record_id','Faculty Name', 'x']]
                
                df.to_csv('ptracker.csv',index=False)
                
                COLUMN = 'x'
                x = df[(COLUMN)].unique().tolist()
                
                oasis_cas = df.loc[(df['x'] == '*Clinical Assessment of Student')]
                obhp = df.loc[(df['x'] == '*PEDS History Taking & Physical Exam')]
                obho = df.loc[(df['x'] == '*PEDS Handoff')]
                
                oasis_cas.to_csv('oasis_cas.csv',index=False)
                obhp.to_csv('obhp.csv',index=False)
                obho.to_csv('obho.csv',index=False)
                
                oasis_cas = pd.read_csv('oasis_cas.csv')
                oasis_cas['distinct_count'] = oasis_cas.groupby(['record_id'])['record_id'].transform('count')
                oasis_cas_s = oasis_cas[['record_id','distinct_count']]
                oasis_cas_s.to_csv('oasis_cas_s.csv',index=False)
                
                oasis_cas['oasis_cas'] = oasis_cas['Faculty Name'].astype(str) + ","
                oasis_cas = oasis_cas.groupby('record_id',group_keys=False)['oasis_cas'].apply(' '.join).reset_index()
                oasis_cas['oasis_cas'] = oasis_cas['oasis_cas'].str.rstrip(',')
                oasis_cas.to_csv('oasis_cas.csv',index=False)
                
                obhp = pd.read_csv('obhp.csv')
                obhp['distinct_count'] = obhp.groupby(['record_id'])['record_id'].transform('count')
                obhp_s = obhp[['record_id','distinct_count']]
                obhp_s.to_csv('obhp_s.csv',index=False)
                
                obhp['cas'] = obhp['Faculty Name'].astype(str) + ","
                obhp = obhp.groupby('record_id',group_keys=False)['cas'].apply(' '.join).reset_index()
                obhp['cas'] = obhp['cas'].str.rstrip(',')
                obhp.to_csv('obhp.csv',index=False)
                
                obho = pd.read_csv('obho.csv')
                obho['distinct_count'] = obho.groupby(['record_id'])['record_id'].transform('count')
                obho_s = obho[['record_id','distinct_count']]
                obho_s.to_csv('obho_s.csv',index=False)
                
                obho['cas'] = obho['Faculty Name'].astype(str) + ","
                obho = obho.groupby('record_id',group_keys=False)['cas'].apply(' '.join).reset_index()
                obho['cas'] = obho['cas'].str.rstrip(',')
                obho.to_csv('obho.csv',index=False)
                
                df=pd.read_csv('oasis_cas.csv',dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('obhp.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df['obhp'] = df[('record_id')].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                mydict = {}
                with open('obho.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df['obho'] = df[('record_id')].map(df1)     
                
                df.to_csv('final.csv',index=False)
                
                ##################################################################
                
                df=pd.read_csv('final.csv',dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('oasis_cas_s.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df['oasissolicit'] = df[('record_id')].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                df.to_csv('final.csv',index=False)
                
                
                ##################################################################
                
                df=pd.read_csv('final.csv',dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('obho_s.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df['obho_s'] = df[('record_id')].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                df.to_csv('final.csv',index=False)
                
                
                ##################################################################
                
                df=pd.read_csv('final.csv',dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('obhp_s.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df['obhp_s'] = df[('record_id')].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                df.to_csv('final.csv',index=False)
                
                ##################################################################
                
                df = pd.read_csv('final.csv')
                df.to_csv('x11 - ptrackero.csv',index=False)
                
                ##################################################################ANALYSIS##################################################################
                import pandas as pd
                import datetime as dt
                
                df = pd.read_csv('00 - originaloasis.csv')
                y = list(df)
                #display(y)
                x = df[['Student Email','Submit Date','Start Date', 'End Date']]
                x.to_csv('oasisx.csv',index=False)
                
                x = pd.read_csv('oasisx.csv')
                
                x['Start Date'] = pd.to_datetime(x['Start Date'])
                x['Submit Date'] = pd.to_datetime(x['Submit Date'])
                
                x['Submit Date'] = x['Submit Date'].dt.date
                
                x['mid_rotation'] = x['Start Date'] + pd.DateOffset(days=14)
                x['end_rotation_twoweeks'] = x['Start Date'] + pd.DateOffset(days=39)
                
                x.to_csv('oasisx.csv',index=False)
                
                import numpy as np
                import pandas as pd 
                df = pd.read_csv('oasisx.csv')
                
                df['before_midrotation']= np.select([df['Submit Date'].between(df['Start Date'], df['mid_rotation'])], ['Yes'], 'No')
                df['before_course_end']= np.select([df['Submit Date'].between(df['Start Date'], df['End Date'])], ['Yes'], 'No')
                df['after_course_end']= np.select([df['Submit Date'].between(df['Start Date'], df['end_rotation_twoweeks'])], ['Yes'], 'No')
                
                df['patient_id'] = df['Student Email'].astype(str)
                df.to_csv('analysis.csv',index=False)
                
                df1=pd.read_csv('analysis'+".csv")
                df2=df1.groupby('Student Email').agg({'Submit Date':min})
                df2.to_csv('submitdate.csv')
                
                import pandas as pd
                import os
                import csv
                
                path = "recordidmapper.csv"
                
                FILETOMAP = 'submitdate.csv'
                RECORDIDMAPPER = path
                COLUMN = 'Student Email'
                
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[2] for rows in reader} 
                    
                df['record_id'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                df = df[['record_id','Submit Date']]
                
                df.columns.values[1] = "cas_submit_min"
                
                df['cas_submit_min'] = df['cas_submit_min'].astype('datetime64[ns]')
                df['cas_submit_min'] = df['cas_submit_min'].dt.strftime('%m-%d-%Y')
                
                df.to_csv(FILETOMAP,index=False)
                
                df = pd.read_csv('00 - originaloasis.csv')
                
                df = df.loc[df['Course'] == "Pediatric Clerkship"]
                
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
                
                FILETOMAP = "OTFconvert.csv"
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = 'email'
                
                import pandas as pd
                import numpy as np
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
                
                df = df.loc[df['Course'] == "Pediatric Clerkship"]
                
                df = df.loc[:, df.columns != 'Course ID']
                
                df = df[['Student Email', '7 Multiple Choice Label']]
                
                df['email'] = df['Student Email'].astype(str)
                df['prof'] = df['7 Multiple Choice Label'].astype(str)
                
                df = df[['email','prof']]
                
                df.to_csv('prof.csv',index=False)
                
                FILETOMAP = "prof.csv"
                RECORDIDMAPPER = 'recordidmapper.csv'
                COLUMN = 'email'
                
                import pandas as pd
                import numpy as np
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
                
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv('OTF_averages.csv',dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('meets.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df[('meets')] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                df.to_csv('OTF_averages.csv',index=False)
                
                import pandas as pd
                import numpy as np
                import csv
                df=pd.read_csv('OTF_averages.csv',dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open('does_not_meet.csv', mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df[('does_not_meet')] = df['record_id'].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                df.to_csv('OTF_averages.csv',index=False)
                
                df = pd.read_csv('00 - originaloasis.csv')
                
                df = df.loc[df['Course'] == "Pediatric Clerkship"]
                
                df = df[['Student Email','8 Answer text','9 Answer text']]
                
                df.to_csv('comments.csv',index=False)
                
                import pandas as pd
                import numpy as np
                import csv
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
                
                import pandas as pd
                import numpy as np
                import csv
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
                df.to_csv('oasissubmission.csv',index=False)
                
                df = pd.read_csv('oasissubmission.csv')
                df = df [['record_id','sum','does_not_meet']]
                
                df.columns.values[1] = "prev_sum_score"
                df.columns.values[2] = "any_prof_score"
                
                df.to_csv('courseanalysis_score.csv',index=False)
                
                import pandas as pd
                import os
                import csv
                
                FILETOMAP = 'submitdate.csv'
                RECORDIDMAPPER = 'courseanalysis_score.csv'
                COLUMN = 'record_id'
                
                df=pd.read_csv(FILETOMAP,dtype=str) #file you want to map to, in this case, I want to map IMP to the encounterids
                
                mydict = {}
                with open(RECORDIDMAPPER, mode='r')as inp:     #file is the objects you want to map. I want to map the IMP in this file to diagnosis.csv
                	reader = csv.reader(inp)
                	df1 = {rows[0]:rows[1] for rows in reader} 
                    
                df['prev_sum_score'] = df[(COLUMN)].map(df1)               #'type' is the new column in the diagnosis file. 'encounter_id' is the key you are using to MAP 
                
                df.to_csv('x12 - analysis.csv',index=False)
                
                ##############################################ENDING##############################################
                import pandas as pd
                df = pd.read_csv('recordidmapper.csv')
                df = df.loc[:, df.columns != 'email']
                df = df.loc[:, df.columns !='email_2']
                df = df.loc[:, df.columns !='student']
                df = df.loc[:, df.columns !='rotation']
                df.to_csv('mainfile.csv',index=False)
                
                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x01 - clinical_domains.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Get column names to map (excluding 'record_id' and 'email' columns)
                col_names = df_map.columns[2:]  # Adjust this to skip 'record_id' and 'email'
                
                # Step 3: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                
                for _, row in df_map.iterrows():
                    record_id = row['record_id']  # Assumes 'record_id' is the first column
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        # For each record_id, map the values from the domain columns (clindom_*)
                        mapping_dict[record_id] = row[2:].to_dict()  # Skipping 'record_id' and 'email' columns
                
                # Step 4: Apply the mapping to df_original for each domain column
                for col in col_names:
                    # Map values from df_original['record_id'] to the corresponding values in mapping_dict
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 5: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)
        
                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x03 - oasissubmission.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Ensure 'record_id' is a string and strip extra spaces
                df_map['record_id'] = df_map['record_id'].astype(str).str.strip()
                df_original['record_id'] = df_original['record_id'].astype(str).str.strip()
                
                # Step 3: Get column names to map (excluding 'record_id')
                col_names = df_map.columns[1:]  # Adjust this to skip 'record_id'
                
                # Step 4: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                for _, row in df_map.iterrows():
                    record_id = row['record_id']
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        mapping_dict[record_id] = row[1:].to_dict()  # Skipping 'record_id'
                
                # Step 5: Apply the mapping to df_original for each domain column
                for col in col_names:
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 6: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)
        
                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x07 - observedho.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Ensure 'record_id' is a string and strip extra spaces
                df_map['record_id'] = df_map['record_id'].astype(str).str.strip()
                df_original['record_id'] = df_original['record_id'].astype(str).str.strip()
                
                # Step 3: Get column names to map (excluding 'record_id')
                col_names = df_map.columns[1:]  # Adjust this to skip 'record_id'
                
                # Step 4: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                for _, row in df_map.iterrows():
                    record_id = row['record_id']
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        mapping_dict[record_id] = row[1:].to_dict()  # Skipping 'record_id'
                
                # Step 5: Apply the mapping to df_original for each domain column
                for col in col_names:
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 6: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)
        
                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x07 - observedhp.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Ensure 'record_id' is a string and strip extra spaces
                df_map['record_id'] = df_map['record_id'].astype(str).str.strip()
                df_original['record_id'] = df_original['record_id'].astype(str).str.strip()
                
                # Step 3: Get column names to map (excluding 'record_id')
                col_names = df_map.columns[1:]  # Adjust this to skip 'record_id'
                
                # Step 4: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                for _, row in df_map.iterrows():
                    record_id = row['record_id']
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        mapping_dict[record_id] = row[1:].to_dict()  # Skipping 'record_id'
                
                # Step 5: Apply the mapping to df_original for each domain column
                for col in col_names:
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 6: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)
        
                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x08 - devass.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Ensure 'record_id' is a string and strip extra spaces
                df_map['record_id'] = df_map['record_id'].astype(str).str.strip()
                df_original['record_id'] = df_original['record_id'].astype(str).str.strip()
                
                # Step 3: Get column names to map (excluding 'record_id')
                col_names = df_map.columns[1:]  # Adjust this to skip 'record_id'
                
                # Step 4: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                for _, row in df_map.iterrows():
                    record_id = row['record_id']
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        mapping_dict[record_id] = row[1:].to_dict()  # Skipping 'record_id'
                
                # Step 5: Apply the mapping to df_original for each domain column
                for col in col_names:
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 6: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)
        
                
                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x09 - nbme.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Ensure 'record_id' is a string and strip extra spaces
                df_map['record_id'] = df_map['record_id'].astype(str).str.strip()
                df_original['record_id'] = df_original['record_id'].astype(str).str.strip()
                
                # Step 3: Get column names to map (excluding 'record_id')
                col_names = df_map.columns[1:]  # Adjust this to skip 'record_id'
                
                # Step 4: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                for _, row in df_map.iterrows():
                    record_id = row['record_id']
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        mapping_dict[record_id] = row[1:].to_dict()  # Skipping 'record_id'
                
                # Step 5: Apply the mapping to df_original for each domain column
                for col in col_names:
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 6: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)
        
                
                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x10 - canvasquiz1.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Ensure 'record_id' is a string and strip extra spaces
                df_map['record_id'] = df_map['record_id'].astype(str).str.strip()
                df_original['record_id'] = df_original['record_id'].astype(str).str.strip()
                
                # Step 3: Get column names to map (excluding 'record_id')
                col_names = df_map.columns[1:]  # Adjust this to skip 'record_id'
                
                # Step 4: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                for _, row in df_map.iterrows():
                    record_id = row['record_id']
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        mapping_dict[record_id] = row[1:].to_dict()  # Skipping 'record_id'
                
                # Step 5: Apply the mapping to df_original for each domain column
                for col in col_names:
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 6: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)
                
                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x10 - canvasquiz2.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Ensure 'record_id' is a string and strip extra spaces
                df_map['record_id'] = df_map['record_id'].astype(str).str.strip()
                df_original['record_id'] = df_original['record_id'].astype(str).str.strip()
                
                # Step 3: Get column names to map (excluding 'record_id')
                col_names = df_map.columns[1:]  # Adjust this to skip 'record_id'
                
                # Step 4: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                for _, row in df_map.iterrows():
                    record_id = row['record_id']
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        mapping_dict[record_id] = row[1:].to_dict()  # Skipping 'record_id'
                
                # Step 5: Apply the mapping to df_original for each domain column
                for col in col_names:
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 6: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)
                
                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x10 - canvasquiz3.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Ensure 'record_id' is a string and strip extra spaces
                df_map['record_id'] = df_map['record_id'].astype(str).str.strip()
                df_original['record_id'] = df_original['record_id'].astype(str).str.strip()
                
                # Step 3: Get column names to map (excluding 'record_id')
                col_names = df_map.columns[1:]  # Adjust this to skip 'record_id'
                
                # Step 4: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                for _, row in df_map.iterrows():
                    record_id = row['record_id']
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        mapping_dict[record_id] = row[1:].to_dict()  # Skipping 'record_id'
                
                # Step 5: Apply the mapping to df_original for each domain column
                for col in col_names:
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 6: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)
                
                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x10 - canvasquiz4.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Ensure 'record_id' is a string and strip extra spaces
                df_map['record_id'] = df_map['record_id'].astype(str).str.strip()
                df_original['record_id'] = df_original['record_id'].astype(str).str.strip()
                
                # Step 3: Get column names to map (excluding 'record_id')
                col_names = df_map.columns[1:]  # Adjust this to skip 'record_id'
                
                # Step 4: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                for _, row in df_map.iterrows():
                    record_id = row['record_id']
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        mapping_dict[record_id] = row[1:].to_dict()  # Skipping 'record_id'
                
                # Step 5: Apply the mapping to df_original for each domain column
                for col in col_names:
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 6: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)
        
                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x11 - ptrackero.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Ensure 'record_id' is a string and strip extra spaces
                df_map['record_id'] = df_map['record_id'].astype(str).str.strip()
                df_original['record_id'] = df_original['record_id'].astype(str).str.strip()
                
                # Step 3: Get column names to map (excluding 'record_id')
                col_names = df_map.columns[1:]  # Adjust this to skip 'record_id'
                
                # Step 4: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                for _, row in df_map.iterrows():
                    record_id = row['record_id']
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        mapping_dict[record_id] = row[1:].to_dict()  # Skipping 'record_id'
                
                # Step 5: Apply the mapping to df_original for each domain column
                for col in col_names:
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 6: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)
        
                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x12 - analysis.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Ensure 'record_id' is a string and strip extra spaces
                df_map['record_id'] = df_map['record_id'].astype(str).str.strip()
                df_original['record_id'] = df_original['record_id'].astype(str).str.strip()
                
                # Step 3: Get column names to map (excluding 'record_id')
                col_names = df_map.columns[1:]  # Adjust this to skip 'record_id'
                
                # Step 4: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                for _, row in df_map.iterrows():
                    record_id = row['record_id']
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        mapping_dict[record_id] = row[1:].to_dict()  # Skipping 'record_id'
                
                # Step 5: Apply the mapping to df_original for each domain column
                for col in col_names:
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 6: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)

                import pandas as pd
                import numpy as np
                
                FILETOMAP = "x13 - sdoh.csv"
                ORIGINALA = "mainfile.csv"
                
                # Step 1: Read the mapping file and the original file
                df_map = pd.read_csv(FILETOMAP)
                df_original = pd.read_csv(ORIGINALA, dtype=str)
                
                # Step 2: Ensure 'record_id' is a string and strip extra spaces
                df_map['record_id'] = df_map['record_id'].astype(str).str.strip()
                df_original['record_id'] = df_original['record_id'].astype(str).str.strip()
                
                # Step 3: Get column names to map (excluding 'record_id')
                col_names = df_map.columns[1:]  # Adjust this to skip 'record_id'
                
                # Step 4: Create a dictionary for mapping from the df_map (each record_id maps to a row)
                mapping_dict = {}
                for _, row in df_map.iterrows():
                    record_id = row['record_id']
                    if pd.notna(record_id):  # Skip rows where 'record_id' is NaN
                        mapping_dict[record_id] = row[1:].to_dict()  # Skipping 'record_id'
                
                # Step 5: Apply the mapping to df_original for each domain column
                for col in col_names:
                    df_original[col] = df_original['record_id'].map(lambda x: mapping_dict.get(x, {}).get(col, np.nan))
                
                # Step 6: Save the modified dataframe back to the original file
                df_original.to_csv(ORIGINALA, index=False)
        
        
                import pandas as pd
                import numpy as np
                from datetime import datetime

                # Read the original file
                df_original = pd.read_csv(ORIGINALA)
                
                # List of columns to leave blank
                no_fill_columns = [
                    'quiz_1_late', 'quiz_2_late', 'quiz_3_late', 'quiz_4_late', 
                    'submitted_dev', 'submitted_ce', 'cas_submit_min'
                ]
                
                # Step 1: Replace NaN with 0 in all columns except those listed in no_fill_columns
                df_original = df_original.apply(
                    lambda col: col.fillna(0) if col.name not in no_fill_columns else col
                )
                
                # Step 2: Convert float columns (i.e., columns with decimal points) to integers
                # Convert all columns with numeric values to integer, keeping string columns (like 'record_id') intact
                for col in df_original.columns:
                    if df_original[col].dtype in ['float64', 'int64'] and col not in no_fill_columns:
                        df_original[col] = df_original[col].apply(lambda x: int(x) if x == int(x) else x)

                today_date = datetime.now().strftime('%m/%d/%Y')
                df_original['datez'] = today_date

                # Save the cleaned dataframe to a CSV
                df_original.to_csv(ORIGINALA, index=False)
        
                ########################################################################################
                ########################################################################################
        
                csv_data = df_original.to_csv(index=False)
        
                st.download_button(
                    label="Download Modified CSV",
                    data=csv_data,
                    file_name="mainfile_for_upload.csv",
                    mime="text/csv"
                )
        else:
            st.warning("Some categories are missing. Please ensure all required files are uploaded.")
    else:
        st.warning("Please upload all the required files to proceed.")
        
if __name__ == "__main__":
    main()

