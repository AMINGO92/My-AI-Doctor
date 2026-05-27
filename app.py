import streamlit as st
from PIL import Image
import pandas as pd
import sqlite3
import datetime
from google import genai
import os
import numpy as np


st.set_page_config(page_title="Fit AI Pro MAX", layout="wide")

API_KEY = os.getenv("GEMINI_API_KEY")

API_KEY = "AIzaSyDw2QoKJexPkDh0bHSv9MSDZBeUQxIm8Ao"

client = genai.Client(api_key=API_KEY)


# ================= UI STYLE =================
st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.25), transparent 28%),
        radial-gradient(circle at top right, rgba(168,85,247,0.22), transparent 30%),
        linear-gradient(145deg,#020617,#0f172a,#111827);

    color: white;
}

.block-container {
    padding-top: 1.8rem;
}

/* ================= TITLE ================= */

h1 {
    text-align: center;
    font-size: 64px;
    font-weight: 900;
    color: white;
}

/* ================= GLASS SECTION ================= */

.section {

    background: rgba(255,255,255,0.06);

    backdrop-filter: blur(22px);

    padding: 24px;

    border-radius: 28px;

    border: 1px solid rgba(255,255,255,0.10);

    box-shadow: 0 10px 45px rgba(0,0,0,0.45);
    margin-bottom: 22px;
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #020617,
            #0f172a,
            #111827
        );
}

/* ================= BUTTON ================= */

.stButton > button {

    width: auto;

    min-width: 180px;

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        );

    color: white !important;

    border: none;

    padding: 14px;

    font-weight: 800;

    font-size: 16px;
}

/* ================= FORM BUTTON ================= */

div[data-testid="stForm"] button {

    width: 220px !important;

    border-radius: 18px !important;

    background:
        linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        ) !important;

    color: white !important;

    border: none !important;

    padding: 14px !important;

    font-weight: 800 !important;

    font-size: 18px !important;
}

/* ================= INPUT BOX ================= */

/* ================= TEXT INPUT ================= */

.stTextInput input,
.stNumberInput input,
textarea {

    background: rgba(255,255,255,0.96) !important;

    color: black !important;

    -webkit-text-fill-color: black !important;

    border-radius: 18px !important;

    border: 2px solid rgba(99,102,241,0.35) !important;

    padding: 14px !important;

    font-size: 17px !important;

    font-weight: 600 !important;

    box-shadow:
        0 4px 20px rgba(0,0,0,0.15),
        0 0 12px rgba(99,102,241,0.15);

    transition: 0.3s ease;
}


/* ================= NUMBER INPUT FIX ================= */

/* ULTRA SMALL + - BUTTON */

.stNumberInput > div > div > button {

    width: 18px !important;

    min-width: 18px !important;

    max-width: 18px !important;

    height: 18px !important;

    min-height: 18px !important;

    flex: 0 0 18px !important;

    padding: 0px !important;

    font-size: 8px !important;

    line-height: 8px !important;

    border-radius: 4px !important;

    background: #2563eb !important;

    color: white !important;
}

/* NUMBER LABEL FIX */

.stNumberInput label {

    color: white !important;

    font-size: 18px !important;

    font-weight: 700 !important;
}

/* NUMBER BUTTONS */

.stNumberInput button {

    background: #2563eb !important;

    color: white !important;

    border-radius: 12px !important;
}
/* ================= INPUT FOCUS ================= */

.stTextInput input:focus,
.stNumberInput input:focus,
textarea:focus {

    border: 2px solid #6366f1 !important;

    box-shadow:
        0 0 0 3px rgba(99,102,241,0.25),
        0 8px 30px rgba(99,102,241,0.25) !important;
}

/* ================= SELECT BOX ================= */

.stSelectbox div[data-baseweb="select"] {

    background: rgba(255,255,255,0.96) !important;

    color: black !important;

    border-radius: 18px !important;
}

/* ================= SELECT LABEL ================= */

.stSelectbox label {

    color: white !important;

    font-weight: 700 !important;
}

/* ================= METRIC CARD ================= */

[data-testid="metric-container"] {

    background: rgba(255,255,255,0.08) !important;

    border-radius: 24px !important;

    padding: 22px !important;

    border: 1px solid rgba(255,255,255,0.10) !important;

    box-shadow:
        0 8px 32px rgba(0,0,0,0.35);

    backdrop-filter: blur(18px);
}

/* ================= METRIC TEXT ================= */

[data-testid="metric-container"] * {

    color: white !important;
}

.stMetric label,
.stMetric div {

    color: white !important;

    font-size: 18px !important;

    font-weight: 700 !important;
}

/* ================= TABS ================= */

.stTabs [data-baseweb="tab"] {

    color: white !important;

    font-size: 18px;

    font-weight: 700;
}

