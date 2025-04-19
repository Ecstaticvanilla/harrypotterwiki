import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["gemini_apikey"])
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def generate_meal_plan(gender, age, weight, height, activity_level, tdee, selected_meals):
    meal_list = ', '.join(selected_meals)
    prompt = f"""
You are a professional nutritionist AI.
Generate a healthy meal plan for:
- Gender: {gender}
- Age: {age} years
- Weight: {weight} kg
- Height: {height} cm
- Activity Level: {activity_level}
- Total Daily Energy Expenditure (TDEE): {tdee:.0f} kcal

Include the following meals only: {meal_list}
For each meal:
• Provide a complete menu  
• Estimate calories (total ≈ TDEE split appropriately)  
• Suggest water intake  
• Ensure balanced macronutrients

Respond in a clean, easy-to-read tabular format.
"""
    resp = model.generate_content(prompt)
    return resp.text
