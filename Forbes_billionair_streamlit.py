import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Forbes Billionaires 2022 Data Analysis")

uploaded_file = st.file_uploader("📁 Upload the Forbes 2022 Billionaires CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📌 Raw Data")
    st.dataframe(df.head())

    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    # Clean net worth column
    df['networth'] = df['networth'].replace('[$B]', '', regex=True).astype('float64')

    # === Net Worth Stats ===
    st.subheader("💰 Net Worth Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mean Net Worth", f"${np.mean(df['networth']):.2f}B")
    with col2:
        st.metric("Median Net Worth", f"${np.median(df['networth']):.2f}B")
    with col3:
        st.metric("Max Net Worth", f"${df['networth'].max():.2f}B")

    st.write("Summary statistics:")
    st.write(df['networth'].describe())

    # === Net Worth Distribution ===
    st.subheader("📈 Net Worth Distribution")
    fig1, ax1 = plt.subplots()
    sb.histplot(df['networth'], bins=10, kde=True, ax=ax1)
    ax1.set_xlabel("Net Worth ($B)")
    st.pyplot(fig1)

    # === Boxplot ===
    st.subheader("📦 Net Worth Boxplot")
    fig2, ax2 = plt.subplots()
    sb.boxplot(x=df['networth'], ax=ax2)
    st.pyplot(fig2)

    # === Top 10 Billionaires ===
    st.subheader("👑 Top 10 Billionaires by Net Worth")
    top_billionaires = df.groupby('name')['networth'].sum().nlargest(10).reset_index()
    st.dataframe(top_billionaires)
    st.bar_chart(data=top_billionaires.set_index('name'))

    # === Top 10 Countries by Number of Billionaires ===
    st.subheader("🌍 Top 10 Countries by Number of Billionaires")
    top_countries = df['country'].value_counts().head(10).reset_index()
    top_countries.columns = ['country', 'count']
    st.dataframe(top_countries)
    st.bar_chart(data=top_countries.set_index('country'))

    # === Country-wise Net Worth (Top 10) ===
    st.subheader("🌎 Top 10 Countries by Total Net Worth")
    top_countries_networth = df.groupby('country')['networth'].sum().nlargest(10).reset_index()
    fig3, ax3 = plt.subplots()
    sb.barplot(x='networth', y='country', data=top_countries_networth, ax=ax3)
    ax3.set_xlabel("Total Net Worth ($B)")
    ax3.set_ylabel("Country")
    st.pyplot(fig3)

    # === Average Net Worth by Industry (Top 10) ===
    st.subheader("🏭 Average Net Worth by Industry (Top 10)")
    avg_networth_industry = df.groupby('industry')['networth'].mean().sort_values(ascending=False).head(10).reset_index()
    fig4, ax4 = plt.subplots()
    sb.barplot(x='networth', y='industry', data=avg_networth_industry, ax=ax4)
    ax4.set_xlabel("Average Net Worth ($B)")
    ax4.set_ylabel("Industry")
    st.pyplot(fig4)

    # === Age Statistics ===
    st.subheader("👴 Age Analysis")
    col4, col5 = st.columns(2)
    with col4:
        st.metric("Mean Age", f"{np.mean(df['age']):.1f} years")
    with col5:
        st.metric("Median Age", f"{np.median(df['age']):.1f} years")

    oldest = df[['name', 'age', 'networth']].sort_values(by='age', ascending=False).head(1)
    st.write("Oldest Billionaire:")
    st.dataframe(oldest)

else:
    st.info("📤 Please upload a CSV file to begin the analysis.")