/* ================= LABELS ================= */

label,
h2,
h3,
h4,
h5,
h6,
p {

    color: white !important;
}

.stSlider label {

    color: white !important;
}

/* ================= PLACEHOLDER ================= */

input::placeholder,
textarea::placeholder {

    color: #6b7280 !important;
}

/* ================= SIDEBAR TEXT ================= */

section[data-testid="stSidebar"] * {

    color: white !important;
}

/* ================= FILE UPLOADER FINAL FIX ================= */

[data-testid="stFileUploader"] label {

    color: white !important;
}

/* DROP ZONE */

[data-testid="stFileUploaderDropzone"] {

    background: rgba(255,255,255,0.96) !important;

    border-radius: 18px !important;

    border: 2px dashed rgba(99,102,241,0.35) !important;

    padding: 18px !important;
}

/* DRAG & DROP TEXT */

[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] div,
[data-testid="stFileUploaderDropzone"] p {

    color: #111827 !important;

    font-weight: 600 !important;
}

/* LOGIN REQUIRED FIX */

[data-testid="stAlert"] {

    color: white !important;
}

[data-testid="stAlert"] * {

    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ================= DATABASE =================
conn = sqlite3.connect("health.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY,password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS user_steps(username TEXT,age REAL,height REAL,weight REAL,sleep REAL,goal TEXT,date TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS daily_log(username TEXT,date TEXT,steps REAL,calories REAL,sleep REAL,notes TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS food_log(username TEXT,date TEXT,food TEXT,calories REAL)")
conn.commit()

# ================= LOGIN =================
st.sidebar.title("🔐 Account")

mode = st.sidebar.radio("Select", ["Login", "Signup"])

if mode == "Signup":

    u = st.sidebar.text_input("Username")
    p = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Create"):

        try:
            c.execute("INSERT INTO users VALUES (?,?)",(u,p))
            conn.commit()
            st.sidebar.success("Created")

        except:
            st.sidebar.error("Exists")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

user = c.execute(
    "SELECT * FROM users WHERE username=? AND password=?",
    (username,password)
).fetchone()

if not user:
    st.warning("Login required")
    st.stop()

# ================= NLP =================
def detect_intent(text):

    text = text.lower()

    if "diet" in text:
        return "diet"

    if "weight" in text:
        return "weight"

    if "calorie" in text:
        return "calorie"

    return "general"

def smart_reply(q, bmi, burn, cal):

    intent = detect_intent(q)

    if intent == "diet":
        return "Increase protein, reduce sugar"

    if intent == "weight":
        return "Fat loss mode" if burn > cal else "Weight gain risk"

    return "Maintain balance"

# ================= STEP =================
if "step" not in st.session_state:
    st.session_state.step = 1

st.title("🔥 Fit AI Pro MAX")

# ================= STEP 1 =================
if st.session_state.step == 1:

    st.markdown("### 😴 Sleep")

    sleep_default = st.session_state.get("sleep", 7.0)

    sleep = st.number_input("Hours", value=sleep_default)

    if st.button("Next ➡️"):

        st.session_state.sleep = sleep
        st.session_state.step = 2
        st.rerun()

# ================= STEP 2 =================
elif st.session_state.step == 2:

    st.markdown("### 📏 Body Details")

    with st.form("body_form"):

        age_default = st.session_state.get("age", 33)
        height_default = st.session_state.get("height", 170)
        weight_default = st.session_state.get("weight", 75.0)

        age = st.number_input("Age", value=age_default)

        height = st.number_input("Height", value=height_default)

        weight = st.number_input("Weight", value=weight_default)

        submit = st.form_submit_button("Next")

        if submit:

            st.session_state.age = age
            st.session_state.height = height
            st.session_state.weight = weight
            st.session_state.step = 3
            st.rerun()

# ================= STEP 3 =================
elif st.session_state.step == 3:

    st.markdown("### 🎯 Goal")

    goal = st.selectbox(
        "Select Goal",
        ["Fat Loss","Muscle Gain"]
    )

    if st.button("Save & Continue"):

        c.execute(
            "INSERT INTO user_steps VALUES (?,?,?,?,?,?,?)",
            (
                username,
                st.session_state.age,
                st.session_state.height,
                st.session_state.weight,
                st.session_state.sleep,
                goal,
                str(datetime.date.today())
            )
        )

        conn.commit()

        st.session_state.step = 4
        st.rerun()

# ================= STEP 4 =================
elif st.session_state.step == 4:

    # ================= TABS =================
    tab1, tab2, tab3 = st.tabs(
        ["📊 Dashboard","🍔 Food Scanner","🤖 AI Coach"]
    )

    # ================= DATA =================
    data = pd.read_sql(
        "SELECT * FROM user_steps WHERE username=?",
        conn,
        params=(username,)
    )

    log = pd.read_sql(
        "SELECT * FROM daily_log WHERE username=?",
        conn,
        params=(username,)
    )

    food_df = pd.read_sql(
        "SELECT * FROM food_log WHERE username=?",
        conn,
        params=(username,)
    )

    latest = data.iloc[-1]

    weight_now = latest['weight']
    height = latest['height']
    age = latest['age']

    # ================= TAB 1 =================
    with tab1:

        # ================= BODY =================
        st.markdown('<div class="section">', unsafe_allow_html=True)

        bmi = weight_now / ((height/100)**2)

        bmr = (
            10 * weight_now
            + 6.25 * height
            - 5 * age
            + 5
        )

        body_fat = (
            (1.2 * bmi)
            + (0.23 * age)
            - 16.2
        )

        st.subheader("🧠 Body Metrics")


        col1, col2, col3 = st.columns(3)

        col1.metric("BMI", round(bmi,2))
        col2.metric("BMR", round(bmr))
        col3.metric("Body Fat %", round(body_fat,2))

        st.subheader("📈 Weight Progress")

        st.line_chart(data["weight"])

        st.markdown('</div>', unsafe_allow_html=True)

        # ================= DAILY =================
        st.markdown('<div class="section">', unsafe_allow_html=True)

        st.subheader("📝 Daily Log")
        
        water = st.slider(
            "💧 Water Intake (ml)",
            0,
            5000,
            2000
        )

        st.progress(min(water / 3000, 1.0))

        col1, col2 = st.columns(2)

        steps = col1.number_input("Steps",0)
        cal = col2.number_input("Calories",0)

        if st.button("💾 Save Today"):

            today = str(datetime.date.today())

            c.execute(
                "DELETE FROM daily_log WHERE username=? AND date=?",
                (username,today)
            )

            c.execute(
                "INSERT INTO daily_log VALUES (?,?,?,?,?,?)",
                (
                    username,
                    today,
                    steps,
                    cal,
                    0,
                    ""
                )
            )

            conn.commit()

            st.success("Saved")

        st.markdown('</div>', unsafe_allow_html=True)

        # ================= ANALYSIS =================
        if log.empty:

            st.info("📊 Please add daily data")

        else:

            avg_steps = int(log["steps"].mean())
            avg_cal = int(log["calories"].mean())

            # ✅ FIXED BURN
            burn = bmr + (avg_steps * 0.04)

            deficit = burn - avg_cal

            st.markdown('<div class="section">', unsafe_allow_html=True)

            st.subheader("🔥 Burn vs Intake")

            col1, col2 = st.columns(2)

            col1.metric("Burn", round(burn))
            col2.metric("Calories", avg_cal)

            if deficit < 0:
                st.error("⚠️ Weight वाढतो आहे")
            else:
                st.success("🔥 Weight कमी होतो आहे")

            st.progress(
                min(100, int((burn/(avg_cal+1))*100))
            )

            st.subheader("🧬 Prediction")

            st.info(
                f"7 Days → {round(weight_now-(deficit*7/7700),2)} kg"
            )

            st.info(
                f"30 Days → {round(weight_now-(deficit*30/7700),2)} kg"
            )

            days = st.slider("Days", 1, 90, 30)

            st.success(
                f"Future → {round(weight_now-(deficit*days/7700),2)} kg"
            )

            st.markdown('</div>', unsafe_allow_html=True)

            # ================= DIET =================
            st.markdown('<div class="section">', unsafe_allow_html=True)

            st.subheader("🥗 Diet Plan")

            maintenance = weight_now * 30

            total = (
                maintenance - 400
                if latest['goal']=="Fat Loss"
                else maintenance + 400
            )

            st.write(f"Calories: {round(total)}")
            st.write(f"Protein: {round(weight_now*2)} g")

            st.markdown('</div>', unsafe_allow_html=True)

    # ================= TAB 2 =================
    with tab2:

        st.markdown('<div class="section">', unsafe_allow_html=True)

        st.subheader("🍔 Smart AI Food Scanner PRO")

        food_file = st.file_uploader(
            "Upload food image",
            type=["png", "jpg", "jpeg"],
            key="food_upload"
        )

        if food_file and API_KEY:

            image = Image.open(food_file)

            col1, col2 = st.columns([1,2])

            with col1:
                st.image(image, caption="Uploaded Food", width=320)

            with col2:

                st.info("🤖 AI is scanning food...")
                st.progress(25)

                st.caption("⚡ Powered by Gemini Vision AI")

            with st.spinner("Deep AI Analysis Running..."):

                try:

                    res = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            """
                            You are elite AI nutritionist.

                            Analyze this food image deeply.

                            Give professional output in this format:

                            1. Food Name

                            2. Estimated Calories

                            3. Protein (g)

                            4. Carbs (g)

                            5. Fat (g)

                            6. Fiber

                            7. Sugar level

                            8. Healthy Score /10

                            9. Best for:
                            - Fat Loss
                            - Muscle Gain
                            - Diabetic
                            - Heart Health

                            10. Risks

                            11. Vitamins & Minerals

                            12. Best Time To Eat

                            13. Workout Suggestion

                            14. Final AI Verdict

                            Keep answer clean, modern and professional.
                            """,
                            image
                        ]
                    )

                    st.progress(100)

                    st.success("✅ AI Food Analysis Complete")

                    st.markdown("## 📋 AI Nutrition Report")

                    st.write(res.text)

                    # ================= ESTIMATED CALORIES =================

                    estimated_calories = 200

                    # ================= SAVE BUTTON =================

                    if st.button("💾 Save Food Analysis"):

                        c.execute(
                            "INSERT INTO food_log VALUES (?,?,?,?)",
                            (
                                username,
                                str(datetime.date.today()),
                                food_file.name,
                                estimated_calories
                            )
                        )

                        conn.commit()

                        st.success("✅ Food Saved Successfully")

                    # ================= SMART HEALTH SCORE =================

                    st.markdown("## 🧠 Smart Health Score")

                    score = np.random.randint(60, 96)

                    st.metric(
                        "AI Health Score",
                        f"{score}/100"
                    )

                    if score >= 85:
                        st.success("🔥 Excellent Food Choice")

                    elif score >= 70:
                        st.warning("⚠️ Moderate Food Choice")

                    else:
                        st.error("❌ Unhealthy Food")

                    # ================= AI RECOMMENDATION =================

                    st.markdown("## 🥗 AI Recommendation")

                    recommendations = [
                        "Increase protein intake",
                        "Reduce sugar consumption",
                        "Add more vegetables",
                        "Drink more water",
                        "Avoid processed foods",
                        "Balance carbs and fats",
                        "Add fruits for vitamins"
                    ]

                    st.write(
                        np.random.choice(
                            recommendations
                        )
                    )

                    # ================= DAILY NUTRITION SUMMARY =================

                    st.markdown("## 📊 Daily Nutrition Summary")

                    total_foods = len(food_df)

                    st.metric(
                        "Foods Logged",
                        total_foods
                    )

                    st.metric(
                        "Estimated Daily Calories",
                        total_foods * estimated_calories
                    )

                except Exception as e:

                    if "429" in str(e):

                        st.error("🚫 Gemini Free Limit Finished")

                        st.info("⏳ Try Again After Some Time")

                    else:

                        st.error(f"❌ Error: {e}")

        st.markdown('</div>', unsafe_allow_html=True)
          

    # ================= TAB 3 =================
    with tab3:

        st.subheader("🍽️ AI Meal Planner")

        meal_goal = st.selectbox(
            "Select Meal Goal",
            ["Fat Loss", "Muscle Gain"]
        )

        if st.button("Generate Meal Plan"):

            prompt = f"""
            Create Indian {meal_goal} meal plan
            with breakfast, lunch, dinner
            and protein rich foods.
            """

            client = genai.Client(api_key=API_KEY)

            
            res = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.success("Meal Plan Ready")

            st.write(res.text)

        st.markdown('<div class="section">', unsafe_allow_html=True)

        st.subheader("🤖 AI Coach")

        user_q = st.text_input("Ask anything")

        if user_q and API_KEY:

            with st.spinner("Thinking..."):


                client = genai.Client(api_key=API_KEY)                

                context = (
                    f"BMI:{round(bmi,2)} "
                    f"Steps:{avg_steps if not log.empty else 0}"
                )

                res = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=context + user_q
                )

                st.success("Answer")

                st.write(res.text)

                st.info(
                    "Tip: " +
                    smart_reply(user_q,bmi,burn,avg_cal)
                )

        st.subheader("🧪 Medical AI")

        files = st.file_uploader(
            "Upload report",
            accept_multiple_files=True
        )

        if files and API_KEY:

            st.write("Total Files:", len(files))

        all_reports = []

        for f in files:

                st.write("Processing:", f.name)

                try:

                    image = Image.open(f)

                    res = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            """
                            Analyze this medical report.

                            Give:
                            1. Short Summary
                            2. Main Problems
                            3. Risks level
                            4. Abnormal findings
                            5. Final Conclusion
                            6. Next Steps

                            Keep answer short and professional.
                            """,
                            image
                        ]
                    )

                    all_reports.append(
                        f"\n\n===== {f.name} =====\n\n{res.text}"
                    )

                except Exception as e:

                    all_reports.append(
                        f"\n\n===== {f.name} =====\n\nERROR: {e}"
                    )

        final_output = "\n\n".join(all_reports)

        st.write(final_output)    

   
