import streamlit as st
from egyptian_id_validator.validation import validate_id
# If you have a generate_id function, import it as well:
# from egyptian_id_validator.generation import generate_id

st.title("Egyptian National ID Validator & Generator")

option = st.radio(
    "Choose an option:",
    ("Validate National ID", "Generate National ID")
)

if option == "Validate National ID":
    id_number = st.text_input("Enter Egyptian National ID:")
    if st.button("Validate"):
        if not id_number:
            st.warning("Please enter an Egyptian National ID.")
        else:
            result = validate_id(id_number)
            if result:
                st.success("Valid ID!")
                st.json(result)
            else:
                st.error("Invalid ID.")

elif option == "Generate National ID":
    st.write("Enter the following details to generate a National ID:")
    birth_date = st.date_input("Birth Date")
    governorate_code = st.text_input("Governorate Code (e.g., 01 for Cairo)")
    gender = st.selectbox("Gender", ("Male", "Female"))
    if st.button("Generate"):
        # You need a function to generate the ID, e.g., generate_id()
        # generated_id = generate_id(birth_date, governorate_code, gender)
        # For demonstration, we'll just show the inputs:
        st.info(f"Birth Date: {birth_date}")
        st.info(f"Governorate Code: {governorate_code}")
        st.info(f"Gender: {gender}")
        st.warning("ID generation function not implemented in this example.")

st.caption("Built with Streamlit")