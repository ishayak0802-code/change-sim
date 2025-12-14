import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION ---
# Replace this with your Google Sheet URL from Step 1
SHEET_URL = https://docs.google.com/spreadsheets/d/1faVJ-Cf7o6b-29KeGOkV9PsK9OptUjXDtJxkg5G7YAQ/edit?usp=sharing
ADMIN_PASSWORD = "teach"  # Password for you to see the dashboard

st.set_page_config(page_title="LSH Change Sim", layout="wide")

# --- HELPER FUNCTIONS ---
def get_data():
    """Reads the Google Sheet data for the Master View"""
    try:
        # Trick to read Google Sheet as CSV
        csv_url = SHEET_URL.replace('/edit?usp=sharing', '/export?format=csv')
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame(columns=["Team", "Round", "Budget", "Morale", "ROI", "Last_Decision"])

# --- SIDEBAR LOGIN ---
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="Ludowa Sieć Handlowa") # You can replace with LSH logo URL
    st.title("🛒 LSH Sim 2020")
    
    user_type = st.radio("Login As:", ["Student Team", "Professor"])
    
    if user_type == "Student Team":
        team_name = st.text_input("Enter Team Name (e.g., Team Alpha)")
        if st.button("Reset / Restart"):
            st.session_state.clear()
            st.rerun()
    else:
        pwd = st.text_input("Admin Password", type="password")
        team_name = "ADMIN"

# --- MASTER VIEW (PROFESSOR) ---
if user_type == "Professor":
    if pwd == ADMIN_PASSWORD:
        st.header("👨‍🏫 Master Dashboard: Real-Time Results")
        if st.button("Refresh Data"):
            st.rerun()
        
        # In a real deployed app with a database, this would pull live data. 
        # For this simulation without a complex DB setup, we will view the concepts.
        st.info("In the fully deployed version, this table shows live student inputs from the connected database.")
        
        # Simulation of what you would see:
        dummy_data = pd.DataFrame({
            "Team": ["Team Alpha", "Team Beta", "Team Gamma"],
            "Round": ["Refreeze", "Change", "Unfreeze"],
            "Budget Rem": ["250,000", "800,000", "950,000"],
            "Morale": ["Low (Crisis)", "High", "Neutral"],
            "Strategy": ["Big Bang", "Phased", "Pending"]
        })
        st.dataframe(dummy_data, use_container_width=True)
        
        st.subheader("Class Discussion Prompts")
        st.markdown("""
        * **For Teams with Low Morale:** "Why did the 'Big Bang' approach cause panic in your workforce?" (Link to *Lewin's Unfreeze*)
        * **For Teams with High Costs:** "Was the expensive training worth the ROI?" (Link to *ADKAR Ability*)
        """)
    else:
        st.error("Incorrect Password")
    st.stop()

# --- STUDENT SIMULATION LOGIC ---

if not team_name:
    st.warning("Please enter a Team Name in the sidebar to begin.")
    st.stop()

# Initialize State (LSH Context 2020)
if 'round' not in st.session_state:
    st.session_state['round'] = 1
    st.session_state['budget'] = 1000000  # 1 Million Zloty [cite: 47]
    st.session_state['morale'] = 60       # Base morale
    st.session_state['roi'] = 0           # Projected ROI
    st.session_state['adoption'] = 0
    st.session_state['history'] = []

# METRICS DISPLAY
col1, col2, col3, col4 = st.columns(4)
col1.metric("Budget (Zloty)", f"{st.session_state['budget']:,}")
col2.metric("Staff Morale", f"{st.session_state['morale']}/100")
col3.metric("Adoption %", f"{st.session_state['adoption']}%")
col4.metric("Current Round", st.session_state['round'])

# --- ROUND 1: UNFREEZE (Strategy) ---
if st.session_state['round'] == 1:
    st.header("Round 1: Strategy & Unfreezing")
    st.markdown("""
    **Context:** It is 2020. LSH has 2000 stores. You have 1M Zloty. 
    Foreign competitors (Lidl/Aldi) are pressuring you. You must modernize. [cite: 480]
    
    **Theory (Kotter):** You must establish a sense of urgency without creating panic.
    """)
    
    st.subheader("Decision 1: The Rollout Strategy ")
    rollout = st.radio("Choose your approach:", [
        "A. One-Time 'Big Bang' (All 2000 stores in 6 months)",
        "B. Two-Phase Rollout (500 stores now, 1500 later)"
    ])
    
    st.subheader("Decision 2: Vendor Selection [cite: 460]")
    vendor = st.radio("Select Vendor:", [
        "A. Single Vendor (300k Zloty - Fast, Rigid)",
        "B. Multi-Vendor (400k Zloty - Flexible, Complex)"
    ])
    
    if st.button("Submit Round 1"):
        # Calc Impacts
        cost = 0
        if "Big Bang" in rollout:
            cost += 0 # Operational strain hidden cost
            st.session_state['morale'] -= 15 # High panic
            st.session_state['roi'] += 20    # Faster ROI
            msg = "Result: The 'Big Bang' created panic! Morale dropped, but financial projections look good."
        else:
            st.session_state['morale'] += 5  # Staff feels safer
            st.session_state['roi'] -= 10    # Slower ROI
            msg = "Result: Phased approach calmed the staff. Slower financial returns."

        if "Single" in vendor:
            cost += 300000
        else:
            cost += 400000
            
        st.session_state['budget'] -= cost
        st.session_state['history'].append(f"R1: {rollout} | {vendor}")
        st.success(msg)
        st.session_state['round'] = 2
        st.rerun()

