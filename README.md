## 🇪🇬 Egyptian National ID Validator & Generator

A lightweight Streamlit application to validate existing Egyptian national ID numbers and (optionally) generate new ones using structured input data.

---

### 🔧 Features

- **Validate ID**: Checks the format and authenticity of Egyptian national ID numbers  
- **Generate ID (coming soon)**: Generate a valid national ID using birth date, governorate code, and gender  
- **Built with**: Python, Streamlit, and [egyptian-id-validator](https://pypi.org/project/egyptian-id-validator/)

---

### 🧠 Usage Overview

1. Select either `Validate National ID` or `Generate National ID` from the sidebar.
2. For validation, input the 14-digit ID and click "Validate".
3. For generation (coming soon), enter birth date, governorate code, and gender — implementation pending.

---

### 📌 Notes

- This app depends on the `validate_id()` function from the `egyptian-id-validator` Python library.
- `generate_id()` is not currently implemented but can be extended based on known ID structure rules.

---

### 📜 License

This project is licensed under the [MIT License](LICENSE).
