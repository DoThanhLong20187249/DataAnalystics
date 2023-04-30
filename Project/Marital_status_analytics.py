import numpy as np
import streamlit as st 
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Analytics Marketing Campaign", page_icon="🇫🇷")
st.sidebar.success("Select a page to view different analytics.")

data = pd.read_csv("D:\ProjetctDataVisual\Project\marketing_campaign.csv",sep="\t")

#clean Data

data.Income=data.Income.fillna(data.Income.median())

#--------------Changing Object to Data time dtypes----------------------

data["year"]=pd.to_datetime(data.Dt_Customer,format='%d-%m-%Y').dt.year
data["month"]=pd.to_datetime(data.Dt_Customer,format='%d-%m-%Y').dt.month







count_marital_status = data['Marital_Status'].value_counts()
type_marital_status = ['Married','Together','Single','Divorced','Widow','Alone','Absurd','YOLO']
df1 = pd.DataFrame({
    'Count':count_marital_status[:],
    'Type of marital status': type_marital_status
})

#Bar chart for display the amount of each type of marital status
fig_bar_marital_status = px.bar(df1,x='Type of marital status',y='Count',color="Type of marital status")  


#pie chart for display the amount of each type of marital status
fig_pie_marital_status = px.pie(df1,values=count_marital_status,names=type_marital_status ,title= "Marital status")  

#------Number of contents by Marital showed by Response
df_Marital_Status = data.groupby(['Marital_Status']).count()['ID'].to_frame().reset_index()
df_Marital_Status = df_Marital_Status.sort_values('ID',ascending=False)
list_c_1 = df_Marital_Status['Marital_Status']
top_8_data_1 = data[data['Marital_Status'].isin(list_c_1)]
df_new_1 = top_8_data_1.groupby(['Marital_Status','Response']).count()['ID'].to_frame().reset_index()

fig5 = plt.figure(figsize=(15,20))
sns.barplot(x="Marital_Status", y="ID", hue="Response",data= df_new_1)
plt.xlabel("")
plt.title('Shows by Marital_Status')
plt.ylabel("Amount")


#countplot for marital status according to education
fig6 = plt.figure(figsize=(12,8))
sns.countplot(x="Marital_Status", hue="Education", data=data)



st.write('## Bar chart to show the amountof Marital Status')
st.write('''The number of customers whose marital status is married ranks first among marital status categories, 
            with the lowest being YOLO, absurd, and Alone.''')
fig_bar_marital_status
st.write("      ")
st.write("      ")

st.write('## Pie chart to show the ratio ranges score of Marital Status')
st.write('''Through the pie chart, we can see that the number 
         of  Marital Status with the highest level of  Marital Status is Married, the lowest is Alone,YOLO,Absurd.''')
fig_pie_marital_status
st.write("      ")
st.write("      ")


st.write("## Bar chart shows the number of contents in  Marital Status")
st.write('''<b>Response: 1 if customer accepted the offer in the last campaign, 0 otherwise </b>''', unsafe_allow_html=True)
st.write(''' 
As you can see in the last campaign, the number of clients with a marital status didn't accept the offer. 
In second place are those whose marital status is Together. 
But instead, those with marital status as single accepted the highest in the last campaign''')
fig5
st.write("      ")
st.write("      ")

st.write("## Education level with Marital Status")
st.write('''Below is a bar chart showing that education levels are concentrated in customers whose marital status is married.''')
st.write('''We find that education Graduation is the highest of all education categories and it is highest in marital status as married''',unsafe_allow_html=True)
fig6