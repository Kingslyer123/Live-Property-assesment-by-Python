import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re  # For text processing

# Custom CSS for Styling
st.markdown("""
    <style>
    body {
        background-color: #333333; /* Gray Background */
        color: #FFFFFF; /* White Text */
    }
    .stApp {
        background-color: #333333; /* Gray Background */
        color: #FFFFFF; /* White Text */
    }
    .css-1d391kg { /* Sidebar background */
        background-color: #000000 !important; /* Black Sidebar Background */
    }
    .css-q8sbsg { /* Sidebar Menu Text */
        color: #000000 !important; /* Black Text */
        font-weight: bold !important;
        font-size: 16px !important; /* Adjust font size */
        padding: 10px; /* Add padding for better spacing */
        border-radius: 5px; /* Rounded corners */
        margin-bottom: 5px; /* Add spacing between menu items */
        background-color: #000000 !important; /* Black Background */
    }
    .css-q8sbsg:hover { /* Hover Effect for Sidebar Menu */
        background-color: #444444 !important; /* Dark Gray Background on Hover */
        color: #FFD700 !important; /* Gold Text on Hover */
        transition: background-color 0.3s ease; /* Smooth hover transition */
    }
    .css-1m8utma, .css-1a32fsj, .css-1m8utma:hover { /* Inputs Styling */
        background-color: #444444 !important; /* Dark Gray Inputs */
        color: #FFFFFF !important; /* White Input Text */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important; /* White for all Headings */
    }
    .stButton button {
        background-color: #555555 !important; /* Button Background */
        color: #FFFFFF !important; /* Button Text */
        border-radius: 5px;
    }
    .css-1d391kg .stSidebarHeader {
        background-color: #000000 !important; /* Black Background for Upload Your Data */
        color: #000000 !important; /* Black Text */
    }
    </style>
""", unsafe_allow_html=True)

# Function to handle non-numeric areas like "2 Kanal"
def convert_area_to_sqft(area):
    """Converts area to square feet if possible."""
    try:
        area = str(area).lower().strip()
        if "kanal" in area:  # Convert Kanal to square feet (1 Kanal = 4500 sq ft)
            return float(re.search(r"\d+", area).group()) * 4500
        elif "marla" in area:  # Convert Marla to square feet (1 Marla = 272 sq ft)
            return float(re.search(r"\d+", area).group()) * 272
        else:
            # Default fallback if area is numeric
            return float(area)
    except Exception:
        return None  # Return None for invalid area entries

# Sidebar Navigation Menu
menu = ["Home", "Search Properties", "City-wise Distribution", "Price Prediction", "Contact Us"]
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", menu)

# Title
st.title("Property Search Engine Dashboard")

# File Upload Section
st.sidebar.subheader("Upload your data")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type="csv")

if uploaded_file:
    try:
        # Read the CSV file
        data = pd.read_csv(uploaded_file)

        # Preprocess 'area' column for compatibility
        if "area" in data.columns:
            data["area"] = data["area"].apply(convert_area_to_sqft)

        # Preprocess 'price' column to ensure numeric values
        data["price"] = pd.to_numeric(data["price"], errors="coerce")

        # Drop rows with invalid or missing data
        data = data.dropna(subset=["price", "area"])

        # Check for necessary columns
        if "city" not in data.columns or "price" not in data.columns:
            st.error("The dataset must have 'city' and 'price' columns.")
        else:
            if selection == "Home":
                st.header("Welcome!")
                st.write("Upload your property data to analyze, visualize, and even predict property prices. Use the sidebar to navigate.")

                with st.expander("Group Members"):
                    st.write("M. Asim Ali")
                    st.write("Hamza Amjad")
                    st.write("Saim Saqib")
                    st.write("Ayesha Shafique")

            elif selection == "Search Properties":
                st.header("Search Properties")
                st.dataframe(data)

                city_input = st.text_input("Enter City", "")
                min_price = st.number_input("Minimum Price", value=0, min_value=0)
                max_price = st.number_input("Maximum Price", value=int(data["price"].max()), min_value=0)

                # Filter data by criteria
                filtered_data = data[
                    (data["city"].str.contains(city_input, case=False, na=False)) &
                    (data["price"] >= min_price) &
                    (data["price"] <= max_price)
                ]

                st.subheader("Search Results")
                st.dataframe(filtered_data)

                if not filtered_data.empty:
                    st.subheader("Data Summary")
                    st.write(filtered_data.describe())
                else:
                    st.warning("No results found for the given search criteria.")

            elif selection == "City-wise Distribution":
                st.header("City-wise Property Distribution")
                city_group = data.groupby("city").agg(total_properties=("city", "count")).reset_index()
                st.bar_chart(city_group.set_index("city"))

                # Pie chart for proportion
                fig, ax = plt.subplots()
                ax.pie(city_group["total_properties"], labels=city_group["city"], autopct="%1.1f%%", startangle=90)
                ax.set_title("City-Wise Property Distribution")
                st.pyplot(fig)

            elif selection == "Price Prediction":
                st.header("Predict Property Price")
                st.write("This feature calculates the property price using the formula: **Price = Area × 900**.")

                st.subheader("Enter Property Features")
                area = st.number_input("Area (in square feet):", min_value=0.0, step=50.0)

                if st.button("Predict Price"):
                    if area > 0:
                        prediction = area * 900  # New price formula
                        st.success(f"The predicted price for a property with area {area} sqft is PKR {prediction:,.2f}")
                    else:
                        st.warning("Please enter a valid value for area.")

            elif selection == "Contact Us":
                st.header("Contact Us")
                st.write("For inquiries, email us at: asimalipoiuy@gmail.com")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.write("Upload a dataset to get started.")
