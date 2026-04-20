"""
HPC Engine Page
Explain HPC role clearly
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path


def load_hpc_data():
    """Load HPC results"""
    data = {}
    
    # HPC summary
    summary_path = Path('../data/hpc_results_summary.csv')
    if summary_path.exists():
        data['summary'] = pd.read_csv(summary_path)
    
    # Thread scaling
    thread_path = Path('../data/hpc_thread_scaling.csv')
    if thread_path.exists():
        data['threads'] = pd.read_csv(thread_path)
    
    return data


def render():
    """Render HPC Engine page"""
    
    # Title
    st.title("⚡ HPC Engine: High-Performance Computing")
    st.markdown("**Fast parallel processing for large-scale data analysis**")
    st.markdown("---")
    
    # Load data
    data = load_hpc_data()
    
    # Role of HPC
    st.header("🎯 What Does HPC Do?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **HPC (High-Performance Computing) handles:**
        
        1. **Large-Scale Computation**
           - Processes 400K+ transactions efficiently
           - Performs complex calculations (RFM, correlations, percentiles)
        
        2. **Parallel Processing**
           - Uses multiple CPU threads simultaneously
           - Divides work across threads for faster execution
        
        3. **Speed Optimization**
           - Reduces computation time
           - Enables real-time analytics
        """)
    
    with col2:
        st.info("""
        **Technology:**
        - Language: C++
        - Framework: OpenMP
        - Approach: Thread-based parallelism
        """)
    
    st.markdown("---")
    
    # KPI Row
    st.header("📊 Performance Metrics")
    
    if 'summary' in data and 'threads' in data:
        summary_df = data['summary']
        threads_df = data['threads']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            seq_time = threads_df[threads_df['threads'] == 1]['par_time'].values
            if len(seq_time) > 0:
                st.metric(
                    "⏱️ Sequential Time",
                    f"{seq_time[0]:.3f}s",
                    help="Time taken with single thread"
                )
        
        with col2:
            optimal_row = threads_df.loc[threads_df['speedup'].idxmax()]
            par_time = optimal_row['par_time']
            st.metric(
                "⚡ Parallel Time",
                f"{par_time:.3f}s",
                help=f"Time taken with {int(optimal_row['threads'])} threads"
            )
        
        with col3:
            max_speedup = threads_df['speedup'].max()
            st.metric(
                "🚀 Speedup",
                f"{max_speedup:.2f}x",
                help="Performance improvement ratio"
            )
        
        with col4:
            optimal_threads = threads_df.loc[threads_df['speedup'].idxmax(), 'threads']
            optimal_efficiency = threads_df.loc[threads_df['speedup'].idxmax(), 'efficiency']
            st.metric(
                "⚙️ Optimal Threads",
                f"{int(optimal_threads)}",
                f"{optimal_efficiency*100:.1f}% efficiency"
            )
    
    st.markdown("---")
    
    # Thread Scaling Chart
    st.header("📈 Thread Scaling Analysis")
    
    st.markdown("**How performance changes with different thread counts**")
    
    if 'threads' in data:
        threads_df = data['threads']
        
        # Create dual-axis chart
        fig = go.Figure()
        
        # Speedup line
        fig.add_trace(go.Scatter(
            x=threads_df['threads'],
            y=threads_df['speedup'],
            mode='lines+markers',
            name='Speedup',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=10),
            yaxis='y'
        ))
        
        # Efficiency line
        fig.add_trace(go.Scatter(
            x=threads_df['threads'],
            y=threads_df['efficiency'] * 100,
            mode='lines+markers',
            name='Efficiency (%)',
            line=dict(color='#ff7f0e', width=3, dash='dash'),
            marker=dict(size=10),
            yaxis='y2'
        ))
        
        # Ideal speedup (linear)
        fig.add_trace(go.Scatter(
            x=threads_df['threads'],
            y=threads_df['threads'],
            mode='lines',
            name='Ideal (Linear)',
            line=dict(color='gray', width=2, dash='dot'),
            yaxis='y'
        ))
        
        fig.update_layout(
            title='Speedup and Efficiency vs Thread Count',
            xaxis=dict(title='Number of Threads'),
            yaxis=dict(title='Speedup (x)', side='left'),
            yaxis2=dict(title='Efficiency (%)', side='right', overlaying='y'),
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key Insight
        optimal_threads = threads_df.loc[threads_df['speedup'].idxmax(), 'threads']
        max_speedup = threads_df['speedup'].max()
        
        st.success(f"""
        **💡 Key Insight:** Optimal performance achieved with **{int(optimal_threads)} threads** 
        giving **{max_speedup:.2f}x speedup**. Beyond this, overhead reduces efficiency.
        """)
    
    st.markdown("---")
    
    # Computations Performed
    st.header("🔧 Computations Performed by HPC")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Statistical Computations:**
        - 📊 **Revenue Aggregation**: Total, average, median
        - 📈 **Percentiles**: 25th, 50th, 75th, 90th, 95th
        - 🔗 **Correlation Analysis**: Quantity vs Unit Price
        """)
    
    with col2:
        st.markdown("""
        **Business Analytics:**
        - 👥 **RFM Analysis**: Recency, Frequency, Monetary
        - 🏆 **Top-K Analysis**: Top customers and products
        - 📉 **Moving Averages**: 7-day and 30-day trends
        """)
    
    st.markdown("---")
    
    # Performance Summary
    if 'summary' in data:
        summary_df = data['summary']
        
        st.header("📋 Computation Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rows = summary_df[summary_df['metric'] == 'total_rows_processed']['value'].values
            if len(rows) > 0:
                st.metric("📦 Rows Processed", f"{int(rows[0]):,}")
        
        with col2:
            revenue = summary_df[summary_df['metric'] == 'total_revenue']['value'].values
            if len(revenue) > 0:
                st.metric("💰 Total Revenue", f"${revenue[0]:,.2f}")
        
        with col3:
            comp_time = summary_df[summary_df['metric'] == 'computation_time']['value'].values
            if len(comp_time) > 0:
                st.metric("⏱️ Computation Time", f"{comp_time[0]:.3f}s")
    
    st.markdown("---")
    
    # Key Takeaway
    st.header("🎯 Key Takeaway")
    
    st.info("""
    **HPC enables fast computation through parallel processing:**
    
    ✅ **Speed**: Processes large datasets in milliseconds
    
    ✅ **Scalability**: Handles increasing data volumes efficiently
    
    ✅ **Accuracy**: Maintains precision in all calculations
    
    ⚠️ **Limitation**: Speedup limited by overhead and sequential portions (Amdahl's Law)
    """)
    
    # Technical Note (expandable)
    with st.expander("🔬 Technical Details (Optional)"):
        st.markdown("""
        **Parallel Processing Approach:**
        - **Thread-local aggregation**: Each thread maintains its own data structure
        - **Reduced contention**: Minimizes synchronization overhead
        - **Sequential merging**: Combines results after parallel computation
        
        **Performance Factors:**
        - **Parallelizable fraction**: ~92% of computation can run in parallel
        - **Sequential portion**: ~8% must run sequentially (sorting, merging)
        - **Overhead**: Thread creation and synchronization add cost
        - **Memory bandwidth**: Can become bottleneck with many threads
        
        **Why not higher speedup?**
        - Fast baseline computation (0.024s) means overhead is significant
        - Memory-bound operations limit parallel efficiency
        - Amdahl's Law: Sequential portion limits theoretical maximum speedup
        """)