# --- ROUND 2: CHANGE (Execution) ---
elif st.session_state['round'] == 2:
    st.header("Round 2: The Implementation (Change)")
    st.markdown("""
    **Context:** Machines are arriving. Staff fears job losses. [cite: 322]
    
    **Theory (Lewin - Movement):** You need to support the change with training and remove obstacles (accessibility).
    """)
    
    st.subheader("Decision 3: Training Strategy ")
    training = st.radio("How will you train 25,000 employees?", [
        "A. Online Modules (Cost: 75k Zloty - Low Engagement)",
        "B. Comprehensive On-Site (Cost: 125k Zloty - High Competency)"
    ])
    
    st.subheader("Decision 4: Accessibility Compliance ")
    access = st.radio("Legal Check - Accessibility Law X:", [
        "A. Minimum Compliance (Cost: 20k Zloty - Risk of Fines)",
        "B. High-End Compliance (Cost: 50k Zloty - No Risk)"
    ])
    
    if st.button("Submit Round 2"):
        cost = 0
        
        # Training Logic
        if "Online" in training:
            cost += 75000
            st.session_state['morale'] -= 10
            st.session_state['adoption'] += 20
            st.warning("Staff are confused by the online videos. Adoption is slow.")
        else:
            cost += 125000
            st.session_state['morale'] += 10
            st.session_state['adoption'] += 50
            st.success("On-site training was a hit! Staff feel confident.")

        # Accessibility Logic
        if "Minimum" in access:
            cost += 20000
            # Hidden risk flag for Round 3
            st.session_state['risk_flag'] = True
        else:
            cost += 50000
            st.session_state['risk_flag'] = False
            
        st.session_state['budget'] -= cost
        st.session_state['history'].append(f"R2: {training} | {access}")
        st.session_state['round'] = 3
        st.rerun()

# --- ROUND 3: REFREEZE (Scenarios) ---
elif st.session_state['round'] == 3:
    st.header("Round 3: Emerging Scenarios (Refreeze)")
    st.markdown("""
    **Theory (ADKAR - Reinforcement):** To make change stick, you must solve immediate problems effectively.
    """)
    
    # Scenario Generation
    scenario = random.choice(["Data Breach", "Vendor Delay", "Accessibility Complaint"])
    
    # Force Accessibility Complaint if they chose Minimum Compliance
    if st.session_state.get('risk_flag') == True:
        scenario = "Accessibility Complaint"
        
    st.error(f"ALERT: {scenario} Detected!")
    
    if scenario == "Data Breach":
        st.write("Description: A customer reports unauthorized charges. GDPR violation risk. [cite: 103]")
        choice = st.radio("Response:", ["A. Pause Rollout (Safety first)", "B. Ignore & Patch later"])
    elif scenario == "Vendor Delay":
        st.write("Description: Hardware is 2 months late. [cite: 86]")
        choice = st.radio("Response:", ["A. Wait (Idle resources)", "B. Switch Vendor (High Cost)"])
    elif scenario == "Accessibility Complaint":
        st.write("Description: Customers with disabilities threaten lawsuit. [cite: 96]")
        st.write("Note: This happened because of Low Compliance choice in R2.")
        choice = st.radio("Response:", ["A. Retrofit Immediately (Expensive)", "B. Fight in Court"])

    if st.button("Finalize Simulation"):
        # Apply penalties based on scenario
        if scenario == "Accessibility Complaint":
            st.session_state['budget'] -= 100000 # Fine + Retrofit cost
            st.session_state['morale'] -= 20
        elif scenario == "Data Breach" and "Pause" in choice:
            st.session_state['roi'] -= 10
            st.session_state['morale'] += 5 # Staff appreciates safety
        
        st.session_state['round'] = 4
        st.rerun()

# --- RESULTS SUMMARY ---
elif st.session_state['round'] == 4:
    st.header("🏁 Simulation Complete")
    
    final_score = st.session_state['roi'] + st.session_state['adoption'] + (st.session_state['morale']/2)
    
    if st.session_state['budget'] < 0:
        st.error(f"BANKRUPT: You overspent by {-st.session_state['budget']} Zloty.")
    else:
        st.success(f"Final Budget Remaining: {st.session_state['budget']:,} Zloty")
    
    st.metric("Final Change Effectiveness Score", f"{final_score:.0f}/200")
    
    st.subheader("Your Decision Path")
    for step in st.session_state['history']:
        st.text(step)
        
    st.markdown("---")
    st.info("Take a screenshot of this page for your professor.")
