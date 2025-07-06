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

def calculate_checksum(id13):
    # Luhn algorithm for Egyptian ID
    weights = [2, 1] * 7  # 13 digits
    total = 0
    for i, digit in enumerate(reversed(id13)):
        d = int(digit)
        w = weights[i]
        prod = d * w
        if prod > 9:
            prod = prod // 10 + prod % 10
        total += prod
    checksum = (10 - (total % 10)) % 10
    return str(checksum)

def generate_id(birth_date, governorate_code, serial, gender_digit, calc_checksum=False):
    century_digit = "2" if birth_date.year < 2000 else "3"
    date_part = birth_date.strftime("%y%m%d")
    gov_code = governorate_code.zfill(2)
    serial_str = serial.zfill(3)
    id13 = f"{century_digit}{date_part}{gov_code}{serial_str}{gender_digit}"
    if calc_checksum:
        checksum = calculate_checksum(id13)
    else:
        checksum = "*"
    return id13 + checksum

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
                st.success("✅ The ID is structurally valid!")
                st.info("Note: This means the ID format and components are correct, but it may not be an officially issued ID.")
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
        st.markdown("#### Serial and Gender Digit")
        serial = st.text_input(
            "Enter 3-digit serial (assigned by Civil Registry, e.g. 123):",
            max_chars=3,
            value="001",
            help="This is the unique serial for people born on the same day in the same governorate."
        )
        # Suggest gender digit based on gender
        if gender == "Male":
            gender_digit_options = ("1", "3", "5", "7", "9")
        else:
            gender_digit_options = ("2", "4", "6", "8")
        gender_digit = st.selectbox(
            "Pick gender digit (odd for Male, even for Female):",
            gender_digit_options,
            index=0,
            help="This digit should be odd for males and even for females."
        )
        calc_checksum = st.checkbox("Calculate checksum digit", value=True, help="Checksum is only calculated if serial and gender digit are valid.")
        # Live preview
        preview_id = ""
        if serial.isdigit() and len(serial) == 3 and gender_digit.isdigit():
            preview_id = generate_id(birth_date, governorate_code, serial, gender_digit, calc_checksum)
        else:
            preview_id = generate_id(birth_date, governorate_code, serial if serial else "***", gender_digit if gender_digit else "*", False)
        st.markdown("**Live Preview:**")
        st.code(preview_id, language="text")
        submitted = st.form_submit_button("Generate")
    if submitted:
        if not (serial.isdigit() and len(serial) == 3 and gender_digit.isdigit()):
            st.warning("Please enter a valid 3-digit serial and select a gender digit.")
        else:
            generated_id = generate_id(birth_date, governorate_code, serial, gender_digit, calc_checksum)
            st.success("Generated Egyptian National ID:")
            st.code(generated_id, language="text")
            st.caption(
                "The last 5 digits of the ID are:\n"
                "- The 4 serial digits (3-digit serial + gender digit) are assigned by the Civil Registry. "
                "You can enter your own serial and pick a gender digit (odd for male, even for female).\n"
                "- The final digit is a checksum, calculated from all previous digits using the Luhn algorithm. "
                "Checksum calculation: Multiply each of the first 13 digits by alternating weights of 2 and 1 (from right to left). "
                "If a product is greater than 9, add its digits. Sum all results. The checksum is the digit that makes the total a multiple of 10."
            )

# st.caption("Built with Streamlit")