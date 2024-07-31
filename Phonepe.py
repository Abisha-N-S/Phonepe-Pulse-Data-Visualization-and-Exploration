import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as px
import requests
import json
from PIL import Image

#SQL creation
mydb = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Abisha123,",
    database="phonepe",
    port="5432"
)

cursor = mydb.cursor()

#Aggregated Insurance
cursor.execute("select * from agg_insurance")
mydb.commit()
t1=cursor.fetchall()
Aggre_insurance=pd.DataFrame(t1, columns=("State", "Year", "Quarter", "Transaction_type", 
                                            "Transaction_count", "Transaction_amount"))

#Aggregated transaction
cursor.execute("select * from agg_transaction")
mydb.commit()
t2=cursor.fetchall()
Aggre_transaction=pd.DataFrame(t2, columns=("State", "Year", "Quarter", "Transaction_type", 
                                            "Transaction_count", "Transaction_amount"))

#Aggregated user
cursor.execute("select * from agg_user")
mydb.commit()
t3=cursor.fetchall()
Aggre_user=pd.DataFrame(t3, columns=("State", "Year", "Quarter", " Brand", 
                                            "Transaction_count", "Percentage"))

#Map  insurance
cursor.execute("select * from map_insurance")
mydb.commit()
t4=cursor.fetchall()
Map_insurance=pd.DataFrame(t4, columns=("State", "Year", "Quarter", "Districts", 
                                            "Transaction_count", "Transaction_amount"))

#Map transaction
cursor.execute("select * from map_transaction")
mydb.commit()
t5=cursor.fetchall()
Map_transaction=pd.DataFrame(t5, columns=("State", "Year", "Quarter", "Districts", 
                                            "Transaction_count", "Transaction_amount"))

#Map user
cursor.execute("select * from map_user")
mydb.commit()
t6=cursor.fetchall()
Map_user=pd.DataFrame(t6, columns=("State", "Year", "Quarter", "Districts", 
                                            "RegisteredUsers", "AppOpens"))

#Top Insurance
cursor.execute("select * from top_insurance")
mydb.commit()
t7=cursor.fetchall()
Top_insurance=pd.DataFrame(t7, columns=("State", "Year", "Quarter", "Pincodes", 
                                            "Transaction_count", "Transaction_amount"))

#Top transaction
cursor.execute("select * from top_transaction")
mydb.commit()
t8=cursor.fetchall()
Top_transaction=pd.DataFrame(t8, columns=("State", "Year", "Quarter", "Pincodes", 
                                            "Transaction_count", "Transaction_amount"))

#Top user
cursor.execute("select * from top_user")
mydb.commit()
t9=cursor.fetchall()
Top_user=pd.DataFrame(t9, columns=("State", "Year", "Quarter", "Pincodes", 
                                            "RegisteredUsers"))

#Year based Transaction
def trans_amount_count(df, year):
    trans_ac=df[df["Year"]==year]
    trans_ac.reset_index(drop=True, inplace=True)

    trans_acy=trans_ac.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    trans_acy.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(trans_acy, x="State", y="Transaction_amount", title=f"{year} Transaction amount",
        color_discrete_sequence=px.colors.sequential.Bluyl_r, height=650, width=600) 
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(trans_acy, x="State", y="Transaction_count", title=f"{year} Transaction count", 
        color_discrete_sequence=px.colors.sequential.Reds_r, height=650, width=600)
        st.plotly_chart(fig_count)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data=json.loads(response.content)
    state=[]
    for i in data["features"]:
        state.append(i["properties"]["ST_NM"])

    state.sort()
    col1, col2=st.columns(2)
    with col1:
        fig_india=px.choropleth(trans_acy, geojson=data, locations="State", featureidkey="properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale="Greens",
                                range_color=(trans_acy["Transaction_amount"].min(),trans_acy["Transaction_amount"].max()),
                                hover_name="State", title=f"{year} Tranaction amount", fitbounds="locations", 
                                height=600, width=600)
        fig_india.update_geos(visible= False)
        st.plotly_chart(fig_india)
    with col2:
        fig_india1=px.choropleth(trans_acy, geojson=data, locations="State", featureidkey="properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale="Reds",
                                range_color=(trans_acy["Transaction_count"].min(),trans_acy["Transaction_count"].max()),
                                hover_name="State", title=f"{year} Tranaction count", fitbounds="locations", 
                                height=600, width=600)
        fig_india1.update_geos(visible= False)
        st.plotly_chart(fig_india1)
    return trans_ac

