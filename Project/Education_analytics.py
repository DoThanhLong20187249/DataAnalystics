import numpy as np
import streamlit as st 
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analytics Education", page_icon="🇫🇷")
st.sidebar.success("Select a page to view different analytics.")

data = pd.read_csv("D:\ProjetctDataVisual\Project\marketing_campaign.csv",sep="\t")

#clean Data

data.Income=data.Income.fillna(data.Income.median())

#--------------Changing Object to Data time dtypes----------------------

data["year"]=pd.to_datetime(data.Dt_Customer,format='%d-%m-%Y').dt.year
data["month"]=pd.to_datetime(data.Dt_Customer,format='%d-%m-%Y').dt.month

#------------------------ people have completed their qualification-----------------------

#make dataFrame
count_education =data['Education'].value_counts()
type_education = ['Graduation', 'Phd', 'Master','2n Cycle','Basic']
df = pd.DataFrame({
    'Count': count_education[:],
    'Type of education': type_education
})


#Pie chart for display the amount of each type of Education
fig_education = px.pie(df,values=count_education,names=type_education ,title="Education")

fig_education.update_layout(
    title_font=dict(size=25, color='#8a8d93', family="Lato, sans-serif"),
    plot_bgcolor='#333',
    paper_bgcolor='#444',
    legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="center", x=0.5),
    font=dict(color='#8a8d93'),
)
#Bar chart for display the amount of each Type of education
fig_bar_education = px.bar(df,x='Type of education',y='Count',color="Type of education")  

#------Number of contents by Education showed by Response
df_education = data.groupby(['Education']).count()['ID'].to_frame().reset_index()
df_education = df_education.sort_values('ID',ascending=False)
list_c = df_education['Education']
top_8_data = data[data['Education'].isin(list_c)]
df_new = top_8_data.groupby(['Education','Response']).count()['ID'].to_frame().reset_index()

fig4 = plt.figure(figsize=(15,10))
sns.barplot(x="Education", y="ID", hue="Response",data= df_new)
plt.xlabel("")
plt.title('Shows by Education')
plt.ylabel("Amount")


#-------In Education,why type of marital status was having highest monthly income-----#

fig_3 = plt.figure(figsize=(15,15))
sns.lineplot(x='month',y='Income',hue='Education',data=data)
plt.title('Monthly vs Income')



#-----layout----
st.write('## Dataset of Marking Campaign')
st.dataframe(data, width=1800)
st.write("      ")
st.write("      ")


st.write('## Pie and Bar chart to show the ratio of ranges of score of Education')
st.write('''Through the pie and Bar chart , we can see that the number 
         of customers with the highest level of education is Graduation, the lowest is Basic education.''')
fig_education
fig_bar_education
st.write("      ")
st.write("      ")


st.write('## Linechart to show In Education was having highest monthly income ')
st.write('''<b>x-Month, y-Income</b>''', unsafe_allow_html=True)
fig_3
st.write("      ")
st.write("      ")

st.write("## Bar chart shows the number of contents in  Education")
st.write('''<b>Response: 1 if customer accepted the offer in the last campaign, 0 otherwise</b>''', unsafe_allow_html=True)
fig4
st.write("      ")
st.write("      ")
