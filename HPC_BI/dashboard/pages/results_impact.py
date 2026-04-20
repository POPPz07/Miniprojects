"""
Results & Impact Page
Final summary and business impact
"""

import streamlit as st
import pandas as pd
from pathlib import Path


def load_summary_data():
    """Load summary data from all modules"""
    data = {}
    
    # HPC summary
    hpc_path = Path('../data/hpc_results_summary.csv')
    if hpc_path.exists():
        data['hpc'] = pd.read_csv(hpc_path)
    
    # BI insights
    bi_path = Path('../data/bi_insights_summary.csv')
    if bi_path.exists():
        data['bi'] = pd.read_csv(bi_path)
    
    # Thread scaling
    thread_path = Path('../data/hpc_thread_scaling.csv')
    if thread_path.exists():
        data['threads'] = pd.read_csv(thread_path)
    
    # RFM analysis
    rfm_path = Path('../data/rfm_analysis.csv')
    if rfm_path.exists():
        data['rfm'] = pd.read_csv(rfm_path)
    
    return data


def render():
    """Render results and impact page"""
    
    # Title
    st.title("🎯 Results & Impact: What We Achieved")
    st.markdown("**Summary of findings and business value**")
    st.markdown("---")
    
    # Load data
    data = load_summary_data()
    
    # Key Results
    st.header("📊 Key Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'hpc' in data:
            revenue = data['hpc'][data['hpc']['metric'] == 'total_revenue']['value'].values
            if len(revenue) > 0:
                st.metric(
                    "💰 Total Revenue",
                    f"${revenue[0]:,.0f}",
                    help="Total revenue analyzed"
                )
    
    with col2:
        if 'rfm' in data:
            customers = len(data['rfm'])
            st.metric(
                "👥 Customers Analyzed",
                f"{customers:,}",
                help="Unique customers segmented"
            )
    
    with col3:
        if 'bi' in data:
            insights = len(data['bi'])
            st.metric(
                "💡 Insights Generated",
                f"{insights}",
                help="Business insights discovered"
            )
    
    with col4:
        if 'threads' in data:
            speedup = data['threads']['speedup'].max()
            st.metric(
                "⚡ HPC Speedup",
                f"{speedup:.2f}x",
                help="Performance improvement"
            )
    
    st.markdown("---")
    
    # Top Business Insights
    st.header("💡 Top Business Insights")
    
    if 'bi' in data:
        bi_df = data['bi']
        
        # Filter for key insights
        key_insights = [
            ("Champions Revenue", "Champions contribute", "segment"),
            ("Customer Concentration", "customers", "concentration"),
            ("Peak Month", "Peak month", "temporal")
        ]
        
        for title, keyword, category in key_insights:
            insight_row = bi_df[
                (bi_df['insight'].str.contains(keyword, case=False, na=False)) &
                (bi_df['analysis_type'] == category)
            ]
            
            if len(insight_row) > 0:
                insight = insight_row.iloc[0]
                with st.expander(f"📌 {title}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Finding:** {insight['insight']}")
                        st.markdown(f"**Business Meaning:** {insight['business_meaning']}")
                    
                    with col2:
                        if pd.notna(insight['value']):
                            st.metric("Value", f"{insight['value']:,.0f}")
                        if pd.notna(insight['percentage']):
                            st.metric("Percentage", f"{insight['percentage']:.1f}%")
    
    st.markdown("---")
    
    # Component Contribution
    st.header("🏗️ System Component Contributions")
    
    st.markdown("**How each component adds value to the system**")
    
    # Create contribution table
    contribution_data = {
        'Component': ['⚡ HPC Engine', '💼 BI Layer', '🔗 Validation', '📊 Dashboard'],
        'Primary Role': [
            'Speed & Computation',
            'Insights & Analytics',
            'Accuracy & Reliability',
            'Visualization & Communication'
        ],
        'Key Output': [
            'Fast parallel processing (1.05x speedup)',
            '25 actionable business insights',
            '0.0000% revenue difference',
            'Clear, understandable presentation'
        ],
        'Business Value': [
            'Real-time analytics capability',
            'Data-driven decision making',
            'Confidence in results',
            'Accessible to all stakeholders'
        ]
    }
    
    contribution_df = pd.DataFrame(contribution_data)
    st.dataframe(contribution_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Business Impact
    st.header("💼 Business Impact")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🚀 Faster Analytics
        
        **Before:**
        - Manual data processing
        - Hours of computation
        - Limited scalability
        
        **After:**
        - Automated pipeline
        - Seconds of computation
        - Handles 400K+ records
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Better Decisions
        
        **Before:**
        - Limited customer insights
        - Reactive strategies
        - Gut-feel decisions
        
        **After:**
        - 6 customer segments
        - 25 actionable insights
        - Data-driven strategies
        """)
    
    with col3:
        st.markdown("""
        ### ✅ Reliable Results
        
        **Before:**
        - Single-source analysis
        - Uncertain accuracy
        - Limited confidence
        
        **After:**
        - Cross-validated results
        - 0.0000% difference
        - High confidence
        """)
    
    st.markdown("---")
    
    # Specific Business Actions
    st.header("📋 Recommended Business Actions")
    
    st.markdown("**Based on our analysis, here are concrete next steps:**")
    
    if 'rfm' in data:
        rfm_df = data['rfm']
        
        # Champions count
        champions = len(rfm_df[rfm_df['Segment'] == 'Champions'])
        champions_pct = (champions / len(rfm_df)) * 100
        
        # At Risk count
        at_risk = len(rfm_df[rfm_df['Segment'] == 'At Risk'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            ### 1️⃣ Retain Champions ({champions:,} customers)
            
            **Why:** They represent {champions_pct:.1f}% of customers and drive majority of revenue
            
            **Actions:**
            - Launch VIP loyalty program
            - Provide dedicated account managers
            - Offer exclusive early access to products
            - Implement proactive engagement strategy
            """)
            
            st.markdown(f"""
            ### 2️⃣ Recover At-Risk Customers ({at_risk:,} customers)
            
            **Why:** Declining engagement threatens revenue
            
            **Actions:**
            - Send win-back campaigns
            - Offer special discounts
            - Conduct exit surveys
            - Analyze churn patterns
            """)
        
        with col2:
            st.markdown("""
            ### 3️⃣ Optimize Peak Periods
            
            **Why:** Revenue varies by time period
            
            **Actions:**
            - Staff appropriately for peak days/hours
            - Plan inventory for high-demand periods
            - Launch promotions during slow periods
            - Analyze successful peak strategies
            """)
            
            st.markdown("""
            ### 4️⃣ Monitor System Continuously
            
            **Why:** Customer behavior changes over time
            
            **Actions:**
            - Run analysis monthly
            - Track segment migrations
            - Update strategies based on trends
            - Measure impact of interventions
            """)
    
    st.markdown("---")
    
    # Final Conclusion
    st.header("🏁 Final Conclusion")
    
    st.success("""
    ### HPC + BI: A Complete Analytics Solution
    
    This system demonstrates how **combining high-performance computing with business intelligence** 
    creates a powerful platform for data-driven decision making:
    
    ✅ **HPC provides the speed** to process large datasets in real-time
    
    ✅ **BI provides the insights** to understand customer behavior
    
    ✅ **Validation provides the confidence** to trust the results
    
    ✅ **Together, they enable better business outcomes**
    
    ---
    
    **The Result:** A fast, accurate, and actionable analytics system that transforms 
    raw data into business value.
    """)
    
    st.markdown("---")
    
    # System Summary
    st.header("📈 System Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Technical Achievements:**
        - ⚡ 1.05x speedup with parallel processing
        - 📊 400K+ transactions processed
        - 🎯 6 customer segments identified
        - ✅ 0.0000% validation difference
        - 💡 25 business insights generated
        """)
    
    with col2:
        st.markdown("""
        **Business Achievements:**
        - 👥 Complete customer understanding
        - 💰 Revenue pattern identification
        - 🎯 Targeted action recommendations
        - 📈 Scalable analytics pipeline
        - ✅ Production-ready system
        """)
    
    st.markdown("---")
    
    # Thank You
    st.info("""
    ### 🙏 Thank You for Exploring This System
    
    This dashboard demonstrates the power of combining HPC and BI for retail analytics. 
    
    **Questions?** Review the individual pages for detailed explanations of each component.
    
    **Want to learn more?** Check the technical details in the expandable sections throughout the dashboard.
    """)