#Quarter based Transaction
def trans_ac_q(df, quarter):
    trans_ac=df[df["Quarter"]==quarter]
    trans_ac.reset_index(drop=True, inplace=True)

    trans_acy=trans_ac.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    trans_acy.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(trans_acy, x="State", y="Transaction_amount", 
                    title=f"{trans_ac["Year"].min()} Year {quarter} Quarter Transaction amount") 
        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(trans_acy, x="State", y="Transaction_count", 
        title=f"{trans_ac["Year"].min()} Year {quarter} Quarter Transaction count")
        st.plotly_chart(fig_count)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data=json.loads(response.content)
    state=[]
    
    for i in data["features"]:
        state.append(i["properties"]["ST_NM"])

    state.sort()
    col1,col2=st.columns(2)
    with col1:
        fig_india=px.choropleth(trans_acy, geojson=data, locations="State", featureidkey="properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale="Greens",
                                range_color=(trans_acy["Transaction_amount"].min(),trans_acy["Transaction_amount"].max()),
                                hover_name="State", title=f"{trans_ac["Year"].min()} Year {quarter} Quarter Tranaction amount", fitbounds="locations", 
                                height=600, width=600)
        fig_india.update_geos(visible= False)
        st.plotly_chart(fig_india)
    with col2:
        fig_india1=px.choropleth(trans_acy, geojson=data, locations="State", featureidkey="properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale="Reds",
                                range_color=(trans_acy["Transaction_count"].min(),trans_acy["Transaction_count"].max()),
                                hover_name="State", title=f"{trans_ac["Year"].min()} Year {quarter} Quarter Tranaction count", fitbounds="locations", 
                                height=600, width=600)
        fig_india1.update_geos(visible= False)
        st.plotly_chart(fig_india1)
    return trans_ac

#Transaction type
def Agg_trans_type(df, state):
    trans_ac=df[df["State"]==state]
    trans_ac.reset_index(drop=True, inplace=True)

    trans_acy=trans_ac.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    trans_acy.reset_index(inplace=True)

    clm1,clm2=st.columns(2)
    with clm1:
        fig_pie_am=px.pie(data_frame=trans_acy, names="Transaction_type", values="Transaction_amount", width=600,
                            title=f"{state} Transaction Amount", hole=0.5)
        st.plotly_chart(fig_pie_am)
    with clm2:
        fig_pie_co=px.pie(data_frame=trans_acy, names="Transaction_type", values="Transaction_count", width=600,
                            title=f"{state} Transaction Count", hole=0.5)
        st.plotly_chart(fig_pie_co)

# Aggre_User_analysis_1
def Aggre_user_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brand")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x= "Brand", y= "Transaction_count", title= f"{year} BRAND AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.haline_r, hover_name= "Brand")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggre_user_Analysis_2
def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brand")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x= "Brand", y= "Transaction_count", title=  f"{quarter} QUARTER, BRAND AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name="Brand")
    st.plotly_chart(fig_bar_1)

    return aguyq

