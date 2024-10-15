import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt

# Load CSS for custom styling
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f4f7;
    }
    h1 {
        color: #2C3E50;
        font-size: 36px;
        text-align: center;
    }
    h2 {
        color: #2980B9;
    }
    .header {
        text-align: center;
        margin: 20px 0;
    }
    .container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True
)

# Title of the app
st.title("Luxury Hotel Data Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Analysis"])

if page == "Home":
    st.markdown("<div class='header'><h1>Explore the World’s Best 50 Hotels</h1></div>", unsafe_allow_html=True)
    st.info("Upload a CSV file containing hotel data to begin analysis.")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        
        # Show the first few rows of the dataset
        st.subheader("Dataset Overview")
        st.write(df.head())
        st.write(f"Dataset contains **{df.shape[0]}** rows and **{df.shape[1]}** columns.")

else:
    st.subheader("Data Analysis")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        
        # Display column names for debugging
        st.write("Column Names in the DataFrame:")
        st.write(df.columns.tolist())

        # Data summary and analysis
        st.write("Summary Statistics:")
        st.write(df.describe())

        # Distribution of Starting Rates
        st.subheader("Distribution of Starting Rates of Hotels")
        fig = px.histogram(df, x='Starting Rate in ($)', nbins=15, title='Distribution of Starting Rates', 
                           labels={'Starting Rate in ($)': 'Starting Rate in ($)'})
        st.plotly_chart(fig)

        # Average Starting Rates by Location
        st.subheader("Average Starting Rates by Location")
        location_rates = df.groupby('Location')['Starting Rate in ($)'].mean().reset_index()
        fig = px.bar(location_rates, x='Location', y='Starting Rate in ($)', title='Average Starting Rates by Location')
        st.plotly_chart(fig)

        # Filter Options
        st.subheader("Filter Data")
        min_rate, max_rate = st.slider("Select the range of Starting Rates", 
                                        min_value=int(df['Starting Rate in ($)'].min()), 
                                        max_value=int(df['Starting Rate in ($)'].max()), 
                                        value=(int(df['Starting Rate in ($)'].min()), int(df['Starting Rate in ($)'].max())))

        min_rooms, max_rooms = st.slider("Select the range of Total Rooms", 
                                          min_value=int(df['Total Rooms'].min()), 
                                          max_value=int(df['Total Rooms'].max()), 
                                          value=(int(df['Total Rooms'].min()), int(df['Total Rooms'].max())))

        filtered_data = df[(df['Starting Rate in ($)'].between(min_rate, max_rate)) & 
                           (df['Total Rooms'].between(min_rooms, max_rooms))]

        st.write(f"Filtered dataset contains **{filtered_data.shape[0]}** rows.")
        st.dataframe(filtered_data)

        # Most Expensive and Least Expensive Hotels
        st.subheader("Most and Least Expensive Hotels")

        # Checking if expected columns exist
        required_columns = ['Name', 'Location', 'Starting Rate in ($)', 'Total Rooms']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"The following columns are missing from the dataset: {', '.join(missing_columns)}")
        else:
            most_expensive = df.loc[df['Starting Rate in ($)'].idxmax()]
            least_expensive = df.loc[df['Starting Rate in ($)'].idxmin()]
            
            st.write("Most Expensive Hotel:")
            st.write(most_expensive[['Name', 'Location', 'Starting Rate in ($)', 'Total Rooms']])
            
            st.write("Least Expensive Hotel:")
            st.write(least_expensive[['Name', 'Location', 'Starting Rate in ($)', 'Total Rooms']])

        # Amenity Selection
        st.subheader("Filter by Amenities")
        
        # Handling NaN values in the amenities column
        df['Hotel Ammenties'] = df['Hotel Ammenties'].fillna('')

        amenities = df['Hotel Ammenties'].str.split(',').explode().str.strip().unique()
        selected_amenities = st.multiselect("Select amenities to filter", options=amenities)

        if selected_amenities:
            # Create a boolean mask for filtering
            amenities_mask = df['Hotel Ammenties'].str.contains('|'.join(selected_amenities), case=False)
            filtered_amenities = df[amenities_mask]

            st.write(f"Filtered by amenities dataset contains **{filtered_amenities.shape[0]}** rows.")
            st.dataframe(filtered_amenities)
        
        

        # Correlation Heatmap
        st.subheader("Correlation Heatmap")
        numeric_df = df.select_dtypes(include=['int64', 'float64'])
        correlation_matrix = numeric_df.corr()
        fig = plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
        st.pyplot(fig)

        # Distribution of Starting Rates
        st.subheader("Distribution of Starting Rates of Hotels")
        plt.figure(figsize=(10, 6))
        sns.histplot(df['Starting Rate in ($)'], kde=True, color='lavender', bins=15)
        plt.title('Distribution of Starting Rates of Hotels', fontsize=16)
        plt.xlabel('Starting Rate in ($)', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        st.pyplot(plt)

        # Total Rooms vs. Starting Rates of Hotels
        st.subheader("Total Rooms vs. Starting Rates of Hotels")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='Total Rooms', y='Starting Rate in ($)', hue='Location', palette='viridis', s=100)
        plt.title('Total Rooms vs. Starting Rates of Hotels', fontsize=16)
        plt.xlabel('Total Rooms', fontsize=12)
        plt.ylabel('Starting Rate in ($)', fontsize=12)
        plt.legend(loc='upper right', title='Location')
        plt.tight_layout()
        st.pyplot(plt)

        # Top 5 Dining Areas by Max Starting Rate
        st.subheader("Top 5 Dining Areas by Max Starting Rate")
        top_dining_areas = df.groupby('Dining Area')['Starting Rate in ($)'].max().sort_values(ascending=False).head(5)
        plt.figure(figsize=(10, 6))
        sns.barplot(x=top_dining_areas.values, y=top_dining_areas.index, palette='coolwarm')
        plt.title('Top 5 Dining Areas by Max Starting Rate', fontsize=16)
        plt.xlabel('Max Starting Rate in ($)', fontsize=12)
        plt.ylabel('Dining Area', fontsize=12)
        plt.tight_layout()
        st.pyplot(plt)

        # Starting Rates by Amenities (Swimming Pool and Spa)
        st.subheader("Starting Rates by Amenities (Swimming Pool and Spa)")
        df['Has Swimming Pool'] = df['Hotel Ammenties'].str.contains('Swimming pool', case=False, na=False)
        df['Has Spa'] = df['Hotel Ammenties'].str.contains('spa/wellness centre', case=False, na=False)

        amenity_melted = df.melt(id_vars=['Starting Rate in ($)'], value_vars=['Has Swimming Pool', 'Has Spa'],
                              var_name='Amenity', value_name='Available')

        plt.figure(figsize=(12, 6))
        sns.boxplot(x='Amenity', y='Starting Rate in ($)', hue='Available', data=amenity_melted, palette='Set2')
        plt.title('Starting Rates by Amenities (Swimming Pool and Spa)', fontsize=16)
        plt.xlabel('Amenity', fontsize=12)
        plt.ylabel('Starting Rate in ($)', fontsize=12)
        plt.legend(title='Availability')
        plt.tight_layout()
        st.pyplot(plt)

        # Top 5 Hotel Amenities Distribution
        st.subheader("Top 5 Hotel Amenities Distribution")
        amenity_distribution = df['Hotel Ammenties'].str.split(',').explode().str.strip().value_counts()
        top_amenities = amenity_distribution.head(5)

        plt.figure(figsize=(8, 8))
        plt.pie(top_amenities, labels=top_amenities.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
        plt.title('Top 5 Hotel Amenities Distribution', fontsize=16)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(plt)

        # Export Filtered Results
        st.subheader("Export Filtered Results")
        if st.button("Download Filtered Data as CSV"):
            filtered_data.to_csv('filtered_data.csv', index=False)
            st.success("Filtered data has been saved as 'filtered_data.csv'.")
    else:
        st.warning("Please upload a CSV file to start the analysis.")
