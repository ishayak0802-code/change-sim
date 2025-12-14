import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
# PASTE YOUR GOOGLE SHEET URL HERE
SHEET_URL = "https://docs.google.com/spreadsheets/d/1faVJ-Cf7o6b-29KeGOkV9PsK9OptUjXDtJxkg5G7YAQ/edit?usp=sharing" 
ADMIN_PASSWORD = "admin"

# --- SETUP & STYLING ---
st.set_page_config(page_title="LSH Change Simulation", layout="wide", page_icon="🛒")

# Helper to load data (Read-Only for Master View)
def load_data():
    try:
        csv_url = SHEET_URL.replace('/edit?usp=sharing', '/export?format=csv')
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame(columns=["Timestamp", "Team", "Round", "Decision", "Cost"])

# --- SIDEBAR: LOGIN & ROLE SELECTOR ---
with st.sidebar:
    st.image("https://via.placeholder.com/150?text=LSH+Logo", use_container_width=True)
    st.header("Login")
    role = st.selectbox("Select Your Role:", [
        "Select...",
        "Professor (Master View)",
        "Team 1: Business & Procurement",
        "Team 2: IT",
        "Team 3: Operations",
        "Team 4: Legal",
        "Team 5: HR & Training",
        "Team 6: Transformation Office",
        "Team 7: Corp Communications"
    ])
    
    if role == "Professor (Master View)":
        pwd = st.text_input("Password", type="password")
        if pwd != ADMIN_PASSWORD:
            st.warning("Incorrect Password")
            st.stop()

# --- PART 1: PROFESSOR MASTER VIEW ---
if role == "Professor (Master View)":
    st.title("👨‍🏫 Classroom Control Center")
    
    if st.button("🔄 Refresh Live Data"):
        st.rerun()
        
    df = load_data()
    
    # Dashboard Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Teams", df['Team'].nunique())
    col2.metric("Total Decisions Made", len(df))
    col3.metric("Total Budget Committed", f"{df['Cost'].sum():,} PLN")
    
    st.divider()
    
    # Pivot View: Teams vs Decisions
    st.subheader("Live Decision Matrix")
    st.dataframe(df.sort_values(by="Timestamp", ascending=False), use_container_width=True)
    
    st.subheader("Discussion Triggers")
    st.info("💡 **Teaching Tip:** If Team 2 (IT) chose 'In-House Development' but Team 1 (Business) chose 'Single Vendor Package', pause the class! These decisions conflict.")

