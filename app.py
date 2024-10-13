import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the dataset
df = pd.read_csv(r'Imports_Exports_Dataset.csv')

# Sample for performance
df_sample = df.sample(n=3000, random_state=42)

# Sidebar filters
st.sidebar.title("Filters")

# Category Filter
categories = df_sample['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", options=categories, default=categories)

# Import/Export Filter
import_export_options = df_sample['Import_Export'].unique()
selected_import_export = st.sidebar.multiselect("Select Import/Export", options=import_export_options, default=import_export_options)

# Year filter (based on the Date column)
df_sample['Date'] = pd.to_datetime(df_sample['Date'], format='%d-%m-%Y')
df_sample['Year'] = df_sample['Date'].dt.year
years = df_sample['Year'].unique()
selected_years = st.sidebar.multiselect("Select Years", options=years, default=years)

# Filter the data based on selections
filtered_df = df_sample[
    (df_sample['Category'].isin(selected_categories)) & 
    (df_sample['Import_Export'].isin(selected_import_export)) & 
    (df_sample['Year'].isin(selected_years))
]

# Title
st.title("Imports and Exports Dashboard")

# Ensure data is not empty
if not filtered_df.empty:

    # First Row - Pie Chart and Box Plot
    col1, col2 = st.columns(2)

    with col1:
        # Pie chart for Import/Export breakdown
        transaction_counts = filtered_df['Import_Export'].value_counts()
        st.markdown('### Import vs Export Transactions')
        fig, ax = plt.subplots()
        ax.pie(transaction_counts, labels=transaction_counts.index, autopct='%1.1f%%', 
               colors=['#1f77b4', '#ff7f0e'])  # Matching colors
        ax.axis('equal')
        st.pyplot(fig)

    with col2:
        # Box Plot for Export/Import by Year
        st.markdown("### Export/Import Distribution by Year")
        plt.figure(figsize=(10,6))
        sns.boxplot(x='Year', y='Import_Export', data=filtered_df, palette=['#1f77b4', '#ff7f0e'])
        plt.title("Yearly Export/Import Box Plot")
        st.pyplot(plt)

    # Second Row - Histogram and Scatter Plot
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('### Histogram of Transaction Values')
        plt.figure(figsize=(10,6))
        plt.hist(filtered_df['Value'], bins=20, color='#1f77b4', edgecolor='black')
        plt.title('Distribution of Transaction Values')
        plt.xlabel('Transaction Value')
        plt.ylabel('Frequency')
        st.pyplot(plt)

    with col4:
        st.markdown('### Scatter Plot: Value vs Year')
        plt.figure(figsize=(10,6))
        sns.scatterplot(x='Year', y='Value', hue='Import_Export', data=filtered_df, palette=['#ff7f0e', '#1f77b4'])
        plt.title('Scatter Plot of Transaction Value by Year')
        st.pyplot(plt)

    # Third Row - Bar chart and Line chart
    col5, col6 = st.columns(2)

    with col5:
        st.markdown('### Transactions by Category')
        category_transaction_counts = filtered_df.groupby('Category')['Value'].sum().reset_index()
        fig = px.bar(category_transaction_counts, x='Category', y='Value', color='Category')
        st.plotly_chart(fig)

    with col6:
        st.markdown('### Average Monthly Transaction Value')
        filtered_df['Month'] = filtered_df['Date'].dt.month
        monthly_avg_value = filtered_df.groupby('Month')['Value'].mean().reset_index()
        fig = px.line(monthly_avg_value, x='Month', y='Value', markers=True)
        st.plotly_chart(fig)

else:
    st.warning("No data available for the selected filters. Please adjust your filters.")
