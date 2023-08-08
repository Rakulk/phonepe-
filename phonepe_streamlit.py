import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pymysql
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(
    page_title="Phonepe Pulse Data Visualization | By Rakul K",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': """# This dashboard app is created by *Rakul K*!
                           Data has been cloned from Phonepe Pulse Github Repo"""}
)

st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")

with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
    
if selected == "Home":
    
    image = Image.open('phonepe_logo.png')
    st.image(image)
    st.video("C:\\Users\\Admin\\Desktop\\phonepe\\PhonePe_bike_insurance_ah_verum_1.50_roobaiku_perunga.__VJ32fT89sJI_247.webm",start_time=0)
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts  are used to get some insights.")
        if st.button("DOWNLOAD THE APP NOW"):
            st.write("Download for a better experience")
            st.markdown('[Click here to download](https://www.phonepe.com/app-download/)', unsafe_allow_html=True)

        
        
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
        
# Top Charts - TRANSACTIONS
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="Rakul1999",
        autocommit=True)
    mycursor=mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    mycursor.execute("USE phonepe")

    if Type == "Transactions":
        col1,col2,col3= st.columns([1,1,1],gap="small")
        
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select States, sum(Transaction_Count) as Total_Transactions_Count,sum(Transaction_Amount),Transaction_Year as Total from agg_trans where Transaction_Year = {Year} and quarters = {Quarter} group by States,Transaction_Year order by Total desc limit 10;")
            df = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Transactions_Count','Total_Amount','Transaction_Year '])
            fig = px.pie(df, values='Total_Amount',
                             names='States',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district, sum(count) as Total_Transactions_Count,sum(amount) as total_amount,Transaction_Year from top_trans_ds where Transaction_Year = {Year} and quarters = {Quarter} group by district,Transaction_Year order by total_amount desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount','Transaction_Year'])
            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select states,pincode, sum(count) as Total_Transactions_Count,sum(amount) as Total,Transaction_Year from top_trans_pn where Transaction_Year = {Year} and quarters = {Quarter} group by states,pincode,Transaction_Year order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['states','Pincode', 'Transactions_Count','Total_Amount','Transaction_Year'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
# Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4= st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :violet[Brands]")
            mycursor.execute(f"select brand, sum(Transaction_Count) as Total_Count,Quarters,avg(percentage)*100 as Avg_Percentage from agg_users where Transaction_Year = {Year} and quarters = {Quarter} group by brand,Quarters,Transaction_Count order by Total_Count desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Quarters','Avg_Percentage'])
            fig = px.bar(df,
                            title='Top 10',
                            x="Total_Users",
                            y="Brand",
                            orientation='h',
                            color='Avg_Percentage',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True) 
        
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select states,district, sum(Registered_users) as Total_Users,Transaction_Year,Quarters from top_users_ds where Transaction_Year = {Year} and quarters = {Quarter} group by states,district,Transaction_Year,Quarters order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['states','District', 'Total_Users','Transaction_Year','Quarters'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select states,Pincode, sum(Registered_users) as Total_Users,Transaction_Year,Quarters from top_users_pn where Transaction_Year = {Year} and quarters = {Quarter} group by states,Pincode,Transaction_Year,Quarters order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['states','Pincode', 'Total_Users','Transaction_Year','Quarters'])
            fig = px.scatter(df, x="Pincode", y="Total_Users",
                 color="Pincode")
            
            st.plotly_chart(fig,use_container_width=True)
        
        with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select states, sum(registered_users) as Total_Users, sum(app_open) as Total_Appopens,Transaction_Year,Quarters from map_users where Transaction_Year = {Year} and quarters = {Quarter} group by states,Transaction_Year,Quarters order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens','Transaction_Year','Quarters'])
            fig = px.pie(df, values='Total_Users',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Appopens'],
                                labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
    
    # EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            password="Rakul1999",
            autocommit=True)
        mycursor=mydb.cursor()
        mycursor.execute("SHOW DATABASES")
        mycursor.execute("USE phonepe")
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select states, sum(count) as Total_Transactions, sum(amount) as Total_amount,Transaction_Year,Quarters from map_trans where Transaction_Year = {Year} and quarters = {Quarter} group by states,Transaction_Year,Quarters order by states")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['states', 'Total_Transactions', 'Total_amount','Transaction_Year','Quarters'])
            
            fig = px.line(df1,x ='states' ,
              y ='Total_amount',
              title = 'Overall State Data - TRANSACTIONS AMOUNT')
          
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"select states, sum(count) as Total_Transactions, sum(amount) as Total_amount,Transaction_Year,Quarters from map_trans where Transaction_Year = {Year} and quarters = {Quarter} group by states,Transaction_Year,Quarters order by states")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['states', 'Total_Transactions', 'Total_amount','Transaction_Year','Quarters'])
            
            fig = px.histogram(df1, x="states",y='Total_Transactions')
            
            st.plotly_chart(fig,use_container_width=True)
        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions,sum(Transaction_amount) as Total_amount from agg_trans where Transaction_Year = {Year} and quarters = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
        
        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select States, District,Transaction_Year,Quarters, sum(count) as Total_Transactions, sum(amount) as Total_amount from top_trans_ds where Transaction_Year = {Year} and Quarters = {Quarter} and States = '{selected_state}' group by States, District,Transaction_Year,Quarters order by states,district")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['States','District','Transaction_Year','Quarters',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
        
        # EXPLORE DATA - USERS      
    if Type == "Users":
        
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            password="Rakul1999",
            autocommit=True)
        mycursor=mydb.cursor()
        mycursor.execute("SHOW DATABASES")
        mycursor.execute("USE phonepe")
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select states, sum(registered_users) as Total_Users, sum(app_open) as Total_Appopens from map_users where Transaction_Year = {Year} and Quarters = {Quarter} group by states order by states")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['states', 'Total_Users','Total_Appopens'])
        fig = px.pie(df1, values="Total_Appopens",
             names="states",
             color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig,use_container_width=True)
        
        #BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select States,Transaction_Year,quarters,District,sum(registered_users) as Total_Users, sum(app_open) as Total_Appopens from map_users where Transaction_Year = {Year} and quarters = {Quarter} and states = '{selected_state}' group by States, District,Transaction_Year,quarters order by states,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['States','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

                
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
        st.write("**:violet[My Project GitHub link]** ⬇️")
        st.write("https://github.com/Rakulk/phonepe-.git")
        st.write("**:violet[My linkedln link]** ⬇️")
        st.write("www.linkedin.com/in/rakul-k-9148241b5")
        
