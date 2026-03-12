import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import json
import uuid

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Trading Rulebook", layout="wide")

DATA_FILE = "rules.json"
IMAGE_FOLDER = "images"
FACE_DB = "faces_db"

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(FACE_DB, exist_ok=True)

# ===============================
# SESSION STATE
# ===============================
if "face_authenticated" not in st.session_state:
    st.session_state.face_authenticated = False

# ===============================
# LOAD RULES
# ===============================
def load_rules():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_rules(rules):
    with open(DATA_FILE, "w") as f:
        json.dump(rules, f, indent=4)

rules = load_rules()

# ===============================
# FACE DETECTOR
# ===============================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detect_face(img):

    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]

    return img[y:y+h, x:x+w]


def face_similarity(face1, face2):

    if face1 is None or face2 is None:
        return 999

    face1 = cv2.resize(face1, (200, 200))
    face2 = cv2.resize(face2, (200, 200))

    diff = cv2.absdiff(face1, face2)

    return np.mean(diff)

# ===============================
# STYLE
# ===============================
st.markdown("""
<style>
.main-title {
font-size:40px;
font-weight:800;
color:#FFD700;
text-align:center;
}

.rule-header {
font-size:26px;
font-weight:700;
color:#00E5FF;
margin-top:30px;
}

.rule-box {
background-color:#111111;
padding:20px;
border-radius:12px;
border-left:6px solid #FFD700;
font-size:18px;
color:white;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# MENU
# ===============================
menu = st.sidebar.radio("Navigation", ["📖 View Rules","🔐 Admin Panel"])

# ===============================
# VIEW RULES
# ===============================
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

# ===============================
# ADMIN PANEL
# ===============================
if menu == "🔐 Admin Panel":

    if not st.session_state.face_authenticated:

        st.subheader("📷 Face Authentication")

        img_file = st.camera_input("Scan Your Face")

        if img_file:

            # Convert camera image
            img = Image.open(img_file)
            img = np.array(img)

            # Convert RGB to BGR for OpenCV
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            captured_face = detect_face(img)

            if captured_face is None:

                st.error("No face detected")

            else:

                match = False
                user = ""

                for file in os.listdir(FACE_DB):

                    db_path = os.path.join(FACE_DB, file)

                    db_img = cv2.imread(db_path)

                    if db_img is None:
                        continue

                    db_face = detect_face(db_img)

                    score = face_similarity(captured_face, db_face)

                    if score < 40:
                        match = True
                        user = file.split(".")[0]
                        break

                if match:

                    st.success(f"Welcome {user}")
                    st.session_state.face_authenticated = True
                    st.rerun()

                else:

                    st.error("Face not recognized")

    else:

        st.success("Admin Access Granted")

        st.subheader("➕ Add New Rule")

        title = st.text_input("Rule Title")

        description = st.text_area("Enter Rule Points (One per line)")

        image_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

        if st.button("Save Rule"):

            if title and description:

                points = [x.strip() for x in description.split("\n") if x.strip()]

                image_path=""

                if image_file:

                    name=f"{uuid.uuid4()}.png"
                    image_path=os.path.join(IMAGE_FOLDER,name)

                    with open(image_path,"wb") as f:
                        f.write(image_file.getbuffer())

                rule={
                "id":str(uuid.uuid4()),
                "title":title,
                "description":points,
                "image":image_path
                }

                rules.append(rule)
                save_rules(rules)

                st.success("Rule Saved")

            else:
                st.warning("Title and Description Required")
