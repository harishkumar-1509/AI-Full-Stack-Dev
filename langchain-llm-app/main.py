import langchain_helper as lch
import streamlit as st

st.title("Pet Name Generator")
animal_type = st.sidebar.selectbox(
    "Enter the type of animal you have:", ["dog", "cat", "bird", "fish"]
)
pet_color = st.sidebar.text_area(
    "Enter the color of your pet:",
    max_chars=15,
)
if st.button("Generate Names"):
    if pet_color:
        pet_names = lch.generate_pet_names(animal_type, pet_color)
        st.subheader("Here are some cool names for your pet:")
        st.write(pet_names)
    else:
        st.warning("Please enter the color of your pet.")
