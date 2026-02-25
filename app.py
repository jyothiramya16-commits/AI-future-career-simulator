import streamlit as st
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from datetime import datetime

st.set_page_config(page_title="Future Growth Intelligence", layout="wide")

# ---------------- THEME ----------------
theme = st.sidebar.radio("Theme Mode", ["Professional Light", "Modern Gradient Dark"])

if theme == "Modern Gradient Dark":
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg,#0f172a,#1e293b,#0f172a);
        color: #e2e8f0;
    }
    .block-container {
        padding-top: 2rem;
    }
    .card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("FUTURE GROWTH INTELLIGENCE SYSTEM")
st.caption("Strategic Lifestyle • Career • Skill Intelligence Engine")

user_id = st.text_input("User ID")

tabs = st.tabs(["Lifestyle Engine", "Career Analyzer", "Skill Gap Engine"])

# ---------------- LIFESTYLE ----------------
with tabs[0]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Lifestyle Growth Intelligence")

    col1, col2 = st.columns(2)
    with col1:
        study = st.slider("📘 Study Hours", 0, 10, 5)
        skill_hours = st.slider("🚀 Skill Development", 0, 10, 4)
    with col2:
        sleep = st.slider("😴 Sleep Quality Hours", 0, 10, 7)
        distraction = st.slider("📱 Distraction Level", 0, 10, 3)

    score = (study*10)+(skill_hours*15)+(sleep*5)-(distraction*8)
    lifestyle_score = max(min(score/1.5,100),0)

    # ---- Stylish Metric Card ----
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg,#2563eb,#7c3aed);
            padding:25px;
            border-radius:18px;
            text-align:center;
            color:white;
            font-size:22px;
            font-weight:bold;
            box-shadow:0px 6px 25px rgba(0,0,0,0.4);
        ">
        Lifestyle Growth Probability <br>
        <span style="font-size:40px;">{round(lifestyle_score)}%</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Growth Balance Overview")

    # -------- Radar Chart --------
    import numpy as np

    categories = ['Study','Skill','Sleep','Distraction']
    values = [study, skill_hours, sleep, 10-distraction]

    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    ax.set_yticklabels([])
    ax.set_title("Lifestyle Balance Radar", pad=20)

    st.pyplot(fig)

    # -------- Donut Chart --------
    st.markdown("### Growth Distribution")

    fig2, ax2 = plt.subplots()
    sizes = [study, skill_hours, sleep, distraction]
    labels = ["Study","Skill","Sleep","Distraction"]

    wedges, texts = ax2.pie(sizes, labels=labels, startangle=90)
    centre_circle = plt.Circle((0,0),0.60,fc='white')
    fig2.gca().add_artist(centre_circle)
    ax2.axis('equal')

    st.pyplot(fig2)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CAREER ANALYZER ----------------
with tabs[1]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Career Readiness Analyzer")

    dream = st.text_input("Dream Profession")

    dedication = st.slider("Dedication Level", 0, 10, 6)
    current_skill = st.slider("Current Skill Level", 0, 10, 5)
    consistency = st.slider("Consistency", 0, 10, 6)

    if dream:
        career_score = (dedication*12 + current_skill*15 + consistency*10)
        readiness = max(min(career_score/1.5,100),0)

        st.metric("Career Achievement Probability", f"{round(readiness)} %")

        if readiness > 75:
            st.success("Strong alignment toward goal.")
        elif readiness > 45:
            st.warning("Moderate readiness. Increase expertise depth.")
        else:
            st.error("Major capability gap detected.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SKILL GAP ENGINE ----------------
with tabs[2]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Real Skill Gap Engine")

    known_skills = st.text_area("List Your Skills (comma separated)")
    profession_select = st.selectbox("Target Field",
                                      ["AI Engineer","Software Developer",
                                       "Data Analyst","UI/UX Designer",
                                       "Management"])

    skill_map = {
        "AI Engineer":["python","machine learning","data structures","math","git"],
        "Software Developer":["python","java","data structures","git","problem solving"],
        "Data Analyst":["python","sql","statistics","excel","visualization"],
        "UI/UX Designer":["design","figma","creativity","user research","prototyping"],
        "Management":["communication","leadership","strategy","planning","decision making"]
    }

    if known_skills:
        user_skills = [s.strip().lower() for s in known_skills.split(",")]
        required = skill_map[profession_select]

        missing = [s for s in required if s not in user_skills]

        readiness_percent = int(((len(required)-len(missing))/len(required))*100)

        st.metric("Skill Match Percentage", f"{readiness_percent} %")

        if missing:
            st.warning(f"Missing Skills: {', '.join(missing)}")
        else:
            st.success("You meet all core skill requirements.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PROFESSION MAPPING ----------------
st.markdown("---")
st.subheader("Intelligent Profession Ranking")

if known_skills:
    ranking = {}
    for role, req in skill_map.items():
        match = len([s for s in req if s in user_skills])
        ranking[role] = int((match/len(req))*100)

    sorted_roles = sorted(ranking.items(), key=lambda x: x[1], reverse=True)

    for role, percent in sorted_roles:
        st.write(f"{role} : {percent}% match")

# ---------------- PDF EXPORT ----------------
def generate_pdf():
    file_name = f"{user_id}_Final_Report.pdf"
    doc = SimpleDocTemplate(file_name, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("FUTURE GROWTH INTELLIGENCE REPORT", styles["Title"]))
    elements.append(Spacer(1,0.3*inch))
    elements.append(Paragraph(f"User ID: {user_id}", styles["Normal"]))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    elements.append(Spacer(1,0.3*inch))
    elements.append(Paragraph(f"Lifestyle Score: {round(lifestyle_score)}%", styles["Normal"]))
    elements.append(Paragraph(f"Career Readiness: {round(readiness) if 'readiness' in locals() else 'N/A'}%", styles["Normal"]))
    elements.append(Paragraph(f"Skill Match: {readiness_percent if 'readiness_percent' in locals() else 'N/A'}%", styles["Normal"]))

    doc.build(elements)
    return file_name

if user_id:
    if st.button("Generate Final PDF Report"):
        pdf_file = generate_pdf()
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="Download Report",
                data=f,
                file_name=pdf_file,
                mime="application/pdf"
            )
