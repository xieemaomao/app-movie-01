import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import re



st.title('Movie data by Siyan Liu and Miaomiao Hou')

df = pd.read_csv('tmdb_5000_movies.csv')
##df = df.sample(600)


df['release_date']=pd.to_datetime(df['release_date'])
df['Time']=pd.to_datetime(df['release_date'])
df['year']=df['release_date'].dt.strftime('%Y')

df['year']=df['year'].fillna(0)
df['year']=df['year'].astype('int')
df_year=df[df['year'] > 2000]

companies_list=[]
for i in range(len(df)):
    if df.loc[i,'production_companies']!="[]":
        result_list = re.findall(r"[{](.*?)[}]", df.loc[i,'production_companies'])
        tmp=json.loads("{"+result_list[0]+"}")
        companies_list.append(tmp['name'])
    else:
        companies_list.append("")
df['companies']=companies_list

country_list=[]
for i in range(len(df)):
    if df.loc[i,'production_countries']!="[]":
        result_list = re.findall(r"[{](.*?)[}]", df.loc[i,'production_countries'])
        tmp1=json.loads("{"+result_list[0]+"}")
        country_list.append(tmp1['name'])
    else:
        country_list.append("")
df['country']=country_list


df_1=df



country_filter = st.sidebar.multiselect(
     'Country Selector',
     df.country.unique(),  # options
     None)  # defaults


year_filter=st.slider('Year',1910,2020,2017)

     

df = df[df.country.isin(country_filter)]  


df=df[df.year <= year_filter]



st.write(df.companies.value_counts())
st.write('there are')
company_counts = st.write(df.companies.nunique())
st.write('movies')
    
plt.style.use('seaborn')

x = np.linspace(1, 10, 20)
fig, ax = plt.subplots(1,2,figsize=(20, 10))

#1
st.subheader('numbers of movie in different countries Top10')
df_country=df_1.groupby('companies')[['country']].max()

fig, ax = plt.subplots(figsize=(20, 10))
df_country.country.value_counts().head(10).plot.bar(ax=ax)
st.pyplot(fig)
plt.show()

#2
st.subheader('vote average after 2000')
fig,ax=plt.subplots()
df2=df_year.groupby('year')[['vote_average','budget']].mean()
df2.vote_average.plot(ax=ax).set_xticks(df2.index, rotation=80)
st.pyplot(fig)


#3
st.subheader('numbers of movies every year after 2000')
fig,ax=plt.subplots()
x=df2.index
y=df_year.year.value_counts()
a2=plt.plot(x,y)
st.pyplot(fig)


#4
st.subheader('Movie production per year')
a=df_year.year.value_counts()
b=list(a) 
##get the number of movie list

df2=df_year.groupby('year')[['vote_average','budget']].mean()
i=0
year_list=[]
while i < len(df2.index):
    year_list.append(df2.index[i])
    i+=1
##get the year list

fig,ax = plt.subplots(figsize=(6,6))

plt.pie(b,
        labels=year_list,
        autopct="%1.2f%%",
        startangle=60,
        )

st.pyplot(fig)

















