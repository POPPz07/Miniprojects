"""
System Journey Page
Tells the story of HPC Engine evolution through 3 iterations
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from pathlib import Path


def load_iteration_data():
    """
    Load iteration history from CSV and JSON files
    
    Returns:
        tuple: (metrics_df, iteration_details)
    """
    # Load iteration metrics CSV
    metrics_path = Path('../.kiro/specs/system-explainability-upgrade/metrics/iteration_metrics.csv')
    
    if metrics_path.exists():
        metrics_df = pd.read_csv(metrics_path)
    else:
        st.error("Iteration metrics file not found. Please run the HPC Engine first.")
        return None, None
    
    # Load iteration JSON details
    iteration_details = []
    evolution_dir = Path('../.kiro/specs/system-explainability-upgrade/evolution')
    
    if evolution_dir.exists():
        for json_file in sorted(evolution_dir.glob('iteration_*.json')):
            with open(json_file, 'r') as f:
                iteration_details.append(json.load(f))
    
    return metrics_df, iteration_details


def render_page_header():
    """Render page header with introduction"""
    st.title("🚀 System Journey: HPC Evolution Story")
    
    st.markdown("""
    ## The Story of Parallel Performance
    
    This page chronicles the evolution of our HPC+BI Retail Analytics System through three distinct iterations.
    Each iteration represents a deliberate design decision, an optimization attempt, or a learning moment about
    the realities of parallel computing.
    
    **What you'll discover:**
    - Why parallel performance doesn't always scale linearly
    - How Amdahl's Law limits theoretical speedup
    - The trade-offs between thread count and efficiency
    - Real-world lessons from optimizing a production system
    
    ---
    """)


def render_iteration_timeline(metrics_df):
    """
    Render interactive timeline of iterations
    
    Args:
        metrics_df: DataFrame with iteration metrics
    """
    st.header("📅 Evolution Timeline")
    
    st.markdown("""
    **What it shows:** The chronological progression of system iterations
    
    **Why it matters:** Understanding the sequence helps explain why certain decisions were made
    
    **Key insight:** Each iteration builds on learnings from the previous one
    """)
    
    # Create timeline visualization
    fig = go.Figure()
    
    # Add iteration markers
    for idx, row in metrics_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[pd.to_datetime(row['timestamp'])],
            y=[row['speedup']],
            mode='markers+text',
            name=f"Iteration {row['iteration_number']}",
            text=[f"Iteration {row['iteration_number']}<br>Speedup: {row['speedup']:.2f}x"],
            textposition="top center",
            marker=dict(size=20, symbol='diamond'),
            hovertemplate=(
                f"<b>Iteration {row['iteration_number']}</b><br>" +
                f"Date: {row['timestamp']}<br>" +
                f"Speedup: {row['speedup']:.2f}x<br>" +
                f"Efficiency: {row['efficiency']*100:.1f}%<br>" +
                f"Threads: {row['thread_count']}<br>" +
                "<extra></extra>"
            )
        ))
    
    fig.update_layout(
        title="System Evolution Timeline",
        xaxis_title="Date",
        yaxis_title="Speedup (x)",
        hovermode='closest',
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_performance_progression(metrics_df):
    """
    Render performance progression charts
    
    Args:
        metrics_df: DataFrame with iteration metrics
    """
    st.header("📈 Performance Progression")
    
    st.markdown("""
    **What it shows:** How speedup and efficiency changed across iterations
    
    **Why it matters:** Reveals the impact of optimizations and the limits of parallelization
    
    **Key insight:** Higher speedup doesn't always mean better efficiency
    """)
    
    # Create two columns for speedup and efficiency
    col1, col2 = st.columns(2)
    
    with col1:
        # Speedup progression
        fig_speedup = go.Figure()
        
        fig_speedup.add_trace(go.Scatter(
            x=metrics_df['iteration_number'],
            y=metrics_df['speedup'],
            mode='lines+markers',
            name='Actual Speedup',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=12)
        ))
        
        fig_speedup.add_trace(go.Scatter(
            x=metrics_df['iteration_number'],
            y=metrics_df['theoretical_max_speedup'],
            mode='lines+markers',
            name='Theoretical Max (Amdahl)',
            line=dict(color='#ff7f0e', width=2, dash='dash'),
            marker=dict(size=8)
        ))
        
        fig_speedup.update_layout(
            title="Speedup Progression",
            xaxis_title="Iteration",
            yaxis_title="Speedup (x)",
            hovermode='x unified',
            height=350
        )
        
        st.plotly_chart(fig_speedup, use_container_width=True)
    
    with col2:
        # Efficiency progression
        fig_efficiency = go.Figure()
        
        fig_efficiency.add_trace(go.Scatter(
            x=metrics_df['iteration_number'],
            y=metrics_df['efficiency'] * 100,
            mode='lines+markers',
            name='Efficiency',
            line=dict(color='#2ca02c', width=3),
            marker=dict(size=12),
            fill='tozeroy',
            fillcolor='rgba(44, 160, 44, 0.2)'
        ))
        
        fig_efficiency.update_layout(
            title="Parallel Efficiency",
            xaxis_title="Iteration",
            yaxis_title="Efficiency (%)",
            hovermode='x unified',
            height=350
        )
        
        st.plotly_chart(fig_efficiency, use_container_width=True)


def render_iteration_details(iteration_details):
    """
    Render detailed information for each iteration
    
    Args:
        iteration_details: List of iteration detail dictionaries
    """
    st.header("🔍 Iteration Deep Dive")
    
    st.markdown("""
    **What it shows:** Detailed breakdown of each iteration's goals, results, and learnings
    
    **Why it matters:** Understanding the 'why' behind each change reveals the engineering process
    
    **Key insight:** Every optimization has trade-offs and constraints
    """)
    
    for iteration in iteration_details:
        with st.expander(f"**Iteration {iteration['iterationNumber']}: {iteration['description']}**", expanded=False):
            # What & Why
            st.subheader("🎯 What & Why")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**What Changed:**")
                st.info(iteration['description'])
            
            with col2:
                st.markdown("**Why This Matters:**")
                st.info(iteration['rationale'])
            
            # Configuration
            st.subheader("⚙️ Configuration")
            config = iteration['configuration']
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Thread Count", config['threadCount'])
            with col2:
                st.metric("Data Size", f"{config['dataSize']:,} rows")
            with col3:
                st.metric("Computations", len(config['computationsEnabled']))
            
            # Performance Results
            st.subheader("📊 Performance Results")
            perf = iteration['performance']
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Speedup", f"{perf['speedup']:.2f}x")
            with col2:
                st.metric("Efficiency", f"{perf['efficiency']*100:.1f}%")
            with col3:
                st.metric("Sequential Time", f"{perf['sequentialTime']:.3f}s")
            with col4:
                st.metric("Parallel Time", f"{perf['parallelTime']:.3f}s")
            
            # Performance Breakdown
            st.markdown("**Time Breakdown:**")
            breakdown = perf['breakdown']
            breakdown_df = pd.DataFrame({
                'Phase': ['Data Loading', 'Parallelizable Computation', 'Sequential Computation', 'Output Generation'],
                'Time (s)': [
                    breakdown['dataLoading'],
                    breakdown['parallelizableComputation'],
                    breakdown['sequentialComputation'],
                    breakdown['outputGeneration']
                ]
            })
            
            fig_breakdown = px.bar(
                breakdown_df,
                x='Phase',
                y='Time (s)',
                title='Execution Time Breakdown',
                color='Time (s)',
                color_continuous_scale='Blues'
            )
            fig_breakdown.update_layout(height=300)
            st.plotly_chart(fig_breakdown, use_container_width=True)
            
            # Technical Analysis
            st.subheader("🔬 Technical Analysis")
            analysis = iteration['technicalAnalysis']
            
            st.markdown("**Performance Analysis:**")
            st.write(analysis['performanceAnalysis'])
            
            st.markdown("**Limiting Factors:**")
            st.warning(analysis['limitingFactors'])
            
            # Amdahl's Law Analysis
            st.markdown("**Amdahl's Law Analysis:**")
            amdahl = analysis['amdahlAnalysis']
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Parallelizable Fraction", f"{amdahl['parallelizableFraction']*100:.1f}%")
            with col2:
                st.metric("Theoretical Max Speedup", f"{amdahl['theoreticalMaxSpeedup']:.2f}x")
            with col3:
                st.metric("Actual Speedup", f"{amdahl['actualSpeedup']:.2f}x")
            with col4:
                st.metric("Parallelization Efficiency", f"{amdahl['parallelizationEfficiency']*100:.1f}%")
            
            # Learnings
            st.subheader("💡 Key Learnings")
            for learning in iteration['learnings']:
                st.markdown(f"- {learning}")
            
            # Next Steps
            st.subheader("🚀 Next Steps")
            for step in iteration['nextSteps']:
                st.markdown(f"- {step}")


def render_hpc_limitations():
    """Render HPC limitations and educational content"""
    st.header("⚠️ Understanding HPC Limitations")
    
    st.markdown("""
    **What it shows:** The fundamental constraints that limit parallel performance
    
    **Why it matters:** Understanding these limitations prevents unrealistic expectations
    
    **Key insight:** Parallel computing is not a silver bullet - it has inherent trade-offs
    """)
    
    # Amdahl's Law Explanation
    with st.expander("**📐 Amdahl's Law: The Fundamental Limit**", expanded=True):
        st.markdown("""
        **Amdahl's Law** states that the maximum speedup of a program is limited by its sequential portion:
        
        ```
        Speedup = 1 / (S + P/N)
        ```
        
        Where:
        - **S** = Sequential fraction (cannot be parallelized)
        - **P** = Parallelizable fraction
        - **N** = Number of processors/threads
        
        **Real-World Implication:**
        Even if 90% of your code is parallelizable, the maximum speedup with infinite processors is only 10x.
        In our system, with 91.6% parallelizable code, the theoretical maximum is ~12x speedup.
        
        **Why We See Lower Speedup:**
        - Synchronization overhead (thread coordination)
        - Memory bandwidth limitations (all threads compete for RAM)
        - Cache contention (threads invalidate each other's cache lines)
        - Operating system scheduling overhead
        """)
    
    # Thread Scaling Behavior
    with st.expander("**🧵 Thread Scaling: Why More Isn't Always Better**"):
        st.markdown("""
        **The Thread Scaling Problem:**
        
        Adding more threads doesn't linearly improve performance because:
        
        1. **Overhead Increases:** Each thread requires:
           - Memory for stack space
           - Context switching time
           - Synchronization primitives (locks, barriers)
        
        2. **Resource Contention:** Threads compete for:
           - CPU cache (L1, L2, L3)
           - Memory bandwidth
           - System bus
        
        3. **Diminishing Returns:** Beyond optimal thread count:
           - Overhead exceeds benefit
           - Efficiency drops dramatically
           - May even slow down vs. fewer threads
        
        **Our Findings:**
        - Optimal: 8 threads (13.2% efficiency)
        - 16 threads would likely decrease performance due to overhead
        - Sweet spot depends on workload characteristics
        """)
    
    # Memory Bandwidth
    with st.expander("**💾 Memory Bandwidth: The Hidden Bottleneck**"):
        st.markdown("""
        **Why Memory Matters More Than CPU:**
        
        Modern CPUs are **memory-bound**, not compute-bound:
        
        - **CPU Speed:** ~3-5 GHz (billions of operations/second)
        - **Memory Speed:** ~20-30 GB/s (limited bandwidth)
        - **Result:** CPUs spend most time waiting for data
        
        **Impact on Parallelization:**
        - All threads share the same memory bus
        - More threads = more memory requests = more contention
        - Cache misses become expensive (100+ cycle penalty)
        
        **Optimization Strategies:**
        - Cache-friendly data structures (our unordered_map optimization)
        - Minimize memory allocations (pre-allocation strategy)
        - Reduce data movement (thread-local aggregation)
        """)
    
    # Practical Recommendations
    with st.expander("**✅ Practical Recommendations**"):
        st.markdown("""
        **When to Use Parallelization:**
        - ✅ Large datasets (>100K rows)
        - ✅ Compute-intensive operations (aggregations, sorting)
        - ✅ Independent operations (embarrassingly parallel)
        - ✅ Long-running tasks (overhead amortized)
        
        **When to Avoid Parallelization:**
        - ❌ Small datasets (<10K rows) - overhead dominates
        - ❌ Sequential algorithms (sorting, prefix sums)
        - ❌ I/O-bound operations (disk/network)
        - ❌ Fine-grained operations (per-row processing)
        
        **Optimization Priority:**
        1. **Algorithm choice** (O(n) vs O(n²) matters more than parallelization)
        2. **Data structures** (cache-friendly layouts)
        3. **Memory access patterns** (sequential > random)
        4. **Parallelization** (only after above are optimized)
        """)


def render_comparison_table(metrics_df):
    """
    Render side-by-side comparison of all iterations
    
    Args:
        metrics_df: DataFrame with iteration metrics
    """
    st.header("📋 Iteration Comparison")
    
    st.markdown("""
    **What it shows:** Side-by-side comparison of key metrics across all iterations
    
    **Why it matters:** Enables quick identification of trends and trade-offs
    
    **Key insight:** Optimization is about finding the right balance, not maximizing every metric
    """)
    
    # Prepare comparison data
    comparison_df = metrics_df[[
        'iteration_number',
        'description',
        'thread_count',
        'speedup',
        'efficiency',
        'parallelizable_fraction',
        'theoretical_max_speedup'
    ]].copy()
    
    # Format for display
    comparison_df['efficiency'] = (comparison_df['efficiency'] * 100).round(1).astype(str) + '%'
    comparison_df['parallelizable_fraction'] = (comparison_df['parallelizable_fraction'] * 100).round(1).astype(str) + '%'
    comparison_df['speedup'] = comparison_df['speedup'].round(2).astype(str) + 'x'
    comparison_df['theoretical_max_speedup'] = comparison_df['theoretical_max_speedup'].round(2).astype(str) + 'x'
    
    # Rename columns for display
    comparison_df.columns = [
        'Iteration',
        'Description',
        'Threads',
        'Speedup',
        'Efficiency',
        'Parallelizable %',
        'Theoretical Max'
    ]
    
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)


def render():
    """Main render function for System Journey page"""
    # Load data
    metrics_df, iteration_details = load_iteration_data()
    
    if metrics_df is None or iteration_details is None:
        st.error("Unable to load iteration data. Please ensure the HPC Engine has been executed.")
        return
    
    # Render page sections
    render_page_header()
    render_iteration_timeline(metrics_df)
    render_performance_progression(metrics_df)
    render_comparison_table(metrics_df)
    render_iteration_details(iteration_details)
    render_hpc_limitations()
    
    # Conclusion
    st.header("🎓 Conclusion")
    st.markdown("""
    ### What We Learned
    
    This journey through HPC optimization reveals several fundamental truths about parallel computing:
    
    1. **Amdahl's Law is Real:** Sequential portions fundamentally limit speedup
    2. **Overhead Matters:** Thread management and synchronization have real costs
    3. **Memory is the Bottleneck:** Modern systems are memory-bound, not compute-bound
    4. **Optimization is Iterative:** Each improvement reveals new bottlenecks
    5. **Trade-offs are Inevitable:** Higher speedup often means lower efficiency
    
    ### The Bigger Picture
    
    Parallel computing is a powerful tool, but it's not magic. Success requires:
    - Understanding your workload characteristics
    - Measuring and profiling before optimizing
    - Accepting the fundamental limits (Amdahl's Law)
    - Balancing speedup, efficiency, and complexity
    
    **Our system achieved 1.05x speedup with 8 threads - modest but honest.** This reflects the reality
    of production systems where overhead, memory bandwidth, and sequential portions limit gains.
    
    The value isn't in the speedup number - it's in understanding *why* we got that number and
    *what* it teaches us about parallel computing.
    """)


if __name__ == "__main__":
    render()
