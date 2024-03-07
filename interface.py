import streamlit as st

# "Input a number" fields
postal_code = st.number_input("Postal Code", value=4000)
bedrooms = st.number_input("Bedrooms", value=2)
surface_of_good = st.number_input("Surface of Good (M²)", value=200)
number_of_facades = st.number_input("Number of Facades", value=4)
living_area = st.number_input("Living Area (M²)", value=100)
construction_year = st.number_input("Construction Year", value=2000)
garden_area = st.number_input("Garden Area (M²)", value=50)

# "Select appropriate value" fields
type_of_property = st.selectbox(
    "Type of Property",
    ("House", "Apartment", "Land", "Office", "Garage", "Industry", "Business", "Other"),
)
kitchen = st.selectbox(
    "Kitchen",
    (
        None,
        "installed",
        "not installed",
        "hyper equiped",
        "semi equiped",
        "usa hyper equipped",
        "usa installed",
        "usa semi equipped",
        "usa uninstalled",
    ),
)
state_of_building = st.selectbox(
    "State of Building",
    (
        None,
        "just renovated",
        "good",
        "as new",
        "to be done up",
        "to renovate",
        "to restore",
    ),
)
heating = st.selectbox(
    "Heating", (None, "gas", "fueloil", "electric", "pellet", "wood", "solar", "carbon")
)

# "True / False" fields
openfire = st.selectbox("Openfire", ("True", "False"))
furnished = st.selectbox("Furnished", ("True", "False"))
terrace = st.selectbox("Terrace", ("True", "False"))
garden = st.selectbox("Garden", ("True", "False"))
pool = st.selectbox("Swimming Pool", ("True", "False"))

st.button("Predict")
