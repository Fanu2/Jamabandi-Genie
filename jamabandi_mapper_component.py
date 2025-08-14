import streamlit as st
import pandas as pd
import json
from rapidfuzz import process
from pathlib import Path

# 📁 Paths
MAPPING_FILE = Path("saved_mappings.json")
SCHEMA_DIR = Path("schemas")
CUSTOM_SCHEMA_FILE = SCHEMA_DIR / "custom_schema.json"

# 📜 Default schema
default_schema = {
    "खाता संख्या": "account_number",
    "खसरा नंबर": "plot_number",
    "साङ्गीदार का नाम": "owner_name",
    "रकबा": "area",
    "अभिलेख में दुरुस्ती का लेखा": "correction_note",
    "शेरक्षर खसरा नाम भूमि": "land_type",
    "खिंजरि": "category",
    "नियम": "rule",
}

# 📊 Schema Preview Table
def show_schema_preview(schema):
    st.markdown("### 📖 Jamabandi Schema Preview")
    schema_df = pd.DataFrame({
        "Hindi Header": list(schema.keys()),
        "Normalized Field": list(schema.values())
    })
    st.dataframe(schema_df)

# 🧰 Mapping Editor UI
def mapping_editor(schema):
    st.markdown("### 🛠 Edit Schema Mapping")
    edited = {}
    for hindi, norm in schema.items():
        new_norm = st.text_input(f"Map '{hindi}' to:", value=norm, key=f"edit_{hindi}")
        edited[hindi] = new_norm

    if st.button("💾 Save Edited Schema"):
        CUSTOM_SCHEMA_FILE.write_text(json.dumps(edited, ensure_ascii=False, indent=2))
        st.success("✅ Custom schema saved.")
    return edited

# 📤 Upload or Select Schema
def load_custom_schema(default="Default"):
    schema_files = {
        "Default": default_schema,
        "Punjab": SCHEMA_DIR / "punjab_schema.json",
        "Haryana": SCHEMA_DIR / "haryana_schema.json",
        "Custom": CUSTOM_SCHEMA_FILE
    }

    selected = st.selectbox("📂 Choose Schema Version", options=list(schema_files.keys()), index=list(schema_files.keys()).index(default))
    if selected == "Default":
        return default_schema

    try:
        path = schema_files[selected]
        schema = json.loads(path.read_text())
        st.success(f"✅ Loaded {selected} schema.")
        return schema
    except Exception as e:
        st.error(f"❌ Failed to load {selected} schema: {e}")
        return default_schema

# 🧮 Compare Two Schemas
def compare_schemas(schema_a, schema_b, label_a="Schema A", label_b="Schema B"):
    st.markdown("### 🧮 Schema Comparison")
    all_keys = sorted(set(schema_a.keys()) | set(schema_b.keys()))
    comparison = [(key, schema_a.get(key, "❌ Missing"), schema_b.get(key, "❌ Missing")) for key in all_keys]
    df_compare = pd.DataFrame(comparison, columns=["Hindi Header", label_a, label_b])
    st.dataframe(df_compare)

# 🧪 Validate Schema
def validate_schema(schema):
    errors = []
    for k, v in schema.items():
        if not isinstance(k, str) or not isinstance(v, str):
            errors.append(f"Non-string entry: '{k}' → '{v}'")
    norm_values = list(schema.values())
    duplicates = [v for v in set(norm_values) if norm_values.count(v) > 1]
    if duplicates:
        errors.append(f"Duplicate normalized fields: {', '.join(duplicates)}")
    required = ["account_number", "plot_number", "owner_name"]
    missing = [field for field in required if field not in norm_values]
    if missing:
        errors.append(f"Missing required fields: {', '.join(missing)}")
    return errors

# 📥 Excel Preview
def show_excel_preview(df):
    st.markdown("### 📥 Excel Preview")
    styled_df = df.copy()
    styled_df.columns = [f"📝 {col}" for col in styled_df.columns]
    st.dataframe(styled_df)

# 🔍 Fuzzy + Manual Remapping
def fuzzy_remap(df, schema, enable_manual=True):
    mapped = {}
    unmatched = []

    saved = {}
    if MAPPING_FILE.exists():
        saved = json.loads(MAPPING_FILE.read_text())

    for col in df.columns:
        if col in saved:
            mapped[col] = saved[col]
            continue
        result = process.extractOne(col, schema.keys(), score_cutoff=75)
        if result:
            match, score = result
            mapped[col] = schema[match]
        else:
            unmatched.append(col)
            mapped[col] = col

    if enable_manual and unmatched:
        st.warning("Some headers couldn't be auto-mapped. Please correct them manually:")
        for col in unmatched:
            new_header = st.selectbox(f"Map '{col}' to:", options=list(schema.values()), key=f"manual_map_{col}")
            mapped[col] = new_header
            saved[col] = new_header
        MAPPING_FILE.write_text(json.dumps(saved, ensure_ascii=False, indent=2))
        st.success("✅ Manual mappings saved.")

    df.columns = [mapped.get(col, col) for col in df.columns]
    return df

# 🧩 Main Component
def jamabandi_mapper_component(df_raw, region_hint="Default"):
    st.subheader("🧩 Jamabandi Schema Mapper")

    schema = load_custom_schema(default=region_hint)
    show_schema_preview(schema)

    if st.checkbox("✏️ Edit Schema Mapping"):
        schema = mapping_editor(schema)

    if st.checkbox("🔍 Compare Punjab vs Haryana Schema"):
        schema_punjab = json.loads((SCHEMA_DIR / "punjab_schema.json").read_text())
        schema_haryana = json.loads((SCHEMA_DIR / "haryana_schema.json").read_text())
        compare_schemas(schema_punjab, schema_haryana, "Punjab", "Haryana")

    errors = validate_schema(schema)
    if errors:
        st.error("❌ Schema validation failed:")
        for err in errors:
            st.markdown(f"- {err}")
        st.stop()

    enable_manual = st.checkbox("Enable Manual Header Mapping", value=True)
    mapped_df = fuzzy_remap(df_raw, schema, enable_manual=enable_manual)

    st.dataframe(mapped_df)
    show_excel_preview(mapped_df)

    return mapped_df
