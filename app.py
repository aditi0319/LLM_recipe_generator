import streamlit as st
from transformers import pipeline
import json
import os

st.set_page_config(page_title="AI Recipe Generator", page_icon="🍳")

# Load model only once
@st.cache_resource
def load_model():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-base"
    )

generator = load_model()

SAVE_FILE = "saved_recipes.json"

# Load saved recipes
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        saved_recipes = json.load(f)
else:
    saved_recipes = []

# Session state
if "recipe" not in st.session_state:
    st.session_state.recipe = ""

def generate_recipe(ingredients):
    prompt = f"""
Create a detailed recipe using these ingredients:

{ingredients}

Return in this format:

Recipe Name:
Ingredients:
Instructions:
"""

    result = generator(
        prompt,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.7
    )

    return result[0]["generated_text"]

def save_recipe(recipe):
    saved_recipes.append(recipe)
    with open(SAVE_FILE, "w") as f:
        json.dump(saved_recipes, f, indent=2)

st.title("🍳 AI Recipe Generator")

ingredients = st.text_input(
    "Enter ingredients (comma separated):",
    placeholder="potato, onion, cheese, butter"
)

if st.button("Generate Recipe"):
    if ingredients.strip():
        with st.spinner("Generating recipe..."):
            st.session_state.recipe = generate_recipe(ingredients)
    else:
        st.warning("Please enter some ingredients.")

if st.session_state.recipe:
    st.subheader("Generated Recipe")
    st.write(st.session_state.recipe)

    if st.button("💾 Save Recipe"):
        save_recipe(st.session_state.recipe)
        st.success("Recipe saved!")

st.subheader("📚 Saved Recipes")

if saved_recipes:
    for i, recipe in enumerate(saved_recipes, 1):
        with st.expander(f"Recipe {i}"):
            st.write(recipe)
else:
    st.info("No recipes saved yet.")
