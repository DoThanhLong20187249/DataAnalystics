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


#--------the maximum small children and teenagers in customer's household who have done education---------#


#-----------------------------------------------Marital Anaylist-----------------------------------------------------------#
#make data
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



#------------- ProDuction----------------######
fruit_cols = ['MntWines', 
              'MntFruits',
              'MntMeatProducts', 
              'MntFishProducts', 
              'MntSweetProducts',
              'MntGoldProds']

# Simplify names
fruit_dict = {'MntWines': 'Wines', 
              'MntFruits': 'Fruits', 
              'MntMeatProducts': 'Meat', 
              'MntFishProducts': 'Fish', 
              'MntSweetProducts': 'Candy',
              'MntGoldProds': 'Gold products'}
colors = ['#EB7383',
          '#AFD3E2', 
          '#19A7CE', 
          '#146C94',
          '#00FFCA',
          '#088395']
fruits = pd.DataFrame(data[fruit_cols].sum().sort_values(ascending=False))
# Replace names
fruits.index = fruits.index.map(fruit_dict)
# Figure size
fig8 = plt.figure(figsize=(12, 5))
fig_product=sns.barplot(data=fruits,
            x=fruits.index,
            y=0,
            palette=colors)
#config 
fig_product.bar_label(fig_product.containers[0])
sns.despine(left=True)



#-----layout----
st.write('## Dataset of Marking Campaign')
st.dataframe(data, width=1800)
st.write("      ")
st.write("      ")


st.write('## Pie chart to show the ratio of ranges of score of Education')
st.write('''Through the pie chart, we can see that the number 
         of customers with the highest level of education is Graduation, the lowest is Basic education.''')
fig_education
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

#---------------------------Accepted Promotions--------------------------------------------#
campaigns = ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5"]
st.write('## Campaign accept rates ')
st.write('''AcceptedCmp1: 1 if customer accepted the offer in the 1st campaign, 0 otherwise\n
AcceptedCmp2: 1 if customer accepted the offer in the 2nd campaign, 0 otherwise\n
AcceptedCmp3: 1 if customer accepted the offer in the 3rd campaign, 0 otherwise\n
AcceptedCmp4: 1 if customer accepted the offer in the 4th campaign, 0 otherwise\n
AcceptedCmp5: 1 if customer accepted the offer in the 5th campaign, 0 otherwise''')
st.write('''The pie charts below show the percentage of customers who accepted the promotion after the number of offers. 
            Through the chart, we can see that most users do not accept promotional offers'''
         ,unsafe_allow_html=True)
select_box2 = st.selectbox('Please select :', campaigns, index=0)
st.write("The Campaign now is:", select_box2)

accept_rate = (data.groupby(select_box2).size() / data[select_box2].count()) * 100
fig7 = plt.figure(figsize=(10,10))
plt.title(f"Accept Rates For {select_box2}")
plt.pie(accept_rate, labels=data[select_box2].unique(), autopct='%1.2f%%')
plt.show()
fig7

st.write('## Number of selled products')
st.write('''Wines are the most selled product, representing 50 percent of sells. Considering \n 
 wines and meat together, they represent 77.78 percent of selled products.''')
fig8
