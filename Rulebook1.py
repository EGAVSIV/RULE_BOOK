import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import json
import uuid

# ======================================
# CONFIG
# ======================================
st.set_page_config(page_title="Trading Rulebook", layout="wide")

DATA_FILE = "rules.json"
IMAGE_FOLDER = "images"
FACE_DB = "faces_db"

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(FACE_DB, exist_ok=True)

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ======================================
# SESSION STATE
# ======================================
if "face_authenticated" not in st.session_state:
    st.session_state.face_authenticated = False

# ======================================
# RULE STORAGE
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
# FACE MATCH FUNCTION
# ======================================
def extract_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        return img[y:y+h, x:x+w]

    return None


def compare_faces(face1, face2):

    face1 = cv2.resize(face1, (200, 200))
    face2 = cv2.resize(face2, (200, 200))

    diff = cv2.absdiff(face1, face2)
    score = np.mean(diff)

    return score


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

        st.subheader("📷 Face Authentication")

        img_file = st.camera_input("Scan Your Face")

        if img_file:

            captured_img = Image.open(img_file)
            captured_np = np.array(captured_img)

            captured_face = extract_face(captured_np)

            if captured_face is None:
                st.error("No face detected")
            else:

                matched = False

                for file in os.listdir(FACE_DB):

                    db_path = os.path.join(FACE_DB, file)

                    db_img = cv2.imread(db_path)

                    db_face = extract_face(db_img)

                    if db_face is None:
                        continue

                    score = compare_faces(captured_face, db_face)

                    if score < 40:  # similarity threshold
                        matched = True
                        user = file.split(".")[0]
                        break

                if matched:
                    st.success(f"Welcome {user} 🔓")
                    st.session_state.face_authenticated = True
                    st.rerun()
                else:
                    st.error("Face not recognized")

    else:

        st.success("Admin Access Granted")

        st.subheader("➕ Add New Rule")

        title = st.text_input("Rule Title")

        description = st.text_area("Enter Rule Points (One per line)")

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

        st.subheader("✏ Manage Existing Rules")

        for rule in rules:

            with st.expander(rule["title"]):

                new_title = st.text_input("Edit Title", rule["title"], key=rule["id"]+"title")

                new_description = st.text_area(
                    "Edit Description",
                    "\n".join(rule["description"]),
                    key=rule["id"]+"desc"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Update", key=rule["id"]+"update"):

                        rule["title"] = new_title
                        rule["description"] = [
                            line.strip()
                            for line in new_description.split("\n")
                            if line.strip()
                        ]

                        save_rules(rules)
                        st.success("Updated Successfully")

                with col2:
                    if st.button("Delete", key=rule["id"]+"delete"):

                        rules.remove(rule)
                        save_rules(rules)
                        st.warning("Rule Deleted")
                        st.rerun()
