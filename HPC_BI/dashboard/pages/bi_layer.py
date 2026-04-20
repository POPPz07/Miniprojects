"""
BI Layer Page
Show business insights clearly
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


def load_bi_data():
    """Load BI results"""
    data = {}
    
    # RFM analysis
    rfm_path = Path('../data/rfm_analysis.csv')
    if rfm_path.exists():
        data['rfm'] = pd.read_csv(rfm_path)
    
    # Revenue by segment
    segment_path = Path('../data/eda_revenue_by_segment.csv')
    if segment_path.exists():
        data['revenue_segment'] = pd.read_csv(segment_path)
    
    # Revenue by month
    month_path = Path('../data/eda_revenue_by_month.csv')
    if month_path.exists():
        data['revenue_month'] = pd.read_csv(month_path)
    
    # Top customers
    top_path = Path('../data/eda_top_customers.csv')
    if top_path.exists():
        data['top_customers'] = pd.read_csv(top_path)
    
    # Outliers
    outlier_path = Path('../data/eda_outliers.csv')
    if outlier_path.exists():
        data['outliers'] = pd.read_csv(outlier_path)
    
    # Clean data
    clean_path = Path('../data/clean_data.csv')
    if clean_path.exists():
        data['clean'] = pd.read_csv(clean_path)
    
    return data


def render():
    """Render BI Layer page"""
    
    # Title
    st.title("💼 BI Layer: Business Intelligence")
    st.markdown("**Transforming data into actionable business insights**")
    st.markdown("---")
    
    # Load data
    data = load_bi_data()
    
    # Role of BI
    st.header("🎯 What Does BI Do?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **BI (Business Intelligence) handles:**
        
        1. **Data Preparation**
           - Cleans and validates raw data
           - Handles missing values and outliers
           - Creates derived features
        
        2. **Customer Segmentation**
           - RFM Analysis (Recency, Frequency, Monetary)
           - Groups customers by behavior
           - Identifies high-value segments
        
        3. **Insight Generation**
           - Revenue patterns and trends
           - Customer behavior analysis
           - Actionable recommendations
        """)
    
    with col2:
        st.info("""
        **Technology:**
        - Language: Python
        - Libraries: pandas, scikit-learn
        - Approach: Data analytics & ML
        """)
    
    st.markdown("---")
    
    # KPI Row
    st.header("📊 BI Performance Metrics")
    
    if 'clean' in data and 'rfm' in data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            clean_records = len(data['clean'])
            st.metric(
                "📦 Clean Records",
                f"{clean_records:,}",
                help="Records after data cleaning"
            )
        
        with col2:
            total_customers = len(data['rfm'])
            st.metric(
                "👥 Total Customers",
                f"{total_customers:,}",
                help="Unique customers analyzed"
            )
        
        with col3:
            segments = data['rfm']['Segment'].nunique()
            st.metric(
                "🎯 RFM Segments",
                f"{segments}",
                help="Customer segments identified"
            )
        
        with col4:
            if 'outliers' in data:
                outlier_types = len(data['outliers'])
                st.metric(
                    "⚠️ Outlier Types",
                    f"{outlier_types}",
                    help="Types of outliers detected"
                )
    
    st.markdown("---")
    
    # RFM Segmentation
    st.header("👥 Customer Segmentation (RFM Analysis)")
    
    st.markdown("**Understanding customer value through Recency, Frequency, and Monetary analysis**")
    
    if 'rfm' in data:
        rfm_df = data['rfm']
        
        # Segment distribution
        segment_counts = rfm_df['Segment'].value_counts().reset_index()
        segment_counts.columns = ['Segment', 'Count']
        segment_counts['Percentage'] = (segment_counts['Count'] / len(rfm_df)) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart
            fig = px.bar(
                segment_counts,
                x='Segment',
                y='Count',
                title='Customer Distribution by Segment',
                text='Percentage',
                color='Count',
                color_continuous_scale='Greens'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Segment descriptions
            st.markdown("""
            **Segment Definitions:**
            
            - **Champions**: Best customers (high R, F, M)
            - **Loyal Customers**: Regular buyers
            - **Potential Loyalists**: Recent customers
            - **At Risk**: Declining engagement
            - **Lost**: Churned customers
            - **Other**: Mixed behavior
            """)
        
        # Key Insight
        champions = segment_counts[segment_counts['Segment'] == 'Champions']
        if len(champions) > 0:
            champ_pct = champions['Percentage'].values[0]
            st.success(f"""
            **💡 Key Insight:** **Champions** represent **{champ_pct:.1f}%** of customers. 
            Focus retention efforts on this high-value segment.
            """)
    
    st.markdown("---")
    
    # Revenue Analysis
    st.header("💰 Revenue Analysis by Segment")
    
    if 'revenue_segment' in data:
        revenue_df = data['revenue_segment']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue by segment
            fig = px.bar(
                revenue_df,
                x='Segment',
                y='total_revenue',
                title='Revenue Contribution by Segment',
                text='percentage',
                color='total_revenue',
                color_continuous_scale='Greens'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(height=400, yaxis_title='Revenue ($)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top segment
            top_segment = revenue_df.loc[revenue_df['total_revenue'].idxmax()]
            st.metric(
                f"🏆 Top Segment: {top_segment['Segment']}",
                f"${top_segment['total_revenue']:,.0f}",
                f"{top_segment['percentage']:.1f}% of total"
            )
            
            st.markdown("""
            **Revenue Concentration:**
            
            High revenue concentration in top segments indicates:
            - Strong customer loyalty
            - Effective targeting opportunities
            - Risk if top customers churn
            """)
        
        # Key Insight
        st.info(f"""
        **💡 Key Insight:** **{top_segment['Segment']}** drives **{top_segment['percentage']:.1f}%** 
        of total revenue. Prioritize retention strategies for this segment.
        """)
    
    st.markdown("---")
    
    # Temporal Trends
    st.header("📈 Revenue Trends Over Time")
    
    if 'revenue_month' in data:
        month_df = data['revenue_month']
        
        # Line chart
        fig = px.line(
            month_df,
            x='year_month',
            y='total_revenue',
            title='Monthly Revenue Trend',
            markers=True
        )
        fig.update_layout(
            height=400,
            xaxis_title='Month',
            yaxis_title='Revenue ($)'
        )
        fig.update_traces(line_color='#2ca02c', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
        
        # Key Insight
        peak_month = month_df.loc[month_df['total_revenue'].idxmax()]
        st.success(f"""
        **💡 Key Insight:** Peak revenue in **{peak_month['year_month']}** 
        (${peak_month['total_revenue']:,.0f}). Analyze this period for successful strategies.
        """)
    
    st.markdown("---")
    
    # Top Customers
    st.header("🏆 Top 10 Customers by Spend")
    
    if 'top_customers' in data:
        top_df = data['top_customers'].head(10)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart
            fig = px.bar(
                top_df,
                x='CustomerID',
                y='total_spend',
                title='Top 10 Customers by Total Spend',
                color='total_spend',
                color_continuous_scale='Greens'
            )
            fig.update_layout(height=400, yaxis_title='Total Spend ($)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Summary stats
            top_10_revenue = top_df['total_spend'].sum()
            if 'clean' in data:
                total_revenue = data['clean']['TotalPrice'].sum()
                top_10_pct = (top_10_revenue / total_revenue) * 100
                
                st.metric(
                    "💰 Top 10 Revenue",
                    f"${top_10_revenue:,.0f}",
                    f"{top_10_pct:.1f}% of total"
                )
            
            st.markdown("""
            **VIP Customer Strategy:**
            
            - Dedicated account management
            - Exclusive offers and rewards
            - Proactive engagement
            - Churn prevention monitoring
            """)
    
    st.markdown("---")
    
    # Outlier Analysis
    st.header("⚠️ Outlier Detection")
    
    if 'outliers' in data:
        outliers_df = data['outliers']
        
        st.markdown("**Identifying unusual patterns that require attention**")
        
        for _, outlier in outliers_df.iterrows():
            with st.expander(f"📌 {outlier['outlier_type'].replace('_', ' ').title()} ({int(outlier['count'])} cases)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **Details:**
                    - **Count**: {int(outlier['count'])} transactions
                    - **Total Value**: ${outlier['total_value']:,.2f}
                    - **Reason**: {outlier['reason']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Business Impact:**
                    {outlier['impact']}
                    
                    **Recommended Action:**
                    {outlier['action']}
                    """)
    
    st.markdown("---")
    
    # Key Takeaway
    st.header("🎯 Key Takeaway")
    
    st.info("""
    **BI transforms raw data into actionable decisions:**
    
    ✅ **Customer Understanding**: RFM segmentation reveals customer value
    
    ✅ **Revenue Insights**: Identify high-performing segments and periods
    
    ✅ **Trend Analysis**: Spot patterns and opportunities
    
    ✅ **Risk Detection**: Outliers highlight potential issues or opportunities
    """)
    
    # Technical Note (expandable)
    with st.expander("🔬 Technical Details (Optional)"):
        st.markdown("""
        **Data Processing Pipeline:**
        1. **Data Cleaning**: Remove missing values, handle outliers
        2. **Feature Engineering**: Create RFM scores, time-based features
        3. **Segmentation**: Apply business rules for customer grouping
        4. **Analysis**: Generate insights and recommendations
        
        **RFM Scoring:**
        - **Recency**: Days since last purchase (1-5 scale)
        - **Frequency**: Number of purchases (1-5 scale)
        - **Monetary**: Total spend (1-5 scale)
        - **Segment**: Combined RFM score determines segment
        
        **Machine Learning (Supporting Role):**
        - Classification: Predict high-value customers (95% accuracy)
        - Clustering: Validate RFM segments (silhouette score: 0.90)
        """)
