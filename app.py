import streamlit as st
import google.generativeai as genai
import json
import os

st.set_page_config(
    page_title="🍳 AI Recipe Generator",
    page_icon="🍳",
    layout="centered"
)

# -------------------------------
# Gemini API Configuration
# -------------------------------
genai.configure(api_key=st.secrets["AQ.Ab8RN6JB8DAJlTQPHrCBj6tUnXmmVVTnO5CeE5eZ1035vAMQZA"])

model = genai.GenerativeModel("gemini-2.5-flash")

SAVE_FILE = "saved_recipes.json"

# -------------------------------
# Load Saved Recipes
# -------------------------------
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        saved_recipes = json.load(f)
else:
    saved_recipes = []

# -------------------------------
# Session State
# -------------------------------
if "recipe" not in st.session_state:
    st.session_state.recipe = ""

# -------------------------------
# Recipe Generator
# -------------------------------
def generate_recipe(ingredients):

    prompt = f"""
You are an expert chef.

Create a delicious recipe using these ingredients:

{ingredients}

Return in the following format:

Recipe Name:

Preparation Time:

Cooking Time:

Ingredients:

Instructions:

Calories (Approx):

Chef Tips:
"""

    response = model.generate_content(prompt)

    return response.text

# -------------------------------
# Save Recipe
# -------------------------------
def save_recipe(recipe):

    saved_recipes.append(recipe)

    with open(SAVE_FILE, "w") as f:
        json.dump(saved_recipes, f, indent=4)

# -------------------------------
# UI
# -------------------------------

st.title("🍳 AI Recipe Generator")

st.write(
    "Generate delicious recipes instantly using Google's Gemini AI."
)

ingredients = st.text_input(
    "Enter Ingredients",
    placeholder="Potato, Cheese, Onion, Garlic..."
)

if st.button("Generate Recipe"):

    if ingredients.strip() == "":
        st.warning("Please enter ingredients.")
    else:

        with st.spinner("Generating Recipe..."):

            st.session_state.recipe = generate_recipe(ingredients)

# Display Recipe
if st.session_state.recipe != "":

    st.subheader("Generated Recipe")

    st.markdown(st.session_state.recipe)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save Recipe"):
            save_recipe(st.session_state.recipe)
            st.success("Recipe Saved!")

    with col2:
        st.download_button(
            "⬇ Download Recipe",
            st.session_state.recipe,
            file_name="recipe.txt",
            mime="text/plain"
        )

# -------------------------------
# Search Saved Recipes
# -------------------------------

st.divider()

st.subheader("📚 Saved Recipes")

search = st.text_input("Search Saved Recipes")

filtered = []

if search.strip():

    for recipe in saved_recipes:
        if search.lower() in recipe.lower():
            filtered.append(recipe)

else:
    filtered = saved_recipes

if filtered:

    for i, recipe in enumerate(filtered):

        with st.expander(f"Recipe {i+1}"):

            st.markdown(recipe)

else:
    st.info("No recipes found.")
