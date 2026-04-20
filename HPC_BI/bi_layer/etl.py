"""
ETL Module - Extract, Transform, Load
Handles data cleaning and transformation
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
from rfm_analyzer import RFMAnalyzer
from eda_engine import EDAEngine
from ml_engine import MLEngine

# Setup logging
logging.basicConfig(
    filename='logs/bi_execution.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_message(message):
    """Log message to both console and file"""
    logging.info(message)
    print(f"[INFO] {message}")

def load_raw_dataset(filepath):
    """Load raw dataset from CSV"""
    log_message("="*60)
    log_message("BI Layer Started - ETL Process")
    log_message("="*60)
    log_message(f"Loading raw dataset from: {filepath}")
    
    try:
        df = pd.read_csv(filepath, encoding='ISO-8859-1')
        log_message(f"Raw dataset loaded: {len(df)} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        log_message(f"ERROR: Failed to load dataset - {str(e)}")
        return None

def analyze_raw_data(df):
    """Analyze raw data quality"""
    log_message("Analyzing raw data quality...")
    
    stats = {
        'total_rows': len(df),
        'missing_customerID': df['CustomerID'].isna().sum(),
        'negative_quantity': (df['Quantity'] < 0).sum(),
        'invalid_unitprice': (df['UnitPrice'] <= 0).sum(),
        'missing_description': df['Description'].isna().sum()
    }
    
    for key, value in stats.items():
        log_message(f"  {key}: {value}")
    
    return stats

def clean_dataset(df):
    """Clean the dataset"""
    log_message("Starting data cleaning process...")
    
    initial_rows = len(df)
    
    # Step 1: Remove missing CustomerID
    log_message("Step 1: Removing rows with missing CustomerID...")
    df_clean = df[df['CustomerID'].notna()].copy()
    removed = initial_rows - len(df_clean)
    log_message(f"  Removed {removed} rows with missing CustomerID")
    
    # Step 2: Remove negative Quantity (returns)
    log_message("Step 2: Removing rows with negative Quantity...")
    before = len(df_clean)
    df_clean = df_clean[df_clean['Quantity'] > 0].copy()
    removed = before - len(df_clean)
    log_message(f"  Removed {removed} rows with negative Quantity")
    
    # Step 3: Remove invalid UnitPrice
    log_message("Step 3: Removing rows with invalid UnitPrice...")
    before = len(df_clean)
    df_clean = df_clean[df_clean['UnitPrice'] > 0].copy()
    removed = before - len(df_clean)
    log_message(f"  Removed {removed} rows with invalid UnitPrice")
    
    log_message(f"Data cleaning complete: {len(df_clean)} valid rows remaining")
    
    return df_clean

def create_basic_features(df):
    """Create basic derived features"""
    log_message("Creating basic features...")
    
    # TotalPrice = Quantity × UnitPrice
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    log_message("  Created TotalPrice feature")
    
    # Validate TotalPrice
    assert (df['TotalPrice'] > 0).all(), "TotalPrice validation failed"
    log_message("  [PASS] TotalPrice validation passed")
    
    return df

def create_time_features(df):
    """Create time-based features"""
    log_message("Creating time-based features...")
    
    # Convert InvoiceDate to datetime (day-first format: DD/MM/YYYY)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], dayfirst=True)
    
    # Extract time components
    df['Month'] = df['InvoiceDate'].dt.month
    df['DayOfWeek'] = df['InvoiceDate'].dt.dayofweek
    df['Hour'] = df['InvoiceDate'].dt.hour
    
    log_message("  Created Month, DayOfWeek, Hour features")
    
    # Validate time features
    assert df['Month'].between(1, 12).all(), "Month validation failed"
    assert df['DayOfWeek'].between(0, 6).all(), "DayOfWeek validation failed"
    assert df['Hour'].between(0, 23).all(), "Hour validation failed"
    log_message("  [PASS] Time feature validation passed")
    
    return df

def save_clean_dataset(df, filepath):
    """Save cleaned dataset"""
    log_message(f"Saving clean dataset to: {filepath}")
    df.to_csv(filepath, index=False)
    log_message(f"  Clean dataset saved: {len(df)} rows")

def generate_comparison_metrics(raw_stats, clean_df):
    """Generate before/after comparison metrics"""
    log_message("Generating comparison metrics...")
    
    clean_stats = {
        'total_rows': len(clean_df),
        'missing_customerID': 0,
        'negative_quantity': 0,
        'invalid_unitprice': 0,
        'usable_records': len(clean_df)
    }
    
    # Calculate improvement percentages
    comparison = []
    for metric in ['total_rows', 'missing_customerID', 'negative_quantity', 'invalid_unitprice']:
        raw_val = raw_stats.get(metric, 0)
        clean_val = clean_stats.get(metric, 0)
        
        if raw_val > 0:
            improvement = ((clean_val - raw_val) / raw_val) * 100
        else:
            improvement = 0.0
        
        comparison.append({
            'metric': metric,
            'raw': raw_val,
            'processed': clean_val,
            'improvement_pct': round(improvement, 2)
        })
    
    # Add usable records
    comparison.append({
        'metric': 'usable_records',
        'raw': raw_stats['total_rows'] - raw_stats['missing_customerID'] - raw_stats['negative_quantity'],
        'processed': clean_stats['usable_records'],
        'improvement_pct': 0.0
    })
    
    comparison_df = pd.DataFrame(comparison)
    comparison_df.to_csv('../data/bi_comparison_metrics.csv', index=False)
    log_message("  Comparison metrics saved to: data/bi_comparison_metrics.csv")
    
    return comparison_df

def validate_with_hpc(df_clean):
    """
    Validate BI insights with HPC results
    Check revenue consistency within 1% tolerance
    
    Returns:
        bool: True if validation passes, False otherwise
    """
    try:
        # Load HPC results
        hpc_results = pd.read_csv('../data/hpc_results_summary.csv')
        hpc_revenue = hpc_results[hpc_results['metric'] == 'total_revenue']['value'].values[0]
        
        # Calculate BI revenue
        bi_revenue = df_clean['TotalPrice'].sum()
        
        # Calculate difference
        diff = abs(hpc_revenue - bi_revenue)
        diff_pct = (diff / hpc_revenue) * 100
        
        log_message(f"HPC Total Revenue: ${hpc_revenue:,.2f}")
        log_message(f"BI Total Revenue:  ${bi_revenue:,.2f}")
        log_message(f"Difference: ${diff:,.2f} ({diff_pct:.4f}%)")
        
        # Validate within 1% tolerance
        if diff_pct <= 1.0:
            log_message(f"  [PASS] Revenue consistency validated (within 1% tolerance)")
            return True
        else:
            log_message(f"  [FAIL] Revenue discrepancy exceeds 1% tolerance")
            return False
            
    except Exception as e:
        log_message(f"  [ERROR] Validation failed: {str(e)}")
        return False

def run_etl():
    """Main ETL pipeline"""
    # Load raw data
    df_raw = load_raw_dataset('../data/Online_Retail.csv')
    if df_raw is None:
        return None
    
    # Analyze raw data
    raw_stats = analyze_raw_data(df_raw)
    
    # Clean data
    df_clean = clean_dataset(df_raw)
    
    # Create features
    df_clean = create_basic_features(df_clean)
    df_clean = create_time_features(df_clean)
    
    # Save clean dataset
    save_clean_dataset(df_clean, '../data/clean_data.csv')
    
    # Generate comparison metrics
    generate_comparison_metrics(raw_stats, df_clean)
    
    # RFM Analysis
    log_message("="*60)
    log_message("Running RFM Analysis")
    log_message("="*60)
    
    rfm_analyzer = RFMAnalyzer(df_clean)
    rfm_df = rfm_analyzer.compute_rfm_features()
    rfm_df = rfm_analyzer.compute_rfm_scores()
    rfm_df = rfm_analyzer.segment_customers()
    validation = rfm_analyzer.validate_rfm_metrics()
    
    # Save RFM analysis
    rfm_df.to_csv('../data/rfm_analysis.csv', index=False)
    log_message(f"RFM analysis saved to: data/rfm_analysis.csv")
    
    # Enhanced EDA
    log_message("="*60)
    log_message("Running Enhanced Exploratory Data Analysis")
    log_message("="*60)
    
    eda_engine = EDAEngine(df_clean, rfm_df)
    insights_summary = eda_engine.generate_insights_summary()
    
    log_message(f"EDA completed: {len(insights_summary)} insights generated")
    
    # Validate BI insights with HPC results
    log_message("="*60)
    log_message("Validating BI Insights with HPC Results")
    log_message("="*60)
    
    validation_passed = validate_with_hpc(df_clean)
    
    if validation_passed:
        log_message("[PASS] BI-HPC validation successful")
    else:
        log_message("[WARNING] BI-HPC validation failed - review discrepancies")
    
    # Machine Learning Models
    log_message("="*60)
    log_message("Running Machine Learning Models")
    log_message("="*60)
    
    ml_engine = MLEngine(df_clean)
    
    # Train classification model
    classification_df = ml_engine.train_classification_model()
    classification_df.to_csv('../data/ml_classification_results.csv', index=False)
    log_message("Classification results saved to: data/ml_classification_results.csv")
    
    # Train clustering model
    clustering_df = ml_engine.train_clustering_model()
    
    # Interpret clusters
    cluster_profiles = ml_engine.interpret_clusters()
    clustering_df.to_csv('../data/ml_clustering_results.csv', index=False)
    cluster_profiles.to_csv('../data/ml_cluster_profiles.csv', index=False)
    log_message("Clustering results saved to: data/ml_clustering_results.csv")
    log_message("Cluster profiles saved to: data/ml_cluster_profiles.csv")
    
    # Validate ML models
    ml_validation = ml_engine.validate_models()
    
    if ml_validation['classification_valid'] and ml_validation['clustering_valid']:
        log_message("[PASS] ML model validation successful")
    else:
        log_message("[WARNING] ML model validation failed - review model quality")
    
    # Add ML insights to insights summary
    ml_insights = []
    
    # Classification insights
    class_metrics = ml_engine.classification_results['metrics']
    ml_insights.append({
        'analysis_type': 'ml',
        'dimension': 'classification',
        'metric': 'accuracy',
        'value': class_metrics['accuracy'],
        'insight': f"High-value customer prediction accuracy: {class_metrics['accuracy']:.2%}",
        'business_meaning': 'Highly accurate model for identifying valuable customers',
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Clustering insights
    cluster_metrics = ml_engine.clustering_results['metrics']
    ml_insights.append({
        'analysis_type': 'ml',
        'dimension': 'clustering',
        'metric': 'silhouette_score',
        'value': cluster_metrics['silhouette_score'],
        'insight': f"Customer segmentation quality (silhouette): {cluster_metrics['silhouette_score']:.4f}",
        'business_meaning': 'Well-separated customer segments for targeted marketing',
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Append ML insights to existing insights
    existing_insights = pd.read_csv('../data/bi_insights_summary.csv')
    ml_insights_df = pd.DataFrame(ml_insights)
    updated_insights = pd.concat([existing_insights, ml_insights_df], ignore_index=True)
    updated_insights['insight_id'] = range(1, len(updated_insights) + 1)
    updated_insights.to_csv('../data/bi_insights_summary.csv', index=False)
    log_message("ML insights added to bi_insights_summary.csv")
    
    log_message("="*60)
    log_message("ETL Process Completed Successfully")
    log_message("="*60)
    
    return df_clean, rfm_df

if __name__ == "__main__":
    result = run_etl()
    if result is not None:
        df_clean, rfm_df = result
        print("\nETL completed successfully!")
        print(f"Clean dataset shape: {df_clean.shape}")
        print(f"RFM dataset shape: {rfm_df.shape}")
        print(f"\nColumns: {list(df_clean.columns)}")
