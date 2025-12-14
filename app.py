import streamlit as st
import pandas as pd
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Change Management Sim", layout="centered")

# --- GAME STATE ---
if 'morale' not in st.session_state:
    st.session_state['morale'] = 50  # Start at 50%
if 'adoption' not in st.session_state:
    st.session_state['adoption'] = 0   # Start at 0% implementation
if 'budget' not in st.session_state:
    st.session_state['budget'] = 100000
if 'round' not in st.session_state:
    st.session_state['round'] = 1

# --- SIDEBAR ---
with st.sidebar:
    st.header("Team Dashboard")
    team_name = st.text_input("Enter Team Name")
    st.divider()
    st.metric("Budget", f"${st.session_state['budget']:,}")
    st.metric("Employee Morale", f"{st.session_state['morale']}%")
    st.metric("Tech Adoption", f"{st.session_state['adoption']}%")
    
    if st.button("Reset Simulation"):
        st.session_state.clear()
        st.rerun()

st.title("🛒 Retail Change Simulation: Project Checkout")
st.markdown("You are the Change Management leads for a Polish retail giant. Your goal: Implement self-checkouts without causing a strike.")

# --- SCENARIO ENGINE ---

# ROUND 1: UNFREEZE (Preparing the Org)
if st.session_state['round'] == 1:
    st.header("Round 1: The Announcement (Unfreeze)")
    st.info("Context: Rumors are spreading that robots will replace cashiers. Anxiety is high.")
    
    st.subheader("Decision: How do you announce the change?")
    
    decision = st.radio("Choose your strategy:", [
        "A. Top-Down Email: 'This is necessary for survival.' (Cost: $0)",
        "B. Town Hall: Open Q&A and vision sharing. (Cost: $5,000)",
        "C. Secret Pilot: Install quietly in one store first. (Cost: $10,000)"
    ])
    
    if st.button("Submit Decision"):
        if not team_name:
            st.error("Please enter a team name in the sidebar!")
        else:
            # LOGIC ENGINE
            if "A." in decision:
                impact_msg = "Result: Efficiency is clear, but panic spreads. Morale drops significantly."
                st.session_state['morale'] -= 15
                st.session_state['adoption'] += 5
            elif "B." in decision:
                impact_msg = "Result: Staff feels heard. Some are skeptical, but panic subsides."
                st.session_state['morale'] += 5
                st.session_state['budget'] -= 5000
                st.session_state['adoption'] += 5
            elif "C." in decision:
                impact_msg = "Result: Rumors get worse because of the secrecy. Union leaders are angry."
                st.session_state['morale'] -= 20
                st.session_state['budget'] -= 10000
                st.session_state['adoption'] += 10
            
            st.success(impact_msg)
            st.session_state['round'] = 2
            st.rerun()

# ROUND 2: CHANGE (Implementation)
elif st.session_state['round'] == 2:
    st.header("Round 2: The Rollout (Change)")
    st.info("Context: The machines are arriving. Older staff are struggling to learn the interface.")
    
    st.subheader("Decision: How do you support the staff?")
    
    decision = st.radio("Choose your strategy:", [
        "A. Sink or Swim: They will learn on the job. (Cost: $0)",
        "B. Peer Training: Appoint 'Digital Champions' from staff. (Cost: $2,000)",
        "C. External Consultants: Hired trainers for a week. (Cost: $15,000)"
    ])
    
    if st.button("Submit Decision"):
        if "A." in decision:
            st.session_state['morale'] -= 10
            st.session_state['adoption'] += 5
        elif "B." in decision:
            st.session_state['morale'] += 10
            st.session_state['budget'] -= 2000
            st.session_state['adoption'] += 20
        elif "C." in decision:
            st.session_state['morale'] += 0
            st.session_state['budget'] -= 15000
            st.session_state['adoption'] += 40
            
        st.session_state['round'] = 3
        st.rerun()

# ROUND 3: REFREEZE (Sustaining)
elif st.session_state['round'] == 3:
    st.header("Round 3: The New Normal (Refreeze)")
    st.write(f"Final Morale: {st.session_state['morale']}%")
    st.write(f"Final Adoption: {st.session_state['adoption']}%")
    st.write(f"Remaining Budget: ${st.session_state['budget']}")
    
    if st.session_state['morale'] < 40:
        st.error("outcome: The union went on strike. The project succeeded technically, but failed culturally.")
    elif st.session_state['adoption'] > 30 and st.session_state['morale'] >= 40:
        st.balloons()
        st.success("Outcome: Successful transformation! You balanced people and profit.")
    else:
        st.warning("Outcome: Stalled. The tech is there, but no one is using it.")
