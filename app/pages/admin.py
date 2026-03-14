# Admin Page
import sys
import os
import streamlit as st
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from src.database import Database

# Initialize database
db = Database()
db.connect()

st.title("⚙️ Admin Panel")

# Check admin
if not st.session_state.user.get('is_admin'):
    st.error("🚫 Access Denied. Admin privileges required.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["📈 Analytics", "👥 Users", "🍽️ Foods"])

with tab1:
    st.subheader("📈 System Analytics")
    
    cursor = db.conn.cursor()
    
    # Stats
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM predictions")
    active_users = cursor.fetchone()[0]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Users", total_users)
    col2.metric("Total Predictions", total_predictions)
    col3.metric("Active Users", active_users)
    col4.metric("Avg Accuracy", "94.5%")
    
    st.divider()
    
    # Popular foods
    st.subheader("🍕 Popular Foods")
    cursor.execute("""
        SELECT predicted_class, COUNT(*) as count
        FROM predictions 
        WHERE predicted_class IS NOT NULL
        GROUP BY predicted_class 
        ORDER BY count DESC 
        LIMIT 10
    """)
    popular_foods = cursor.fetchall()
    
    if popular_foods:
        food_data = {
            'Food': [f[0] for f in popular_foods],
            'Scans': [f[1] for f in popular_foods]
        }
        df = pd.DataFrame(food_data)
        st.dataframe(df, width=600, hide_index=True)
    else:
        st.info("No prediction data available yet.")

with tab2:
    st.subheader("👥 User Management")
    
    cursor.execute("""
        SELECT id, username, email, is_admin, is_active, created_at
        FROM users
        ORDER BY created_at DESC
    """)
    users = cursor.fetchall()
    
    if users:
        users_data = {
            'ID': [u[0] for u in users],
            'Username': [u[1] for u in users],
            'Email': [u[2] for u in users],
            'Admin': ['✅' if u[3] else '❌' for u in users],
            'Status': ['Active' if u[4] else 'Inactive' for u in users],
            'Joined': [u[5][:10] if u[5] else 'N/A' for u in users]
        }
        
        df = pd.DataFrame(users_data)
        st.dataframe(df, width=800, hide_index=True)
        st.info(f"📊 Total Users: {len(users)}")
    else:
        st.warning("No users found.")

with tab3:
    st.subheader("🍽️ Food Database Management")
    
    all_foods = db.get_all_foods()
    
    if all_foods:
        foods_data = {
            'ID': [f['id'] for f in all_foods],
            'Name': [f['name'] for f in all_foods],
            'Category': [f['category'] for f in all_foods],
            'Calories': [int(f['calories']) for f in all_foods],
            'Region': [f['region'] for f in all_foods]
        }
        
        df = pd.DataFrame(foods_data)
        st.dataframe(df, width=800, hide_index=True)
        st.info(f"📊 Total Foods: {len(all_foods)}")

db.close()
