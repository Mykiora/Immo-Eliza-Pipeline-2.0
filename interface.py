import streamlit as st
from preprocessing import predict
import numpy as np


def predict_request() -> None:
    """
    Set the session state "clicked" to True to activate the button, then stores
    all the inputs in a dictionary and sends it to the "predict" function to get
    a result.

    Returns :
    None
    """
    st.session_state.clicked = True

    property_type_map = {
        "house": 1,
        "apartment": 2,
        "land": 3,
        "office": 4,
        "garage": 5,
        "industry": 6,
        "business": 7,
        "other": 8,
    }

    property_data = {
        "Openfire": openfire,
        "Furnished": furnished,
        "Terrace": terrace,
        "Garden": garden,
        "TypeOfProperty": property_type_map[type_of_property],
        "PostalCode": postal_code,
        "SubtypeOfProperty": np.nan,
        "TypeOfSale": np.nan,
        "Kitchen": kitchen,
        "StateOfBuilding": state_of_building,
        "Heating": heating,
        "Bedrooms": bedrooms,
        "SurfaceOfGood": surface_of_good,
        "SwimmingPool": pool,
        "NumberOfFacades": number_of_facades,
        "LivingArea": living_area,
        "ConstructionYear": construction_year,
        "GardenArea": garden_area,
    }

    st.session_state.prediction = predict(property_data)


st.title("Immo Eliza Pipeline")

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
    ("house", "apartment", "land", "office", "garage", "industry", "business", "other"),
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

st.button("Predict", on_click=predict_request)

if "clicked" not in st.session_state:
    st.session_state.clicked = False

if st.session_state.clicked:
    st.markdown(f"### Prediction : ≈{st.session_state.prediction} €")
