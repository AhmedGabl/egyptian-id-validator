import streamlit as st
from datetime import datetime
from egyptian_id_validator.validation import validate_id

# Helper function to generate Egyptian National ID
def generate_id(birth_date, governorate_code, gender):
    # Century digit: 2 for 1900s, 3 for 2000s
    century_digit = "2" if birth_date.year < 2000 else "3"
    # YYMMDD
    date_part = birth_date.strftime("%y%m%d")
    # Governorate code (should be 2 digits)
    gov_code = governorate_code.zfill(2) if governorate_code.isdigit() else "**"
    # Serial: 4 digits, last digit is gender (odd for male, even for female)
    # We'll use *** for unknown parts
    serial = "***"
    gender_digit = "1" if gender == "Male" else "2"
    # Compose ID (without checksum)
    partial_id = f"{century_digit}{date_part}{gov_code}{serial}{gender_digit}"
    # Checksum: can't generate without full info, so use *
    checksum = "*"
    return partial_id + checksum

st.set_page_config(page_title="Egyptian National ID Validator & Generator", layout="centered")
st.title("🇪🇬 Egyptian National ID Validator & Generator")

st.markdown("Validate or generate Egyptian National IDs easily.")

option = st.radio(
    "Choose an option:",
    ("Validate National ID", "Generate National ID"),
    horizontal=True
)

if option == "Validate National ID":
    st.subheader("Validate National ID")
    id_number = st.text_input("Enter Egyptian National ID:", max_chars=14)
    if st.button("Validate"):
        if not id_number:
            st.warning("Please enter an Egyptian National ID.")
        else:
            result = validate_id(id_number)
            if result:
                st.success("✅ Valid ID!")
                st.json(result)
            else:
                st.error("❌ Invalid ID.")

elif option == "Generate National ID":
    st.subheader("Generate National ID")
    with st.form("generate_id_form"):
        col1, col2 = st.columns(2)
        with col1:
            birth_date = st.date_input("Birth Date", min_value=datetime(1900,1,1), max_value=datetime.today())
        with col2:
            governorate_code = st.text_input("Governorate Code (e.g., 01 for Cairo)", max_chars=2)
        gender = st.selectbox("Gender", ("Male", "Female"))
        submitted = st.form_submit_button("Generate")
    if submitted:
        generated_id = generate_id(birth_date, governorate_code, gender)
        st.success("Generated Egyptian National ID:")
        st.code(generated_id, language="text")
        st.caption("Fields marked with * are placeholders for unknown/generated parts.")

st.caption("Built with Streamlit")