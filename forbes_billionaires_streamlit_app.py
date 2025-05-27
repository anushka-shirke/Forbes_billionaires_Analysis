
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

CHART_SIZE = (4, 2.5)

st.set_page_config(layout="wide")
st.title("📊 Forbes Billionaires 2022 Data Analysis")

uploaded_file = st.file_uploader("📁 Upload the Forbes 2022 Billionaires CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📌 Raw Data")
    st.dataframe(df.head())

    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    df['networth'] = df['networth'].replace('[$B]', '', regex=True).astype('float64')

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

    st.subheader("📈 Net Worth Distribution")
    fig1, ax1 = plt.subplots(figsize=CHART_SIZE, dpi=100)
    sb.histplot(df['networth'], bins=10, kde=True, ax=ax1)
    ax1.set_xlabel("Net Worth ($B)")
    fig1.tight_layout()
    st.pyplot(fig1)

    st.subheader("📦 Net Worth Boxplot")
    fig2, ax2 = plt.subplots(figsize=CHART_SIZE, dpi=100)
    sb.boxplot(x=df['networth'], ax=ax2)
    fig2.tight_layout()
    st.pyplot(fig2)

    st.subheader("👑 Top 10 Billionaires by Net Worth")
    top_billionaires = df.groupby('name')['networth'].sum().nlargest(10).reset_index()
    st.dataframe(top_billionaires)
    st.bar_chart(data=top_billionaires.set_index('name'))

    st.subheader("🌍 Top 10 Countries by Number of Billionaires")
    top_countries = df['country'].value_counts().head(10).reset_index()
    top_countries.columns = ['country', 'count']
    st.dataframe(top_countries)
    st.bar_chart(data=top_countries.set_index('country'))

    st.subheader("🌎 Top 10 Countries by Total Net Worth")
    top_countries_networth = df.groupby('country')['networth'].sum().nlargest(10).reset_index()
    fig3, ax3 = plt.subplots(figsize=CHART_SIZE, dpi=100)
    sb.barplot(x='networth', y='country', data=top_countries_networth, ax=ax3)
    ax3.set_xlabel("Total Net Worth ($B)")
    ax3.set_ylabel("Country")
    fig3.tight_layout()
    st.pyplot(fig3)

    st.subheader("🏭 Average Net Worth by Industry (Top 10)")
    avg_networth_industry = df.groupby('industry')['networth'].mean().sort_values(ascending=False).head(10).reset_index()
    fig4, ax4 = plt.subplots(figsize=CHART_SIZE, dpi=100)
    sb.barplot(x='networth', y='industry', data=avg_networth_industry, ax=ax4)
    ax4.set_xlabel("Average Net Worth ($B)")
    ax4.set_ylabel("Industry")
    fig4.tight_layout()
    st.pyplot(fig4)

    st.subheader("👴 Age Analysis")
    col4, col5 = st.columns(2)
    with col4:
        st.metric("Mean Age", f"{np.mean(df['age']):.1f} years")
    with col5:
        st.metric("Median Age", f"{np.median(df['age']):.1f} years")

    col6, col7 = st.columns(2)
    with col6:
        oldest = df[['name', 'age', 'networth']].sort_values(by='age', ascending=False).head(1)
        st.write("🧓 Oldest Billionaire:")
        st.dataframe(oldest)

    with col7:
        youngest = df[['name', 'age', 'networth']].sort_values(by='age', ascending=True).head(1)
        st.write("🧒 Youngest Billionaire:")
        st.dataframe(youngest)

    st.subheader("🔎 Filter Data by Country and Industry")
    selected_countries = st.multiselect("Select Countries", options=sorted(df['country'].dropna().unique()), default=[])
    selected_industries = st.multiselect("Select Industries", options=sorted(df['industry'].dropna().unique()), default=[])
    metric = st.radio("Choose Metric to Analyze:", ["Age", "Net Worth"])

    filtered_df = df.copy()
    if selected_countries:
        filtered_df = filtered_df[filtered_df['country'].isin(selected_countries)]
    if selected_industries:
        filtered_df = filtered_df[filtered_df['industry'].isin(selected_industries)]

    st.subheader(f"📊 {metric} Distribution (Filtered)")

    if metric == "Age":
        fig_hist, ax = plt.subplots(figsize=CHART_SIZE, dpi=100)
        sb.histplot(filtered_df['age'].dropna(), bins=20, kde=True, color='skyblue', ax=ax)
        ax.set_xlabel("Age")
        ax.set_title("Age Distribution")
        fig_hist.tight_layout()
        st.pyplot(fig_hist)

        fig_box, ax2 = plt.subplots(figsize=CHART_SIZE, dpi=100)
        sb.boxplot(x=filtered_df['age'].dropna(), color='lightgreen', ax=ax2)
        ax2.set_title("Age Boxplot")
        fig_box.tight_layout()
        st.pyplot(fig_box)

    elif metric == "Net Worth":
        fig_hist, ax = plt.subplots(figsize=CHART_SIZE, dpi=100)
        sb.histplot(filtered_df['networth'].dropna(), bins=20, kde=True, color='orange', ax=ax)
        ax.set_xlabel("Net Worth ($B)")
        ax.set_title("Net Worth Distribution")
        fig_hist.tight_layout()
        st.pyplot(fig_hist)

        fig_box, ax2 = plt.subplots(figsize=CHART_SIZE, dpi=100)
        sb.boxplot(x=filtered_df['networth'].dropna(), color='gold', ax=ax2)
        ax2.set_title("Net Worth Boxplot")
        fig_box.tight_layout()
        st.pyplot(fig_box)

    st.subheader("🧾 Filtered Data Preview")
    st.dataframe(filtered_df)

    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(filtered_df)

    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_billionaires.csv',
        mime='text/csv'
    )
