"""
HPC + BI Retail Analytics Dashboard
Clean, concise, and explainable interface
"""

import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="HPC + BI Retail Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean design
st.markdown("""
<style>
    /* Global styling */
    .main {
        padding: 2rem;
    }
    
    /* Card styling */
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    
    /* Color scheme */
    .hpc-color { color: #1f77b4; }  /* Blue */
    .bi-color { color: #2ca02c; }   /* Green */
    .validation-color { color: #9467bd; }  /* Purple */
    
    /* Section headers */
    h1 { color: #1f1f1f; font-size: 2.5rem; }
    h2 { color: #1f77b4; font-size: 2rem; margin-top: 2rem; }
    h3 { color: #2ca02c; font-size: 1.5rem; }
    
    /* Insight boxes */
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application"""
    
    # Sidebar navigation
    st.sidebar.title("🚀 Navigation")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Select Page:",
        [
            "📊 Overview",
            "⚡ HPC Engine",
            "💼 BI Layer",
            "🔗 System Integration",
            "🎯 Results & Impact"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### About
    **HPC + BI Retail Analytics**
    
    Combining high-performance computing with business intelligence for fast, accurate insights.
    """)
    
    # Route to pages
    if page == "📊 Overview":
        from pages import overview
        overview.render()
    elif page == "⚡ HPC Engine":
        from pages import hpc_engine
        hpc_engine.render()
    elif page == "💼 BI Layer":
        from pages import bi_layer
        bi_layer.render()
    elif page == "🔗 System Integration":
        from pages import system_integration
        system_integration.render()
    elif page == "🎯 Results & Impact":
        from pages import results_impact
        results_impact.render()

if __name__ == "__main__":
    main()
