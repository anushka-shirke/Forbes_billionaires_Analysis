import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

st.title("Forbes Billionaires Data Analysis")

uploaded_file = st.file_uploader("Upload the Forbes 2022 Billionaires CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data")
    st.dataframe(df.head())

    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    # Clean net worth column
    df['networth'] = df['networth'].replace('[$B]', '', regex=True).astype('float64')

    # Show basic stats
    st.subheader("Net Worth Statistics")
    st.write("Mean Net Worth: $", np.mean(df['networth']))
    st.write("Median Net Worth: $", np.median(df['networth']))
    st.write(df['networth'].describe())

    # Histogram
    st.subheader("Net Worth Distribution")
    fig1, ax1 = plt.subplots()
    sb.histplot(df['networth'], bins=10, ax=ax1)
    st.pyplot(fig1)

    # Boxplot
    fig2, ax2 = plt.subplots()
    sb.boxplot(x=df['networth'], ax=ax2)
    st.pyplot(fig2)

    # Top 10 Billionaires
    st.subheader("Top 10 Billionaires by Net Worth")
    top_billionaires = df.groupby('name')['networth'].sum().nlargest(10)
    st.bar_chart(top_billionaires)

    # Top 10 Countries by Count
    st.subheader("Top 10 Countries by Number of Billionaires")
    top_countries = df['country'].value_counts().head(10)
    st.bar_chart(top_countries)

    # Country-wise Net Worth
    st.subheader("Country-wise Net Worth (All Countries)")
    fig3, ax3 = plt.subplots()
    sb.barplot(x='country', y='networth', data=df, ax=ax3)
    plt.xticks(rotation=90)
    st.pyplot(fig3)

    # Average Net Worth by Industry
    st.subheader("Average Net Worth by Industry")
    avg_networth_industry = df.groupby('industry')['networth'].mean()
    fig4, ax4 = plt.subplots()
    sb.barplot(x=avg_networth_industry.index, y=avg_networth_industry.values, ax=ax4)
    plt.xticks(rotation=90)
    st.pyplot(fig4)

    # Age Analysis
    st.subheader("Age Analysis")
    st.write("Mean Age: ", np.mean(df['age']))
    st.write("Median Age: ", np.median(df['age']))
    oldest = df.groupby('name')[['networth', 'age']].sum().nlargest(1, 'age')
    st.write("Oldest Billionaire:")
    st.dataframe(oldest)

else:
    st.info("Please upload a CSV file to begin analysis.")