#Aggre_user_alalysis_3
def Aggre_user_plot_3(df, state):
    auyqs= df[df["State"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brand", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRAND, TRANSACTION COUNT, PERCENTAGE",width= 1000, markers= True)
    st.plotly_chart(fig_line_1)

#Map_insurance_district
def Map_insur_District(df, state):

    trans_ac= df[df["State"] == state]
    trans_ac.reset_index(drop = True, inplace= True)

    trans_acy= trans_ac.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    trans_acy.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(trans_acy, x= "Transaction_amount", y= "Districts", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2= px.bar(trans_acy, x= "Transaction_count", y= "Districts", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

# map_user_plot_1
def map_user_plot_1(df, year):
    muy= df[df["Year"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("State")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "State", y= ["RegisteredUser", "AppOpens"],
                        title= f"{year} REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

# map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("State")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "State", y= ["RegisteredUser", "AppOpens"],
                        title= f"{df['Year'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["State"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUser", y= "Districts", orientation= "h",
                                title= f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:

        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "Districts", orientation= "h",
                                title= f"{states.upper()} APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

# top_insurance_plot_1
def Top_insurance_plot_1(df, state):
    tiy= df[df["State"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                                title= "TRANSACTION AMOUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:

        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= "Pincodes",
                                title= "TRANSACTION COUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)

def top_user_plot_1(df, year):
    tuy= df[df["Year"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["State", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "State", y= "RegisteredUsers", color= "Quarter", width= 1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "State",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

# top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["State"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_pot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= "REGISTEREDUSERS, PINCODES, QUARTER",
                        width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_pot_2)

#sql connection
def top_chart_transaction_amount(table_name):
    mydb = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Abisha123,",
    database="phonepe",
    port="5432"
    )

    cursor = mydb.cursor()
    #plot_1
    query1= f'''SELECT state, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY state
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("state", "transaction_amount"))

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="state", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "state",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT state, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY state
                ORDER BY transaction_amount
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("state", "transaction_amount"))

    with col2:
        fig_amount_2= px.bar(df_2, x="state", y="transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "state",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT state, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY state
                ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("state", "transaction_amount"))

    fig_amount_3= px.bar(df_3, y="state", x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "state", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_transaction_count(table_name):
    mydb = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Abisha123,",
    database="phonepe",
    port="5432"
    )

    cursor = mydb.cursor()

    #plot_1
    query1= f'''SELECT state, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY state
                ORDER BY transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("state", "transaction_count"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="state", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "state",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

     #plot_2
    query2= f'''SELECT state, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY state
                ORDER BY transaction_count
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("state", "transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x="state", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "state",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT state, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY state
                ORDER BY transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("state", "transaction_count"))

    fig_amount_3= px.bar(df_3, y="state", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "state", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_registered_user(table_name, state):
    mydb = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Abisha123,",
    database="phonepe",
    port="5432"
    )

    cursor = mydb.cursor()

    #plot_1
    query1= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "registereduser"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="districts", y="registereduser", title="TOP 10 OF REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "registereduser"))

    with col2:
        fig_amount_2= px.bar(df_2, x="districts", y="registereduser", title="LAST 10 REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "registereduser"))

    fig_amount_3= px.bar(df_3, y="districts", x="registereduser", title="AVERAGE OF REGISTERED USER", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_appopens(table_name, state):
    mydb = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="Abisha123,",
        database="phonepe",
        port="5432"
    )

    cursor = mydb.cursor()

    #plot_1
    query1= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "appopens"))


    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="districts", y="appopens", title="TOP 10 OF APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "appopens"))

    with col2:

        fig_amount_2= px.bar(df_2, x="districts", y="appopens", title="LAST 10 APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "appopens"))

    fig_amount_3= px.bar(df_3, y="districts", x="appopens", title="AVERAGE OF APPOPENS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_registered_users(table_name):
    mydb = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Abisha123,",
    database="phonepe",
    port="5432"
    )

    cursor = mydb.cursor()

    #plot_1
    query1= f'''SELECT state, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY state
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("state", "registeredusers"))

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="state", y="registeredusers", title="TOP 10 OF REGISTERED USERS", hover_name= "state",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT state, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY state
                ORDER BY registeredusers
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("state", "registeredusers"))

    with col2:

        fig_amount_2= px.bar(df_2, x="state", y="registeredusers", title="LAST 10 REGISTERED USERS", hover_name= "state",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT state, AVG(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY state
                ORDER BY registeredusers;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("state", "registeredusers"))

    fig_amount_3= px.bar(df_3, y="state", x="registeredusers", title="AVERAGE OF REGISTERED USERS", hover_name= "state", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#streamlit
st.set_page_config(layout= "wide")
st.title("Phonepe Data Visualization and Exploration")
#st.image("https://cdn3.freelogovectors.net/wp-content/uploads/2023/01/phonepe-logo-freelogovectors.net_.png", width=250)

#side bar
with st.sidebar:
    select=option_menu("Main menu",["Home","Explore data","Top chats"])

if select=="Home":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"D:\Data Science\Project2\Ph image.png"),width= 600)

    col3,col4= st.columns(2)

    with col3:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    with col4:
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

elif select=="Explore data":
    tab1, tab2, tab3=st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method1 =st.radio("Select the Methods",["Aggregated Insurance Analysis","Aggregated Transaction Analysis","Aggregated User Analysis"])

        if method1=="Aggregated Insurance Analysis":
            clm1, clm2=st.columns(2)
            with clm1:
                years=st.slider("Select the year", Aggre_insurance["Year"].min(), 
                         Aggre_insurance["Year"].max(), Aggre_insurance["Year"].min())
            trans_ac=trans_amount_count(Aggre_insurance, years)

            col1,col2=st.columns(2)
            with col1:
                quarter=st.slider("Select the quarter", trans_ac["Quarter"].min(), 
                        trans_ac["Quarter"].max(), Aggre_insurance["Quarter"].min())
            trans_ac_q(trans_ac, quarter)

        elif method1=="Aggregated Transaction Analysis":
            clm1, clm2=st.columns(2)
            with clm1:
                years=st.slider("Select the year", Aggre_transaction["Year"].min(), 
                         Aggre_transaction["Year"].max(), Aggre_transaction["Year"].min())
            Agg_tran_ac=trans_amount_count(Aggre_transaction, years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select State", Agg_tran_ac["State"].unique())
            Agg_trans_type(Agg_tran_ac, states)

            col1,col2=st.columns(2)
            with col1:
                quarter=st.slider("Select the quarter", Agg_tran_ac["Quarter"].min(), 
                        Agg_tran_ac["Quarter"].max(), Agg_tran_ac["Quarter"].min())
            Agg_tran_ac_q= trans_ac_q(Agg_tran_ac, quarter)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State", Agg_tran_ac_q["State"].unique())
            Agg_trans_type(Agg_tran_ac_q, states)

        elif method1=="Aggregated User Analysis":

            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select The Year",Aggre_user["Years"].min(), Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y= Aggre_user_plot_1(Aggre_user, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)

    with tab2:
        method2 =st.radio("Select the Methods",["Map Insurance","Map Transaction","Map User"])
        if method2=="Map Insurance":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mi",Map_insurance["Year"].min(), Map_insurance["Year"].max(),Map_insurance["Year"].min())
            map_insur_tac_Y= trans_amount_count(Map_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mi", map_insur_tac_Y["State"].unique())

            Map_insur_District(map_insur_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mi",map_insur_tac_Y["Quarter"].min(), map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min())
            map_insur_tac_Y_Q= trans_ac_q(map_insur_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_Ty", map_insur_tac_Y_Q["State"].unique())

            Map_insur_District(map_insur_tac_Y_Q, states)
        elif method2=="Map Transaction":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",Map_transaction["Year"].min(), Map_transaction["Year"].max(),Map_transaction["Year"].min())
            map_tran_tac_Y= trans_amount_count(Map_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mi", map_tran_tac_Y["State"].unique())

            Map_insur_District(map_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mt",map_tran_tac_Y["Quarter"].min(), map_tran_tac_Y["Quarter"].max(),map_tran_tac_Y["Quarter"].min())
            map_tran_tac_Y_Q= trans_ac_q(map_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_Ty", map_tran_tac_Y_Q["State"].unique())

            Map_insur_District(map_tran_tac_Y_Q, states)
        elif method2=="Map User":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mu",Map_user["Year"].min(), Map_user["Year"].max(),Map_user["Year"].min())
            map_user_Y= map_user_plot_1(Map_user, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mu",map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q= map_user_plot_2(map_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_mu", map_user_Y_Q["State"].unique())

            map_user_plot_3(map_user_Y_Q, states)

    with tab3:
        method3 =st.radio("Select the Methods",["Top Insurance","Top Transaction","Top User"])
        if method3=="Top Insurance":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_ti",Top_insurance["Year"].min(), Top_insurance["Year"].max(),Top_insurance["Year"].min())
            top_insur_tac_Y= trans_amount_count(Top_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_ti", top_insur_tac_Y["State"].unique())

            Top_insurance_plot_1(top_insur_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mu",top_insur_tac_Y["Quarter"].min(), top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())
            top_insur_tac_Y_Q= trans_ac_q(top_insur_tac_Y, quarters)

        elif method3=="Top Transaction":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_tt",Top_transaction["Year"].min(), Top_transaction["Year"].max(),Top_transaction["Year"].min())
            top_tran_tac_Y= trans_amount_count(Top_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tt", top_tran_tac_Y["State"].unique())

            Top_insurance_plot_1(top_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_tt",top_tran_tac_Y["Quarter"].min(), top_tran_tac_Y["Quarter"].max(),top_tran_tac_Y["Quarter"].min())
            top_tran_tac_Y_Q= trans_ac_q(top_tran_tac_Y, quarters)
        elif method3=="Top User":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_tu",Top_user["Year"].min(), Top_user["Year"].max(),Top_user["Year"].min())
            top_user_Y= top_user_plot_1(Top_user, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tu", top_user_Y["State"].unique())

            top_user_plot_2(top_user_Y, states)

elif select=="Top chats":
    question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. App opens of Map User",
                                                    "10. Registered users of Top User",
                                                    ])

    if question == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question == "6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "8. Registered users of Map User":

        states= st.selectbox("Select the State", map_user["States"].unique())   
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user", states)

    elif question == "9. App opens of Map User":

        states= st.selectbox("Select the State", map_user["States"].unique())   
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)

    elif question == "10. Registered users of Top User":

        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")