import streamlit as st
from PIL import Image
import os
import json
import uuid
import face_recognition
import numpy as np

# ======================================
# CONFIG
# ======================================
st.set_page_config(page_title="Trading Rulebook", layout="wide")

DATA_FILE = "rules.json"
IMAGE_FOLDER = "images"
FACE_DB = "faces_db"

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(FACE_DB, exist_ok=True)

# ======================================
# LOAD FACE DATABASE
# ======================================
known_encodings = []
known_names = []

for file in os.listdir(FACE_DB):
    img_path = os.path.join(FACE_DB, file)

    try:
        img = face_recognition.load_image_file(img_path)
        enc = face_recognition.face_encodings(img)

        if enc:
            known_encodings.append(enc[0])
            known_names.append(file.split(".")[0])

    except:
        pass


# ======================================
# SESSION STATE
# ======================================
if "face_authenticated" not in st.session_state:
    st.session_state.face_authenticated = False


# ======================================
# LOAD RULES
# ======================================
def load_rules():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_rules(rules):
    with open(DATA_FILE, "w") as f:
        json.dump(rules, f, indent=4)


rules = load_rules()

# ======================================
# CUSTOM STYLE
# ======================================
st.markdown("""
<style>
.main-title {
    font-size: 40px;
    font-weight: 800;
    color: #FFD700;
    text-align: center;
}

.rule-header {
    font-size: 26px;
    font-weight: 700;
    color: #00E5FF;
    margin-top: 30px;
}

.rule-box {
    background-color: #111111;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #FFD700;
    font-size: 18px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ======================================
# SIDEBAR
# ======================================
menu = st.sidebar.radio("Navigation", ["📖 View Rules", "🔐 Admin Panel"])

# ======================================
# VIEW RULES
# ======================================
if menu == "📖 View Rules":

    st.markdown('<div class="main-title">📊 MY TRADING RULEBOOK</div>', unsafe_allow_html=True)

    if not rules:
        st.info("No rules added yet.")
    else:
        for rule in rules:
            st.markdown(f'<div class="rule-header">{rule["title"]}</div>', unsafe_allow_html=True)

            st.markdown('<div class="rule-box">', unsafe_allow_html=True)

            for point in rule["description"]:
                st.markdown(f"• {point}")

            st.markdown('</div>', unsafe_allow_html=True)

            if rule["image"] and os.path.exists(rule["image"]):
                st.image(rule["image"], use_container_width=True)

            st.markdown("---")

# ======================================
# ADMIN PANEL
# ======================================
if menu == "🔐 Admin Panel":

    if not st.session_state.face_authenticated:

        st.subheader("📷 Face Authentication Required")

        img_file = st.camera_input("Scan Your Face")

        if img_file is not None:

            image = face_recognition.load_image_file(img_file)
            encodings = face_recognition.face_encodings(image)

            if encodings:

                face_encoding = encodings[0]

                distances = face_recognition.face_distance(
                    known_encodings, face_encoding
                )

                if len(distances) > 0 and min(distances) < 0.5:

                    idx = np.argmin(distances)
                    user = known_names[idx]

                    st.success(f"Welcome {user} ✅")
                    st.session_state.face_authenticated = True
                    st.rerun()

                else:
                    st.error("Face not recognized ❌")

            else:
                st.warning("No face detected")

    else:

        st.success("Admin Access Granted 🔓")

        st.subheader("➕ Add New Rule")

        title = st.text_input("Rule Title")

        description = st.text_area(
            "Enter Rule Points (One per line)",
            height=150
        )

        image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

        if st.button("Save Rule"):

            if title and description:

                points = [
                    line.strip()
                    for line in description.split("\n")
                    if line.strip()
                ]

                image_path = ""

                if image_file:
                    image_name = f"{uuid.uuid4()}.png"
                    image_path = os.path.join(IMAGE_FOLDER, image_name)

                    with open(image_path, "wb") as f:
                        f.write(image_file.getbuffer())

                new_rule = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "description": points,
                    "image": image_path
                }

                rules.append(new_rule)
                save_rules(rules)

                st.success("Rule Saved Successfully 🎯")

            else:
                st.warning("Title and Description Required")

        # ======================================
        # EDIT / DELETE RULES
        # ======================================
        st.subheader("✏ Manage Existing Rules")

        for rule in rules:

            with st.expander(rule["title"]):

                new_title = st.text_input(
                    "Edit Title",
                    rule["title"],
                    key=rule["id"] + "title"
                )

                new_description = st.text_area(
                    "Edit Description (One per line)",
                    "\n".join(rule["description"]),
                    key=rule["id"] + "desc"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button("Update", key=rule["id"] + "update"):

                        rule["title"] = new_title
                        rule["description"] = [
                            line.strip()
                            for line in new_description.split("\n")
                            if line.strip()
                        ]

                        save_rules(rules)
                        st.success("Updated Successfully")

                with col2:

                    if st.button("Delete", key=rule["id"] + "delete"):

                        rules.remove(rule)
                        save_rules(rules)
                        st.warning("Rule Deleted")
                        st.rerun()
