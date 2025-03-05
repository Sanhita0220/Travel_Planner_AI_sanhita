import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pandas as pd
import plotly.express as px
from langchain.prompts import PromptTemplate
from chatbot import chatbot_ui

# Set Page Config with Background
st.set_page_config(page_title="AI Travel Planner", layout="wide")



# ✅ Banner Image with Title Overlay
st.markdown(
    """
    <style>
        .banner-container {
            position: relative;
            text-align: center;
            margin-bottom: 20px;
            background-color: rgba(66, 94, 80, 1);
            
        }
        .banner-img {
            width: 90%;
            max-height: 200px;
            object-fit: cover;
            border-radius: 15px;
        }
        .banner-title {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 60px; /* font size */
            font-weight: bold;
            color: white;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
        }
        .banner-subtitle {
            position: absolute;
            top: 85%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 20px; /* font size */
            font-weight: bold;
            color: white;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
        }
        
    </style>
    <div class="banner-container">
        <img class="banner-img" src="https://thumbs.dreamstime.com/b/travel-13094661.jpg">
        <div class="banner-title">Travel Planner</div>
        <div class="banner-subtitle">Plan your trips effortlessly with AI-powered cost estimation and itinerary generation.</div>
    </div>

    """,
    unsafe_allow_html=True
)


# ✅ Centered Title
#st.markdown("<h1 style='text-align: center;'>Travel Planner</h1>", unsafe_allow_html=True)

