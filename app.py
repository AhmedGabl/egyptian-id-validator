import streamlit as st
from datetime import datetime
from egyptian_id_validator.validation import validate_id

# Complete list of governorates with codes
GOVERNORATES = [
    ("01", "Cairo"),
    ("02", "Alexandria"),
    ("03", "Port Said"),
    ("04", "Suez"),
    ("11", "Damietta"),
    ("12", "Dakahlia"),
    ("13", "Sharkia"),
    ("14", "Kalyoubia"),
    ("15", "Kafr El Sheikh"),
    ("16", "Gharbia"),
    ("17", "Monufia"),
    ("18", "Beheira"),
    ("19", "Ismailia"),
    ("21", "Giza"),
    ("22", "Beni Suef"),
    ("23", "Fayoum"),
    ("24", "Minya"),
    ("25", "Assiut"),
    ("26", "Sohag"),
    ("27", "Qena"),
    ("28", "Aswan"),
    ("29", "Luxor"),
    ("31", "Red Sea"),
    ("32", "New Valley"),
    ("33", "Matrouh"),
    ("34", "North Sinai"),
    ("35", "South Sinai"),
    ("88", "Foreign"),
]

def generate_id(birth_date, governorate_code, gender):
    # Century digit: 2 for 1900s, 3 for 2000s
    century_digit = "2" if birth_date.year < 2000 else "3"
    date_part = birth_date.strftime("%y%m%d")
    gov_code = governorate_code.zfill(2)
    serial = "***"
    gender_digit = "1" if gender == "Male" else "2"
    partial_id = f"{century_digit}{date_part}{gov_code}{serial}{gender_digit}"
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
            gov_display = [f"{code} - {name}" for code, name in GOVERNORATES]
            gov_selected = st.selectbox("Governorate", gov_display)
            governorate_code = gov_selected.split(" - ")[0]
        gender = st.selectbox("Gender", ("Male", "Female"))
        submitted = st.form_submit_button("Generate")
    if submitted:
        generated_id = generate_id(birth_date, governorate_code, gender)
        st.success("Generated Egyptian National ID:")
        st.code(generated_id, language="text")
        st.caption("Fields marked with * are placeholders for unknown/generated parts.")

st.caption("Built with Streamlit")