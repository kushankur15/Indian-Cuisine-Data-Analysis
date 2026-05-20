import streamlit as st
import plotly.express as px
import pandas as pd
import streamlit.components.v1 as components
st.set_page_config(layout="wide")

df = pd.read_csv("swiggy_vs_zomato_3000.csv")

st.title('Indian Cuisine Dashboard')
st.caption('Based on Zomato and Swiggy data')


options = st.selectbox(
    "Choose An Interactive Chart To Visualize",
    ["Average Dinning Cost Based On City",
     "Average Dinning Cost Based On Cuisine",
     "Swiggy-Zomato Average Ratings over Cuisine",
     "Monthly Orders Based On Cuisine",
     "Estimated Monthly Orders Based On City",
     "Estimated Net Profit Based On City"]
)

cuisines = df['cuisines'].value_counts()
valid_cuisines = cuisines[cuisines > 7].index
cuisine_df = df[df['cuisines'].isin(valid_cuisines)]


if options == "Average Dinning Cost Based On City":
    city_cost = df.groupby('city')['avg_cost_per_person_inr'].median().reset_index()
    fig_1 = px.bar(
        city_cost,
        x='avg_cost_per_person_inr',
        y='city',
        orientation='h',
        color_discrete_sequence=['cyan']
    )
    col1, col2 = st.columns([3,1])

    with col1:
        st.subheader("Average Dinning Cost Per Person")
        st.plotly_chart(fig_1, use_container_width=True)
    with col2:
        st.subheader("Insights")
        st.write(
            '''
            • Mumbai, Ahmedabad and Delhi shows higher median dinning cost more than 860 INR\n
            • Kolkata shows a least dining cost with less than 800 INR
            '''
        )



elif options == "Average Dinning Cost Based On Cuisine":
    selected_cuisines = st.multiselect(
        "Select Cuisines",
        options=sorted(valid_cuisines),
        default=sorted(valid_cuisines)[:10]
    )   
    filtered_df = cuisine_df[
        cuisine_df['cuisines'].isin(selected_cuisines)
    ]
    avg_cost_cuisine = (
        filtered_df
        .groupby('cuisines')['avg_cost_per_person_inr']
        .median()
        .reset_index()
    )

    fig = px.bar(
        avg_cost_cuisine,
        y='cuisines',
        x='avg_cost_per_person_inr',
        orientation='h',
        color_discrete_sequence=["#40ffac"]
    )

    col1, col2 = st.columns([3,1])

    with col1:
        st.subheader("Average Dining Cost per Person Based on Cuisine")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Insights")
        st.write(
            '''
            • Chinese, Italian and Mughlai show higher median cost

            • Street Food, Cafe and Biryani show lower median cost
            '''
        )


elif options=="Swiggy-Zomato Average Ratings over Cuisine":
    selected_cuisines = st.multiselect(
        "Select Cuisines",
        options=sorted(valid_cuisines),
        default=sorted(valid_cuisines)[:10]
    )   
    filtered_df = cuisine_df[
        cuisine_df['cuisines'].isin(selected_cuisines)
    ]
    ratings_df = pd.melt(
        filtered_df,
        id_vars='cuisines',
        value_vars=['swiggy_rating', 'zomato_rating'],
        var_name='platform',
        value_name='ratings'
    )

    ratings_df['platform'] = ratings_df['platform'].replace({
        'swiggy_rating': 'Swiggy',
        'zomato_rating': 'Zomato'
    })
    ratings_df_new = ratings_df.groupby(['cuisines','platform'])['ratings'].mean().reset_index()

    fig = px.bar(
        ratings_df_new,
        x='cuisines',
        y='ratings',
        color='platform',
        color_discrete_map={
        'Swiggy': '#ff7a1a',
        'Zomato': '#ff2d2d'
    },
        barmode='group'
    )

    col1, col2 = st.columns([3,1])
    with col1:
        st.subheader("Swiggy-Zomato Average Ratings over Cuisine")
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        st.subheader("Insights")
        st.write(
            '''
                • 5 cuisines have more ratings on Swiggy than Zomato\n
                • 10 cuisines have more ratings on Zomato than Swiggy\n
                • 7 cuisines have almost same ratings on Zomato and Swiggy\n
                • Lebanese Cuisine has the highest average rating of 4.087 on Swiggy\n
                • Mughlai Cuisine has the lowest average rating of 3.88 on Swiggy\n
                • North Indian Cuisine has the highest rating of 4.087 on Zomato\n
                • Seafood Cuisine has the lowest rating of 3.944 on Zomato\n
            '''
        )
    with open("ratings.html", "r") as f:
        html_code = f.read()

    st.components.v1.html(html_code, height=500)



elif options=="Monthly Orders Based On Cuisine":
    selected_cuisines = st.multiselect(
        "Select Cuisines",
        options=sorted(valid_cuisines),
        default=sorted(valid_cuisines)[:21]
    )   
    filtered_df = cuisine_df[
        cuisine_df['cuisines'].isin(selected_cuisines)
    ]
    monthly_orders_df = pd.melt(
        filtered_df,
        id_vars='cuisines',
        value_vars=['swiggy_estimated_monthly_orders','zomato_estimated_monthly_orders'],
        var_name='platform',
        value_name='monthly_orders'
    )
    monthly_orders_df['platform'] = monthly_orders_df['platform'].replace({
        'swiggy_estimated_monthly_orders': 'swiggy',
        'zomato_estimated_monthly_orders': 'zomato'
    })
    monthly_orders = monthly_orders_df.groupby(['cuisines','platform'])['monthly_orders'].median().reset_index()

    fig = px.bar(
        monthly_orders,
        x='cuisines',
        y='monthly_orders',
        color='platform',
        color_discrete_map={
        'Swiggy': "#ff7614",
        'Zomato': "#ff0f0f"
    },
        barmode='group'
    )

    col1, col2 = st.columns([3,1])
    with col1: 
        st.subheader("Estimated Monthly Orders")
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        st.subheader("Insights")
        st.write(
            '''
                • Zomato has the highest avg monthly order On Japanese Cuisine: 223\n
                • Swiggy has the highest avg monthly order On Japanese Cuisine: 222\n
                • Zomato has the lowest avg monthly order On Korean Cuisine: 170\n
                • Swiggy has the lowest avg monthly order On Korean Cuisine: 169
            '''
        )

    st.subheader("Overall Monthly Orders Comparison")
    html_code = open("orders.html", "r").read()
    st.components.v1.html(html_code, height=550)

elif options=="Estimated Monthly Orders Based On City":
    
    html_code = """
        <div class='tableauPlaceholder' id='vizContainer'></div>
        <script type='module'
        src='https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js'>
        </script>

        <tableau-viz
            id='tableauViz'
            src='https://public.tableau.com/views/Swiggy_zomato_monthly_orders/Sheet1?:showVizHome=no'
            width='100%'
            height='900'
            toolbar='bottom'
            hide-tabs>
        </tableau-viz>
        """
    components.html(html_code, height=900)


elif options=="Estimated Net Profit Based On City":
    html_code = """
        <script type="module"
        src="https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js">
        </script>

        <tableau-viz
            id="tableauViz"
            src="https://public.tableau.com/views/Swiggy_zomato_net_profit/Sheet2?:showVizHome=no"
            width="100%"
            height="900"
            toolbar="bottom"
            hide-tabs>
        </tableau-viz>
        """ 
    components.html(html_code, height=900)

    st.subheader("Total Estimated profit Comparison")
    html_code = open("profit.html", "r").read()
    st.components.v1.html(html_code, height=800)
