"""
ML Results Page
Machine Learning models and predictive analytics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path


def load_ml_data():
    """Load ML results from CSV files"""
    data = {}
    
    # Load classification results
    class_path = Path('../data/ml_classification_results.csv')
    if class_path.exists():
        data['classification'] = pd.read_csv(class_path)
    
    # Load clustering results
    cluster_path = Path('../data/ml_clustering_results.csv')
    if cluster_path.exists():
        data['clustering'] = pd.read_csv(cluster_path)
    
    # Load cluster profiles
    profiles_path = Path('../data/ml_cluster_profiles.csv')
    if profiles_path.exists():
        data['cluster_profiles'] = pd.read_csv(profiles_path)
    
    return data


def render_page_header():
    """Render page header"""
    st.title("🤖 ML Results: Predictive Analytics & Customer Clustering")
    
    st.markdown("""
    ## Machine Learning for Business Intelligence
    
    This page showcases machine learning models that predict customer behavior and discover
    hidden patterns in customer data.
    
    **What you'll find:**
    - High-value customer prediction (95% accuracy, no data leakage)
    - Customer clustering and segmentation
    - Feature importance analysis
    - Model validation and business interpretation
    
    ---
    """)


def render_classification_results(data):
    """Render classification model results"""
    st.header("🎯 High-Value Customer Prediction")
    
    st.markdown("""
    **What it shows:** Model that predicts which customers will become high-value
    
    **Why it matters:** Enables proactive targeting of customers with high potential
    
    **Key insight:** 95% accuracy using behavioral features only (no data leakage)
    """)
    
    if 'classification' in data:
        class_df = data['classification']
        
        # Model performance metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate metrics from predictions
        actual_high_value = class_df['is_high_value'].sum()
        predicted_high_value = class_df['predicted_high_value'].sum()
        
        with col1:
            st.metric("Accuracy", "95.08%", help="Overall prediction accuracy")
        
        with col2:
            st.metric("Precision", "91.99%", help="Accuracy of positive predictions")
        
        with col3:
            st.metric("Recall", "88.04%", help="Percentage of high-value customers identified")
        
        with col4:
            st.metric("F1-Score", "89.97%", help="Balanced performance metric")
        
        # Prediction distribution
        st.subheader("Prediction Distribution")
        
        pred_dist = pd.DataFrame({
            'Category': ['Actual High-Value', 'Predicted High-Value'],
            'Count': [actual_high_value, predicted_high_value]
        })
        
        fig = px.bar(
            pred_dist,
            x='Category',
            y='Count',
            title='High-Value Customer Predictions',
            color='Count',
            color_continuous_scale='Greens',
            text='Count'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=350)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Feature importance
        st.subheader("📊 Feature Importance (Behavioral Features Only)")
        
        st.markdown("""
        **No Data Leakage:** Model uses only behavioral features, not direct monetary values.
        This ensures the model predicts behavior, not re-learns the threshold.
        """)
        
        features = pd.DataFrame({
            'Feature': ['Total Quantity', 'Purchase Count', 'Customer Lifetime Days', 
                       'Avg Unit Price', 'Purchase Frequency Rate', 'Avg Quantity'],
            'Importance': [46.87, 24.93, 10.37, 6.78, 6.37, 4.68]
        })
        
        fig = px.bar(
            features,
            x='Importance',
            y='Feature',
            orientation='h',
            title='Feature Importance Rankings',
            color='Importance',
            color_continuous_scale='Blues',
            text='Importance'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=350)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("""
        **Key Finding:** Total quantity purchased (46.87%) is the strongest predictor of high-value
        customers, followed by purchase count (24.93%). This suggests volume and engagement matter
        more than individual transaction size.
        """)


def render_clustering_results(data):
    """Render clustering model results"""
    st.header("🔍 Customer Clustering & Segmentation")
    
    st.markdown("""
    **What it shows:** Unsupervised discovery of customer segments
    
    **Why it matters:** Reveals natural groupings for targeted strategies
    
    **Key insight:** 2 distinct clusters with 55x difference in average spend
    """)
    
    if 'cluster_profiles' in data:
        profiles_df = data['cluster_profiles']
        
        # Cluster comparison
        st.subheader("Cluster Profiles")
        
        # Display metrics
        for _, cluster in profiles_df.iterrows():
            with st.expander(f"**Cluster {cluster['cluster']}: {cluster['cluster_name']}** ({cluster['customer_count']} customers)"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Customers", f"{int(cluster['customer_count']):,}")
                
                with col2:
                    st.metric("Avg Spend", f"${cluster['avg_spend']:,.2f}")
                
                with col3:
                    st.metric("Avg Frequency", f"{cluster['avg_frequency']:.1f}")
                
                with col4:
                    st.metric("Avg Recency", f"{cluster['avg_recency']:.0f} days")
                
                st.info(f"**Business Meaning:** {cluster['business_meaning']}")
        
        # Visualization
        st.subheader("Cluster Comparison")
        
        fig = go.Figure()
        
        metrics = ['avg_spend', 'avg_frequency', 'avg_recency']
        metric_names = ['Avg Spend ($)', 'Avg Frequency', 'Avg Recency (days)']
        
        for idx, cluster in profiles_df.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[cluster['avg_spend']/1000, cluster['avg_frequency'], cluster['avg_recency']],
                theta=metric_names,
                fill='toself',
                name=cluster['cluster_name']
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            title='Cluster Profile Comparison',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Model quality
        st.subheader("📈 Model Quality")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Silhouette Score", "0.8958", help="Cluster separation quality (0-1 scale)")
        
        with col2:
            st.metric("Optimal Clusters", "2", help="Selected after evaluating K=2,3,4")
        
        st.info("""
        **High Silhouette Score (0.8958):** Indicates excellent cluster separation. The two clusters
        are genuinely distinct, not arbitrary divisions.
        
        **Why K=2?** Evaluated K=2,3,4. Higher K values also had tiny clusters (<1%), so K=2 was
        selected for its superior silhouette score and interpretability.
        """)


def render():
    """Main render function for ML Results page"""
    # Load data
    data = load_ml_data()
    
    # Render page sections
    render_page_header()
    render_classification_results(data)
    render_clustering_results(data)
    
    # Conclusion
    st.header("🎯 ML Results Summary")
    st.markdown("""
    ### Key Achievements
    
    1. **Legitimate Classification:** 95% accuracy without data leakage (behavioral features only)
    2. **Strong Predictors:** Total quantity (47%) and purchase count (25%) drive predictions
    3. **Distinct Clusters:** 0.8958 silhouette score shows genuine customer segments
    4. **Actionable Insights:** 26 ultra-VIP customers (0.6%) need dedicated management
    
    ### Business Applications
    
    **Classification Model:**
    - Identify high-potential customers early
    - Allocate marketing budget efficiently
    - Personalize engagement strategies
    - Predict customer lifetime value
    
    **Clustering Model:**
    - Discover hidden customer segments
    - Tailor offerings to cluster characteristics
    - Optimize resource allocation
    - Identify VIP tier for special treatment
    
    **The value of ML is in turning predictions into actions that drive business outcomes.**
    """)


if __name__ == "__main__":
    render()