# Function to validate API Key
def validate_api_key(api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content("Test message")
        return response is not None
    except Exception:
        return False


# Function to generate AI-based travel cost estimation
def get_ai_travel_cost(source, destination, budget, currency, travelers, adults, children, transport_mode, food_included, travel_date):
    prompt_template = PromptTemplate(
        input_variables=["source", "destination", "budget", "currency", "travelers", "transport_mode", "food_included", "travel_date"],
        template="""
        You are a detailed AI travel assistant. Provide a breakdown of travel costs from {source} to {destination} on {travel_date}.
        Consider {travelers} travelers and suggest the most optimal transport mode if {transport_mode} is 'Any'.
        Include costs for flights, trains, and local transport. Factor in visa fees if applicable.
        Break down the budget into transportation, accommodation, food, and miscellaneous expenses.
        Adjust prices for weekends and peak seasons. Provide cost-saving tips.
        Return the estimate in {currency}.
        """
    )
    prompt = prompt_template.format(
        source=source,
        destination=destination,
        budget=budget if budget > 0 else "not specified",
        currency=currency,
        travelers=travelers,
        transport_mode=transport_mode,
        food_included=food_included,
        travel_date=travel_date
    )
    
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text if response else "Error generating cost estimation."

# Function to generate AI-based itinerary
def generate_itinerary(source, destination, travel_date, travelers, adults, children):
    prompt = f"""
    You are an expert travel planner. Generate a structured itinerary for a trip from {source} to {destination} on {travel_date}.
    The trip includes {travelers} both {adults} and {children} travelers. Provide:
    - Must-visit tourist attractions, hidden gems, and local experiences.
    - Accommodation suggestions (budget, mid-range, luxury).
    - Transport recommendations, including local transit options.
    - Best restaurants to try local cuisine.
    - Hourly breakdown for activities, considering travel time.
    - Cost-saving travel tips and best visiting hours for attractions.
    """
    
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text if response else "Error generating itinerary."

# Sidebar for API Key
st.sidebar.header("🔑 API Key Setup")
st.sidebar.markdown('<div class="main-container">', unsafe_allow_html=True)
api_key = st.sidebar.text_input("Enter your Google API Key:", type="password")

if api_key and validate_api_key(api_key):
    st.sidebar.success("API Key Validated ✅")
else:
    st.sidebar.warning("Enter a valid Google API Key to continue!")
    st.stop()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
        .stColumn {
            background-color: rgba(66, 94, 80, 1); /* green background #425E50*/
            padding: 20px;
            border-radius: 10px;
        }
    </style>
    <div class="container">
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([2, 2, 2], gap="large")

st.markdown(
    """
    <style>
        /* Style for all input labels */
        label {
            color: white !important;  /* White Label Text */
            font-weight: bold;  /* Make text bold */
            font-size: 25px;  /* Adjust font size */
        }

        /* Style for input fields */
        div.stTextInput > div > div > select {
            border: 2px solid white !important;  /* White Border */
            color: #425E50 !important;  /* White Text */
            background-color: transparent !important; /* Transparent Background */
            border-radius: 8px; /* Rounded Borders */
            padding: 8px;
            border-line-color: #425E50; /* White Border Line */
            selection-color: #425E50; /* White Selection Color */
        },
        div.stNumberInput > div > div > select {
            border: 2px solid white !important;  /* White Border */
            color: #425E50 !important;  /* White Text */
            background-color: transparent !important; /* Transparent Background */
            border-radius: 8px; /* Rounded Borders */
            padding: 8px;
            border-line-color: #425E50; /* White Border Line */
            selection-color: #425E50; /* White Selection Color */
        },
        div.stSelectbox > div > div > select {
            border: 2px solid white !important;  /* White Border */
            color: #425E50 !important;  /* White Text */
            background-color: transparent !important; /* Transparent Background */
            border-radius: 8px; /* Rounded Borders */
            padding: 8px;
            border-line-color: #425E50; /* White Border Line */
            selection-color: #425E50; /* White Selection Color */
        }

        /* Style for checkbox */
        div.stCheckbox > label {
            color: white !important; /* White text */
            font-weight: bold;
            tick-color: #425E50; /* White tick */
        }

        /* Placeholder text color */
        div.stTextInput > div > div > input::placeholder,
        div.stNumberInput > div > div > input::placeholder {
            color: white !important; /* White Placeholder */
        }
        /* Tab Highlight & Bar Line */
        div[data-testid="stTabs"] div[role="tablist"] {
            border-bottom: 2px solid #FFFFFF !important; /* Change tab bar color */
            border-highlight: #425E50 !important; /* Change tab highlight color */
        }

        div[data-testid="stTabs"] div[role="tablist"] button[aria-selected="true"] {
            color: white !important; /* Active tab text color */
            background-color: #425E50 !important; /* Active tab background */
            border-radius: 10px 10px 0 0; /* Rounded edges */
        }

        /* Button Styling */
        div.stButton > button {
            color: #425E50 !important; /* Button Label */
            border: 2px solid #425E50 !important; /* Button Border */
            background-color: transparent !important; /* Transparent Background */
            padding: 8px 20px;
            border-radius: 8px;
            font-weight: bold;
            transition: 0.3s ease-in-out;
        }

        /* Button Hover Effect */
        div.stButton > button:hover {
            background-color: #425E50 !important; /* Change color on hover */
            color: white !important;
        }
    </style>
    
    """,
    unsafe_allow_html=True
)

with col1:
    source = st.text_input("🏠 Source:")
    travelers = st.number_input("👥 Travelers:", min_value=1, value=1)
    currency = st.selectbox("💰 Currency:", ["INR", "USD", "EUR", "GBP", "AUD", "CAD"], index=0)
    travel_date = st.date_input("📅 Travel Date:", min_value=datetime.today()).strftime('%Y-%m-%d')

with col2:
    destination = st.text_input("📍 Destination:")
    adults = st.number_input("🧑 Adults:", min_value=1, value=1)
    transport_mode = st.selectbox("🚆 Transport Mode:", ["Flight", "Train", "Bus", "Cab", "Any"], index=4)

with col3:
    budget = st.number_input("💵 Budget (Optional):", min_value=0, value=0)
    children = st.number_input("👶 Children:", min_value=0, value=0)
    food_included = st.checkbox("🍽️ Include Food? (+$200 per person per day)")

st.markdown("</div>", unsafe_allow_html=True)
 

chatbot_ui()

tab1, tab2 = st.tabs(["💰 Cost Estimation", "📍 Itinerary"])

with tab1:
    if st.button("Get Travel Cost Estimate 📊"):
        with st.spinner("Calculating cost..."):
            cost_estimate = get_ai_travel_cost(source, destination, budget, currency, travelers, adults, children, transport_mode, food_included, travel_date)
            st.subheader("📊 AI-Powered Travel Cost Estimates")
            st.write(cost_estimate)

with tab2:
    if st.button("Generate Itinerary 📌"):
        with st.spinner("Generating itinerary..."):
            itinerary = generate_itinerary(source, destination, travel_date, travelers, adults, children)
            st.subheader("📍 AI-Generated Itinerary:")
            st.write(itinerary)

st.markdown('</div>', unsafe_allow_html=True)

