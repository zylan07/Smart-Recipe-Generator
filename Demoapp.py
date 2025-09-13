import streamlit as st
import google.generativeai as genai
import random

# ========== CONFIG ==========
# Configure Gemini (replace with your actual API key)
genai.configure(api_key="AIzaSyCGvWUmJhRiQfmQOS-dfiREkWryqdudkE8")
model = genai.GenerativeModel("gemini-1.5-flash")

# Valid credentials
VALID_USERS = ["saran", "sathya", "tp"]
VALID_PASSWORD = "267267"

# Ingredient categories
VEG_INGREDIENTS = [
    "Tomato", "Onion", "Potato", "Rice", "Spinach", "Carrot", "Mushroom", "Paneer", "Cheese", "Bread"
]
NONVEG_INGREDIENTS = [
    "Chicken", "Egg", "Fish", "Prawns", "Mutton", "Beef", "Duck", "Turkey", "Bacon"
]

# Surprise recipes
SURPRISE_RECIPES = {
    "veg": [
        "Paneer Butter Masala, Rice, Garlic Naan",
        "Vegetable Pulao, Raita, Salad",
        "Mushroom Soup, Garlic Bread, Cheese",
        "Spinach Curry, Rice, Carrot Fry"
    ],
    "nonveg": [
        "Chicken Biryani, Onion Raita",
        "Grilled Fish, Lemon Butter Sauce",
        "Egg Curry, Chapati",
        "Prawn Masala, Rice"
    ]
}

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Smart Recipe Generator", page_icon="🍴", layout="wide")

# ========== LOGIN FLOW ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "category" not in st.session_state:
    st.session_state.category = None

# Step 1: Login Page
if not st.session_state.logged_in:
    st.title("👨‍💻 Tri Techies")
    st.subheader("📌 Smart Recipe Generator")
    st.markdown("### 👥 Team Members:")
    st.markdown("""
    - Saran S  
    - Sathya R V  
    - Tharun Pranav T
    """)

    st.markdown("---")
    st.header("🔐 Login to Continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username.lower() in VALID_USERS and password == VALID_PASSWORD:
            st.session_state.logged_in = True
            st.success("✅ Login successful! Please select Veg or Non-Veg next.")
            st.rerun()
        else:
            st.error("❌ Incorrect username or password. Try again.")

# Step 2: Veg/Non-Veg Selection
elif st.session_state.logged_in and st.session_state.category is None:
    st.title("🍽️ Choose Your Preference")
    option = st.radio("Do you want Veg or Non-Veg recipes?", ["Veg", "Non-Veg"])

    if st.button("Confirm Choice"):
        st.session_state.category = option.lower()
        st.success(f"✅ You selected {option}! Loading ingredient options...")
        st.rerun()

# Step 3: Main App
else:
    category = st.session_state.category

    st.title("🥘 Smart Recipe Generator - What's in My Fridge?")
    st.markdown(f"### 🍳 Selected Category: **{category.capitalize()}**")

    # Sidebar
    with st.sidebar:
        st.header("👩‍🍳 Cooking Tips")
        st.info("💡 Use fresh ingredients for better taste!\n\n🔥 Spice it up with herbs!\n\n🥗 Balance flavors: sweet, salty, sour, bitter.")
        st.markdown("---")
        st.caption("Created with ❤️ by Tri Techies")

    # Ingredients list based on category
    ingredient_list = VEG_INGREDIENTS if category == "veg" else NONVEG_INGREDIENTS

    # Layout: two columns
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🛒 Choose Ingredients")

        selected_items = st.multiselect("Pick from available items:", ingredient_list)

        custom_ingredients = st.text_area("Or add your own (comma separated):")

        # Merge inputs
        all_ingredients = ", ".join(selected_items) + (", " + custom_ingredients if custom_ingredients else "")

        # Buttons
        generate_btn = st.button("🍲 Generate Recipe")
        surprise_btn = st.button("🎲 Surprise Me!")

    with col2:
        if generate_btn or surprise_btn:
            if not all_ingredients.strip() and not surprise_btn:
                st.warning("⚠️ Please enter or select some ingredients first!")
            else:
                # Surprise recipes are based on veg/non-veg choice
                if surprise_btn and not all_ingredients.strip():
                    all_ingredients = random.choice(SURPRISE_RECIPES[category])

                prompt = f"""
                You are a recipe generator AI. User has the following {category} ingredients: {all_ingredients}.
                - Suggest a creative recipe name.
                - Provide step-by-step cooking instructions.
                - Suggest 2-3 possible substitutions for missing or uncommon ingredients.
                """

                with st.spinner("Cooking up your recipe... 🍳"):
                    response = model.generate_content(prompt)

                st.success("✨ Recipe Ready!")

                # Show Recipe
                st.subheader("🍴 Recipe Suggestion")
                st.write(response.text)

                # Expandable instructions
                with st.expander("📋 Detailed Steps"):
                    st.markdown(response.text)

                # Placeholder image
                st.image("https://i.ibb.co/6b9tL0W/recipe-placeholder.jpg", caption="Your Dish (illustrative) 🍽️", use_container_width=True)
