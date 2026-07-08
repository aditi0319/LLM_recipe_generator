import streamlit as st
from transformers import pipeline
import json
import os

# Initialize Hugging Face pipeline with the chosen model
generator = pipeline(
    "text-generation",
    model="flax-community/t5-recipe-generation"
)

SAVE_FILE = "saved_recipes.json"

# Load saved recipes
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        saved_recipes = json.load(f)
else:
    saved_recipes = []

# Function to generate recipe
def generate_recipe(ingredients):
    prompt = f"Create a recipe using these ingredients: {ingredients}. Include recipe name and step-by-step instructions."
    # Display the prompt in bold
    st.markdown(f"**Prompt:** {prompt}")
    result = generator(prompt, max_length=150)[0]["generated_text"]
    return result

# Function to save recipe
def save_recipe(recipe_text):
    saved_recipes.append(recipe_text)
    with open(SAVE_FILE, "w") as f:
        json.dump(saved_recipes, f, indent=2)

# --- Streamlit UI ---
st.title("AI Recipe Generator")

ingredients = st.text_input("Enter ingredients (comma separated):")

if st.button("Generate Recipe"):
    if ingredients.strip():
        recipe = generate_recipe(ingredients)
        st.subheader("Generated Recipe")
        st.write(recipe)

        # Save button appears only after generating a recipe
        if st.button("Save This Recipe"):
            save_recipe(recipe)
            st.success("Recipe saved!")
    else:
        st.warning("Please enter some ingredients!")

# View saved recipes
st.subheader("Saved Recipes")
if saved_recipes:
    for i, r in enumerate(saved_recipes, 1):
        with st.expander(f"Recipe {i}"):
            st.write(r)
else:
    st.info("No recipes saved yet.")
