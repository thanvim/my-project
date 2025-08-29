import streamlit as st
import google.generativeai as genai
import base64
from PIL import Image
import os
import datetime
import time
import threading
import base64


# Set up API Key
API_KEY = "AIzaSyD5i8wRYKgSBZ2MYgpsXYVP8bwRNuSN3Ec"  # Replace with your API Key
genai.configure(api_key=API_KEY)

# Define model
MODEL_NAME = "gemini-1.5-pro"

# Function to generate meal plan
def generate_meal_plan(dietary_preference):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
       
        prompt = f"""
        Create a detailed 7-day meal plan for a {dietary_preference} diet.
        Each day should include:
        - Breakfast, Lunch, and Dinner
        - The meal name
        - Ingredients listed on separate lines
        - Estimated nutritional values (**Calories**, **Protein**, **Carbs**, **Fats** in separate lines and highlighted).
        """
       
        response = model.generate_content(prompt)
        return response.text if response.text else "Failed to generate meal plan."
    except Exception as e:
        return f"Error: {str(e)}"


# Function to get nutrition advice from AI Chat Assistant
def get_nutrition_advice(user_input):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(user_input)
        return response.text if response.text else "Sorry, I couldn't process your question."
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI Styling
st.set_page_config(page_title="AI Meal Planner", page_icon="🍽️", layout="wide")

st.markdown(
    """
    <style>
    .custom-header {
        font-size: 48px;
        font-weight: bold;
        background: rgb(2,0,36);
        background: linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 35%, rgba(0,212,255,1) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    <div class="custom-header">
        Nutriscience 
    </div>
    """,
    unsafe_allow_html=True
)

# Apply custom CSS for white text
st.markdown(
    """
    <style>
    .stApp {
        background: url(data:image/jpeg;base64,{encoded_background_image}) no-repeat center center fixed;
        background-size: cover;
    }
    .stMarkdown, .stTextInput, .stHeader, .stSubheader, .stCaption {
        color: Black;
    }
    .stButton>button {
        color: black !important;
        background-color: #f0f0f0 !important;
        border-radius: 10px;
        padding: 10px;
        font-weight: bold;
    }
    .custom-subheader {
        color: yellow !important;
        font-weight: bold;
        font-size: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Title and Description
st.title("🍽️ AI-Powered Meal Planner")
st.markdown("**Get a personalized 7-day meal plan with nutrient details!**")

# Sidebar for user input
with st.sidebar:
    st.header("⚙️ Dietary Preferences")
    diet_type = st.selectbox("Choose your diet type:", ["Balanced", "Vegetarian", "Vegan", "Keto", "High Protein", "Paleo", "Mediterranean", "Low Carb"])
   
    st.header("📋 Meal Plan Details")
    st.markdown("""
    - The plan includes 3 meals per day (Breakfast, Lunch, Dinner).  
    - Ingredients will be listed on separate lines.
    - Nutritional details: **Calories**, **Protein**, **Carbs**, and **Fats** in separate lines and highlighted.  
    - Customize your diet preference from the options above.
    """)
 
# Main Content for Meal Plan Generation
st.markdown("""
👋 Welcome to the AI-powered meal planner! Click the button below to generate your custom 7-day meal plan.
""")

generate_btn = st.button("🚀 Generate Meal Plan")

if generate_btn:
    with st.spinner("🔄 Generating meal plan..."):
        meal_plan = generate_meal_plan(diet_type)
       
        # Display result
        st.markdown("### 📜 Your 7-Day Meal Plan")
        st.markdown("**Click each day to expand and view details.**")
       
        # Splitting into days
        meal_lines = meal_plan.split('\n')
        day_meals = {}
        current_day = None
       
        for line in meal_lines:
            if "Day" in line:
                current_day = line.strip()
                day_meals[current_day] = []
            elif current_day:
                if "Calories:" in line:
                    line = line.replace("Calories:", "<span class='highlight'>Calories:</span>")
                if "Protein:" in line:
                    line = line.replace("Protein:", "<span class='highlight'>Protein:</span>")
                if "Carbs:" in line:
                    line = line.replace("Carbs:", "<span class='highlight'>Carbs:</span>")
                if "Fats:" in line:
                    line = line.replace("Fats:", "<span class='highlight'>Fats:</span>")
                day_meals[current_day].append(line)
       
        for day, meals in day_meals.items():
            with st.expander(day):
                st.markdown("\n".join(meals), unsafe_allow_html=True)
        # Download Button
        st.download_button(label="📥 Download Meal Plan", data=meal_plan, file_name="meal_plan.txt", mime="text/plain")

# Setting the default background image

def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()
background_image_path = "BackgroundAI.jpg"  # Ensure the image exists in the same directory
encoded_background_image = get_base64_image(background_image_path)

# AI Chat Assistant for Nutrition Advice
st.markdown("---")
st.header("🤖 AI Chat Assistant for Nutrition Advice")

with st.container():
    st.markdown("**Ask me anything about nutrition, diet plans, or healthy eating!**")

    user_question = st.text_input("💬 Enter your nutrition-related question:")
    
    if st.button("💡 Get Advice"):
        if user_question.strip():
            with st.spinner("🤖 Thinking..."):
                advice = get_nutrition_advice(user_question)
                st.markdown(f"**🔹 AI :** {advice}")
        else:
            st.warning("⚠️ Please enter a question before clicking the button.")


if "background_applied" not in st.session_state:
    st.session_state["background_applied"] = True
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpeg;base64,{encoded_background_image}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("data:image/jpeg;base64,{encoded_background_image}") no-repeat center center fixed !important;
        background-size: cover !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)



