"""
BI Insights Page
Business Intelligence analytics and customer insights
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path


def load_bi_data():
    """Load BI results from CSV files"""
    data = {}
    
    # Load insights summary
    insights_path = Path('../data/bi_insights_summary.csv')
    if insights_path.exists():
        data['insights'] = pd.read_csv(insights_path)
    
    # Load RFM analysis
    rfm_path = Path('../data/rfm_analysis.csv')
    if rfm_path.exists():
        data['rfm'] = pd.read_csv(rfm_path)
    
    # Load EDA outputs
    eda_files = {
        'revenue_by_segment': '../data/eda_revenue_by_segment.csv',
        'revenue_by_country': '../data/eda_revenue_by_country.csv',
        'customer_metrics': '../data/eda_customer_metrics.csv',
        'top_customers': '../data/eda_top_customers.csv',
        'revenue_by_dow': '../data/eda_revenue_by_dow.csv',
        'outliers': '../data/eda_outliers.csv'
    }
    
    for key, path in eda_files.items():
        file_path = Path(path)
        if file_path.exists():
            data[key] = pd.read_csv(file_path)
    
    return data


def render_page_header():
    """Render page header"""
    st.title("📊 BI Insights: Customer Analytics & Business Intelligence")
    
    st.markdown("""
    ## Transforming Data into Actionable Business Insights
    
    This page showcases the Business Intelligence layer's analytical capabilities, from customer
    segmentation to revenue analysis and outlier detection.
    
    **What you'll discover:**
    - RFM-based customer segmentation with business meaning
    - Revenue patterns and concentration analysis
    - Temporal trends and seasonality
    - Outlier detection with actionable recommendations
    
    ---
    """)


def render_key_insights(data):
    """Render key business insights"""
    st.header("💡 Key Business Insights")
    
    st.markdown("""
    **What it shows:** Top actionable insights from comprehensive data analysis
    
    **Why it matters:** These insights drive business decisions and strategy
    
    **Key insight:** Data analysis is only valuable when it leads to action
    """)
    
    if 'insights' in data:
        insights_df = data['insights']
        
        # Filter for most impactful insights
        priority_insights = insights_df[
            insights_df['analysis_type'].isin(['segment', 'concentration', 'outlier'])
        ].head(6)
        
        for _, insight in priority_insights.iterrows():
            with st.expander(f"**{insight['analysis_type'].title()}: {insight['dimension']}**"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Insight:** {insight['insight']}")
                    st.info(f"**Business Meaning:** {insight['business_meaning']}")
                
                with col2:
                    if pd.notna(insight.get('value')):
                        st.metric("Value", f"{insight['value']:,.0f}")
                    if pd.notna(insight.get('percentage')):
                        st.metric("Percentage", f"{insight['percentage']:.1f}%")


def render_rfm_segmentation(data):
    """Render RFM segmentation analysis"""
    st.header("👥 RFM Customer Segmentation")
    
    st.markdown("""
    **What it shows:** Customer distribution across RFM segments
    
    **Why it matters:** Different segments require different marketing strategies
    
    **Key insight:** 22% Champions generate 65% of revenue - protect this segment at all costs
    """)
    
    if 'revenue_by_segment' in data:
        segment_df = data['revenue_by_segment']
        
        # Create sunburst chart
        fig = px.sunburst(
            segment_df,
            path=['Segment'],
            values='total_revenue',
            title='Revenue Distribution by RFM Segment',
            color='total_revenue',
            color_continuous_scale='RdYlGn',
            hover_data=['transaction_count']
        )
        fig.update_layout(height=500)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Segment details
        st.subheader("Segment Breakdown")
        
        # Add percentage column
        segment_df['revenue_pct'] = (segment_df['total_revenue'] / segment_df['total_revenue'].sum()) * 100
        
        # Display table
        display_df = segment_df[['Segment', 'total_revenue', 'revenue_pct', 'avg_transaction', 'transaction_count']].copy()
        display_df.columns = ['Segment', 'Total Revenue', 'Revenue %', 'Avg Transaction', 'Transactions']
        display_df['Total Revenue'] = display_df['Total Revenue'].apply(lambda x: f"${x:,.2f}")
        display_df['Revenue %'] = display_df['Revenue %'].apply(lambda x: f"{x:.1f}%")
        display_df['Avg Transaction'] = display_df['Avg Transaction'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Strategic recommendations
        st.subheader("📋 Strategic Recommendations by Segment")
        
        recommendations = {
            'Champions': '🏆 **VIP Treatment:** Dedicated account managers, exclusive offers, early access to new products',
            'Loyal Customers': '💎 **Maintain Engagement:** Regular communication, loyalty rewards, appreciation programs',
            'Potential Loyalists': '🌱 **Convert to Loyal:** Targeted campaigns, incentives for repeat purchases, personalized offers',
            'At Risk': '⚠️ **Immediate Intervention:** Win-back campaigns, special discounts, feedback surveys',
            'Lost': '📉 **Win-Back or Deprioritize:** Analyze churn reasons, targeted re-engagement, or reallocate resources',
            'Other': '🔍 **Further Segmentation:** Analyze behavior patterns, create sub-segments, test strategies'
        }
        
        for segment, recommendation in recommendations.items():
            if segment in segment_df['Segment'].values:
                st.markdown(f"**{segment}:** {recommendation}")


def render_revenue_concentration(data):
    """Render revenue concentration analysis"""
    st.header("📈 Revenue Concentration (Pareto Analysis)")
    
    st.markdown("""
    **What it shows:** How revenue is distributed across the customer base
    
    **Why it matters:** Reveals dependency on key customers and risk concentration
    
    **Key insight:** 5% of customers generate 50% of revenue - high concentration risk
    """)
    
    if 'insights' in data:
        insights_df = data['insights']
        concentration_insights = insights_df[insights_df['dimension'] == 'customer_pareto']
        
        if len(concentration_insights) > 0:
            # Create visualization
            pareto_data = []
            for _, row in concentration_insights.iterrows():
                pareto_data.append({
                    'Threshold': row['segment'],
                    'Customer Count': int(row['value']),
                    'Customer %': row['percentage']
                })
            
            pareto_df = pd.DataFrame(pareto_data)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=pareto_df['Threshold'],
                y=pareto_df['Customer Count'],
                name='Customer Count',
                marker_color='#1f77b4',
                text=pareto_df['Customer %'].apply(lambda x: f"{x:.1f}%"),
                textposition='outside'
            ))
            
            fig.update_layout(
                title='Customer Concentration Analysis',
                xaxis_title='Revenue Threshold',
                yaxis_title='Number of Customers',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.warning("""
            **High Concentration Risk:** A small number of customers drive the majority of revenue.
            
            **Implications:**
            - Loss of a few key customers could significantly impact revenue
            - Diversification strategy needed to reduce dependency
            - Enhanced retention programs for top customers essential
            """)


def render_temporal_trends(data):
    """Render temporal trend analysis"""
    st.header("📅 Temporal Trends & Seasonality")
    
    st.markdown("""
    **What it shows:** Revenue patterns across time dimensions
    
    **Why it matters:** Enables demand forecasting and resource planning
    
    **Key insight:** Thursday is peak day - optimize staffing and inventory accordingly
    """)
    
    if 'revenue_by_dow' in data:
        dow_df = data['revenue_by_dow']
        
        # Day of week chart
        fig = px.bar(
            dow_df,
            x='day_name',
            y='total_revenue',
            title='Revenue by Day of Week',
            color='total_revenue',
            color_continuous_scale='Blues',
            text='total_revenue'
        )
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig.update_layout(
            xaxis_title='Day of Week',
            yaxis_title='Total Revenue ($)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        peak_day = dow_df.loc[dow_df['total_revenue'].idxmax(), 'day_name']
        low_day = dow_df.loc[dow_df['total_revenue'].idxmin(), 'day_name']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"""
            **Peak Day: {peak_day}**
            
            - Ensure adequate staffing
            - Stock high-demand items
            - Optimize system capacity
            """)
        
        with col2:
            st.info(f"""
            **Lowest Day: {low_day}**
            
            - Run promotional campaigns
            - Schedule maintenance
            - Offer special discounts
            """)


def render_customer_insights(data):
    """Render customer behavior insights"""
    st.header("🎯 Customer Behavior Analysis")
    
    st.markdown("""
    **What it shows:** Customer spending patterns and lifetime value distribution
    
    **Why it matters:** Informs customer acquisition cost and retention investment
    
    **Key insight:** Median customer spends $674 - focus on moving customers up the value ladder
    """)
    
    if 'customer_metrics' in data:
        metrics_df = data['customer_metrics']
        
        # Customer total spend distribution
        fig = px.histogram(
            metrics_df,
            x='total_spend',
            nbins=50,
            title='Customer Total Spend Distribution',
            labels={'total_spend': 'Total Spend ($)', 'count': 'Number of Customers'},
            color_discrete_sequence=['#2ca02c']
        )
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Median Spend", f"${metrics_df['total_spend'].median():,.2f}")
        
        with col2:
            st.metric("Mean Spend", f"${metrics_df['total_spend'].mean():,.2f}")
        
        with col3:
            st.metric("90th Percentile", f"${metrics_df['total_spend'].quantile(0.9):,.2f}")
        
        with col4:
            st.metric("Top 1%", f"${metrics_df['total_spend'].quantile(0.99):,.2f}")
        
        st.info("""
        **Value Ladder Strategy:** Most customers are occasional buyers (median $674).
        Opportunity to increase customer lifetime value through:
        - Loyalty programs
        - Cross-sell and upsell
        - Personalized recommendations
        - Exclusive member benefits
        """)


def render_outlier_analysis(data):
    """Render outlier detection results"""
    st.header("🔍 Outlier Detection & Analysis")
    
    st.markdown("""
    **What it shows:** Unusual patterns requiring attention
    
    **Why it matters:** Outliers can indicate opportunities, risks, or data quality issues
    
    **Key insight:** 222 ultra-high-value customers (5%) generate $4.5M revenue - VIP treatment required
    """)
    
    if 'outliers' in data:
        outliers_df = data['outliers']
        
        # Outlier summary
        for _, outlier in outliers_df.iterrows():
            with st.expander(f"**{outlier['outlier_type'].replace('_', ' ').title()}** ({outlier['count']} instances)"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Reason:** {outlier['reason']}")
                    st.markdown(f"**Impact:** {outlier['impact']}")
                    st.markdown(f"**Recommended Action:** {outlier['action']}")
                    st.info(f"**Business Meaning:** {outlier['business_meaning']}")
                
                with col2:
                    st.metric("Count", f"{outlier['count']:,}")
                    st.metric("Total Value", f"${outlier['total_value']:,.2f}")


def render():
    """Main render function for BI Insights page"""
    # Load data
    data = load_bi_data()
    
    # Render page sections
    render_page_header()
    render_key_insights(data)
    render_rfm_segmentation(data)
    render_revenue_concentration(data)
    render_temporal_trends(data)
    render_customer_insights(data)
    render_outlier_analysis(data)
    
    # Conclusion
    st.header("🎯 BI Insights Summary")
    st.markdown("""
    ### Key Takeaways
    
    1. **Revenue Concentration:** 65% from Champions (22% of customers) - high dependency risk
    2. **Pareto Principle:** 5% of customers generate 50% of revenue - focus retention here
    3. **Temporal Patterns:** Thursday peak, Sunday low - optimize operations accordingly
    4. **Customer Value:** Median $674 spend - opportunity for value ladder programs
    5. **Outliers:** 222 ultra-high-value customers need VIP treatment
    
    ### Strategic Priorities
    
    **Immediate Actions:**
    1. Implement VIP program for top 5% customers (Champions + high spenders)
    2. Launch win-back campaigns for "At Risk" and "Lost" segments
    3. Optimize Thursday operations (staffing, inventory, capacity)
    4. Develop value ladder to move customers from $674 median to higher tiers
    
    **Long-term Strategy:**
    1. Reduce revenue concentration through customer base diversification
    2. Build loyalty programs to convert "Potential Loyalists"
    3. Implement predictive churn models for early intervention
    4. Personalize marketing based on RFM segments
    
    **The value of BI isn't in the numbers - it's in the actions they inspire.**
    """)


if __name__ == "__main__":
    render()
