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

#create Color
colors = ['#EB7383',
          '#AFD3E2', 
          '#19A7CE', 
          '#146C94',
          '#00FFCA',
          '#088395']
#-----------------------------------Birth_Year-------------------#
gen_order = ['Silent Generation (<=1945)', 'Baby Boomers (1946-1964)',
             'Gen X (1965-1980)', 'Millennials (1981-1996)']

df_birth_year = data.groupby('Year_Birth')['ID'].count().reset_index()
df_birth_year.columns = ['Birth Year', 'Customer Count']

fig = px.bar(df_birth_year, x='Birth Year', y='Customer Count', title='Birth Year')
fig.update_layout(yaxis_title=None, xaxis_title=None)

def birth_year_generation(birth_year):
    if birth_year <= 1945:
        return 'Silent Generation (<=1945)'
    if birth_year <= 1964:
        return 'Baby Boomers (1946-1964)'
    if birth_year <= 1980:
        return 'Gen X (1965-1980)'
    if birth_year <= 1996:
        return 'Millennials (1981-1996)'
    if birth_year <= 2012:
        return 'Gen Z (1997-2012)'
    return 'Gen Alpha (>=2012)'

data['Generation'] = data['Year_Birth'].apply(birth_year_generation)
df_Generation = data['Generation'].value_counts().reset_index()
df_Generation.columns = ['Generation', 'Count']

fig1 = px.pie(df_Generation, values='Count', names='Generation', title='Generation',
             category_orders={'Generation': gen_order})



#---------------------------Accepted Promotions--------------------------------------------#
columns = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']
promotions = pd.DataFrame(data[columns].sum())

# Plot figure
fig9 = plt.figure(figsize=(10,10))
fig_promotion= sns.barplot(data=promotions, 
            y=0, 
            x=promotions.index,
            palette=colors)
fig_promotion.bar_label(fig_promotion.containers[0])
sns.despine(left=True)



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

#----------------Layout----------------------#
st.write('## Birth Year nalytics')
st.write('The number of customers is usually concentrated in about 1965-1980')
fig
fig1

st.write('## Number of accepted promotions')
st.write('''the 3 most recent promotions had a lot of acceptions, so the marketing campaign is more accurate over time.''')
fig9


st.write('## Number of selled products')
st.write('''Wines are the most selled product, representing 50 percent of sells. Considering \n 
wines and meat together, they represent 77.78 percent of selled products.''')
fig8