# --- PART 2: STUDENT TEAM VIEWS ---
elif role != "Select...":
    st.title(f"🛒 {role}")
    st.markdown("---")
    
    # Initialize Session State for Students
    if 'submitted' not in st.session_state:
        st.session_state['submitted'] = False

    # --- TEAM SPECIFIC LOGIC ---
    
    # TEAM 1: BUSINESS [Source: 425]
    if "Team 1" in role:
        st.info("**Mission:** Allocate the 1M PLN budget and decide on the vendor strategy.")
        st.subheader("Decision 1: Vendor Strategy")
        q1 = st.radio("Choose approach:", [
            "Single Vendor (Cost: 300k, Fast but Rigid) [cite: 433]",
            "Multiple Vendors (Cost: 400k, Flexible but Complex) [cite: 434]"
        ])
        st.subheader("Decision 2: Budget Allocation")
        q2 = st.radio("Primary Budget Focus:", [
            "Heavy IT & Ops (Technical Stability)",
            "Heavy HR & Training (Adoption Focus)"
        ])
        cost = 300000 if "Single" in q1 else 400000

    # TEAM 2: IT [Source: 53]
    elif "Team 2" in role:
        st.info("**Mission:** Ensure software readiness and integration with legacy POS.")
        st.subheader("Decision 1: Development Approach")
        q1 = st.radio("Choose Strategy:", [
            "Off-the-Shelf (150k + 50k/yr, Ready in 3mo, Low Customization) [cite: 65]",
            "In-House Dev (300k, 6mo, High Integration) [cite: 66]"
        ])
        st.subheader("Decision 2: Testing Strategy")
        q2 = st.radio("Choose Strategy:", [
            "Extensive Testing (50k, Adds 2mo, Low Risk) [cite: 69]",
            "Minimal Testing (0k, Fast, High Risk) [cite: 70]"
        ])
        cost = (150000 if "Off-the-Shelf" in q1 else 300000) + (50000 if "Extensive" in q2 else 0)

    # TEAM 3: OPERATIONS [Source: 145]
    elif "Team 3" in role:
        st.info("**Mission:** Manage physical installation in 2000 stores.")
        st.subheader("Decision 1: Store Prioritization")
        q1 = st.radio("Sequence:", [
            "High-Revenue Stores First (Faster ROI, neglects small stores) [cite: 161]",
            "Even Distribution (Equitable, Slower ROI) [cite: 162]"
        ])
        st.subheader("Decision 2: Installation Timeline")
        q2 = st.radio("Approach:", [
            "One-Time Rollout (6mo, High Disruption Risk) [cite: 154]",
            "Phased Rollout (Phase 1 in 3mo, Phase 2 in 6mo) [cite: 154]"
        ])
        cost = 200000  # Base logic from docs

    # TEAM 4: LEGAL [Source: 271]
    elif "Team 4" in role:
        st.info("**Mission:** Manage GDPR and Accessibility Law X compliance.")
        st.subheader("Decision 1: Accessibility Compliance")
        q1 = st.radio("Level of Compliance:", [
            "High-End Compliance (50k, Zero Risk) [cite: 283]",
            "Minimum Compliance (20k, Risk of 500k Fine) [cite: 284]"
        ])
        st.subheader("Decision 2: Vendor Contracts")
        q2 = st.radio("Contract Type:", [
            "Standard (Free, Low protection) [cite: 287]",
            "Comprehensive (10k, High protection) [cite: 288]"
        ])
        cost = (50000 if "High-End" in q1 else 20000) + (10000 if "Comprehensive" in q2 else 0)

    # TEAM 5: HR [Source: 103]
    elif "Team 5" in role:
        st.info("**Mission:** Manage workforce transition and 30% resistance rate.")
        st.subheader("Decision 1: Transition Plan")
        q1 = st.radio("Strategy:", [
            "Redeployment to Service Roles (100k, Retains Staff) [cite: 115]",
            "Severance Packages (200k, Lowers Morale) [cite: 116]"
        ])
        st.subheader("Decision 2: Training Strategy")
        q2 = st.radio("Format:", [
            "Comprehensive On-Site (125k, High Competency) [cite: 119]",
            "Online Modules (75k, Lower Engagement) [cite: 120]"
        ])
        cost = (100000 if "Redeployment" in q1 else 200000) + (125000 if "On-Site" in q2 else 75000)

    # TEAM 6: TRANSFORMATION (Risk) [Derived from Source 46, 510]
    elif "Team 6" in role:
        st.info("**Mission:** Risk Management and Contingency Planning.")
        st.subheader("Decision 1: Contingency Fund")
        q1 = st.radio("Allocation:", [
            "Secure 10% of Budget for Unknowns (Safe)",
            "Maximize Operational Spend (Risky)"
        ])
        st.subheader("Decision 2: Scenario Planning")
        q2 = st.radio("Primary Fear:", [
            "Vendor Delays [cite: 511]",
            "Data Breach [cite: 528]"
        ])
        cost = 0

    # TEAM 7: COMMS (PR) [Derived from Source 122]
    elif "Team 7" in role:
        st.info("**Mission:** Manage Internal and External messaging.")
        st.subheader("Decision 1: Internal Message")
        q1 = st.radio("Tone:", [
            "Transparent: 'Jobs will change.' (Trust)",
            "Reassuring: 'No one loses a job.' (Risky if untrue)"
        ])
        st.subheader("Decision 2: Customer Launch")
        q2 = st.radio("Campaign:", [
            "Digital Only (Low Cost)",
            "In-Store Ambassadors (High Cost/High Adoption)"
        ])
        cost = 10000 # Estimated

    # --- SUBMIT LOGIC ---
    st.divider()
    if st.button("Submit Decisions"):
        # In a real app, this uses GSheet API. For this demo, we simulate success.
        # To make this actually write to the sheet, you need the Google API setup.
        # Since you are non-coder, we will display the instruction:
        
        st.success("Decisions Submitted to Professor!")
        st.write(f"**Log:** {role} selected '{q1}' and '{q2}'. Cost: {cost}")
        st.info("📝 *Note for Professor: To make this write to the real Sheet automatically, you need to enable the Google Drive API. For now, students can screenshot this page.*")
        
        # Display Change Management Insight
        st.markdown("### 🧠 Change Management Concept")
        if "Team 1" in role or "Team 3" in role:
            st.write("**Theory: Lewin's Force Field Analysis.** You are deciding on the 'Driving Forces' (Efficiency, ROI) vs 'Restraining Forces' (Cost, Complexity).")
        elif "Team 5" in role or "Team 7" in role:
            st.write("**Theory: ADKAR Model (Awareness/Desire).** Your decisions directly impact the 'People' side of change. Cheap training fails to build 'Ability'.")
        elif "Team 4" in role or "Team 6" in role:
            st.write("**Theory: Kotter's Risk Analysis.** Ignoring barriers (like accessibility) allows complacency, which can derail the 'Refreezing' stage.")
