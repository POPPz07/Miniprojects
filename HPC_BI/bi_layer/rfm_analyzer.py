"""
RFM Analyzer Module
Implements RFM (Recency, Frequency, Monetary) analysis for customer segmentation
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    filename='../logs/bi_execution.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_message(message):
    """Log message to both console and file"""
    logging.info(message)
    print(f"[INFO] {message}")


class RFMAnalyzer:
    """
    RFM Analyzer for customer segmentation
    
    Computes:
    - Recency: Days since last purchase
    - Frequency: Number of unique purchases
    - Monetary: Total spend
    """
    
    def __init__(self, df):
        """
        Initialize RFM Analyzer
        
        Args:
            df: DataFrame with columns: CustomerID, InvoiceNo, InvoiceDate, TotalPrice
        """
        self.df = df.copy()
        self.rfm_df = None
        self.reference_date = None
        
        log_message("RFMAnalyzer initialized")
    
    def compute_rfm_features(self):
        """
        Compute RFM features for all customers
        
        Returns:
            DataFrame with columns: CustomerID, Recency, Frequency, Monetary
        """
        log_message("="*60)
        log_message("Computing RFM Features")
        log_message("="*60)
        
        # Ensure InvoiceDate is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.df['InvoiceDate']):
            self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])
        
        # Get reference date (most recent date in dataset)
        self.reference_date = self.df['InvoiceDate'].max()
        log_message(f"Reference date: {self.reference_date}")
        
        # Group by CustomerID and compute RFM metrics
        log_message("Aggregating customer data...")
        
        rfm_data = self.df.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (self.reference_date - x.max()).days,  # Recency
            'InvoiceNo': 'nunique',  # Frequency (unique invoices)
            'TotalPrice': 'sum'  # Monetary
        }).reset_index()
        
        # Rename columns
        rfm_data.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
        
        # Convert CustomerID to string for consistency
        rfm_data['CustomerID'] = rfm_data['CustomerID'].astype(str)
        
        self.rfm_df = rfm_data
        
        log_message(f"RFM features computed for {len(rfm_data)} customers")
        log_message(f"  Recency range: {rfm_data['Recency'].min()} - {rfm_data['Recency'].max()} days")
        log_message(f"  Frequency range: {rfm_data['Frequency'].min()} - {rfm_data['Frequency'].max()} purchases")
        log_message(f"  Monetary range: ${rfm_data['Monetary'].min():.2f} - ${rfm_data['Monetary'].max():.2f}")
        
        return self.rfm_df
    
    def get_rfm_summary(self):
        """
        Get summary statistics for RFM metrics
        
        Returns:
            Dictionary with summary statistics
        """
        if self.rfm_df is None:
            log_message("WARNING: RFM features not computed yet. Call compute_rfm_features() first.")
            return None
        
        summary = {
            'total_customers': len(self.rfm_df),
            'avg_recency': self.rfm_df['Recency'].mean(),
            'avg_frequency': self.rfm_df['Frequency'].mean(),
            'avg_monetary': self.rfm_df['Monetary'].mean(),
            'median_recency': self.rfm_df['Recency'].median(),
            'median_frequency': self.rfm_df['Frequency'].median(),
            'median_monetary': self.rfm_df['Monetary'].median()
        }
        
        log_message("RFM Summary Statistics:")
        for key, value in summary.items():
            if 'monetary' in key.lower():
                log_message(f"  {key}: ${value:.2f}")
            else:
                log_message(f"  {key}: {value:.2f}")
        
        return summary
    
    def compute_rfm_scores(self):
        """
        Compute RFM scores (1-5 scale) using quintile-based scoring
        
        Returns:
            DataFrame with RFM scores added
        """
        if self.rfm_df is None:
            log_message("ERROR: RFM features not computed yet. Call compute_rfm_features() first.")
            return None
        
        log_message("="*60)
        log_message("Computing RFM Scores")
        log_message("="*60)
        
        # Compute quintiles for each metric
        # Recency: Lower is better (5 = most recent)
        # Frequency: Higher is better (5 = most frequent)
        # Monetary: Higher is better (5 = highest spend)
        
        # Use qcut with duplicates='drop' to handle duplicate values
        try:
            self.rfm_df['R_Score'] = pd.qcut(
                self.rfm_df['Recency'], 
                q=5, 
                labels=[5, 4, 3, 2, 1],  # Reverse order: lower recency = higher score
                duplicates='drop'
            ).astype(int)
        except ValueError:
            # If qcut fails due to too many duplicates, use rank-based approach
            log_message("WARNING: Using rank-based approach for Recency scoring due to duplicate values")
            self.rfm_df['R_Score'] = pd.cut(
                self.rfm_df['Recency'].rank(method='first'),
                bins=5,
                labels=[5, 4, 3, 2, 1]
            ).astype(int)
        
        try:
            self.rfm_df['F_Score'] = pd.qcut(
                self.rfm_df['Frequency'],
                q=5,
                labels=[1, 2, 3, 4, 5],  # Higher frequency = higher score
                duplicates='drop'
            ).astype(int)
        except ValueError:
            log_message("WARNING: Using rank-based approach for Frequency scoring due to duplicate values")
            self.rfm_df['F_Score'] = pd.cut(
                self.rfm_df['Frequency'].rank(method='first'),
                bins=5,
                labels=[1, 2, 3, 4, 5]
            ).astype(int)
        
        try:
            self.rfm_df['M_Score'] = pd.qcut(
                self.rfm_df['Monetary'],
                q=5,
                labels=[1, 2, 3, 4, 5],  # Higher monetary = higher score
                duplicates='drop'
            ).astype(int)
        except ValueError:
            log_message("WARNING: Using rank-based approach for Monetary scoring due to duplicate values")
            self.rfm_df['M_Score'] = pd.cut(
                self.rfm_df['Monetary'].rank(method='first'),
                bins=5,
                labels=[1, 2, 3, 4, 5]
            ).astype(int)
        
        # Create combined RFM score string
        self.rfm_df['RFM_Score'] = (
            self.rfm_df['R_Score'].astype(str) +
            self.rfm_df['F_Score'].astype(str) +
            self.rfm_df['M_Score'].astype(str)
        )
        
        log_message("RFM scores computed successfully")
        log_message(f"  R_Score range: {self.rfm_df['R_Score'].min()} - {self.rfm_df['R_Score'].max()}")
        log_message(f"  F_Score range: {self.rfm_df['F_Score'].min()} - {self.rfm_df['F_Score'].max()}")
        log_message(f"  M_Score range: {self.rfm_df['M_Score'].min()} - {self.rfm_df['M_Score'].max()}")
        
        return self.rfm_df
    
    def segment_customers(self):
        """
        Segment customers based on RFM scores
        
        Segments:
        - Champions: R >= 4, F >= 4, M >= 4
        - Loyal Customers: F >= 4, M >= 4
        - Potential Loyalists: R >= 4, F <= 3
        - At Risk: R <= 2, F >= 3
        - Lost: R <= 2, F <= 2
        - Other: All others
        
        Returns:
            DataFrame with Segment column added
        """
        if self.rfm_df is None or 'R_Score' not in self.rfm_df.columns:
            log_message("ERROR: RFM scores not computed yet. Call compute_rfm_scores() first.")
            return None
        
        log_message("="*60)
        log_message("Segmenting Customers")
        log_message("="*60)
        
        def assign_segment(row):
            r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
            
            if r >= 4 and f >= 4 and m >= 4:
                return 'Champions'
            elif f >= 4 and m >= 4:
                return 'Loyal Customers'
            elif r >= 4 and f <= 3:
                return 'Potential Loyalists'
            elif r <= 2 and f >= 3:
                return 'At Risk'
            elif r <= 2 and f <= 2:
                return 'Lost'
            else:
                return 'Other'
        
        self.rfm_df['Segment'] = self.rfm_df.apply(assign_segment, axis=1)
        
        # Log segment distribution
        segment_counts = self.rfm_df['Segment'].value_counts()
        log_message("Customer Segmentation Results:")
        for segment, count in segment_counts.items():
            percentage = (count / len(self.rfm_df)) * 100
            log_message(f"  {segment}: {count} customers ({percentage:.1f}%)")
        
        return self.rfm_df
    
    def validate_rfm_metrics(self):
        """
        Validate RFM metrics and scores
        
        Checks:
        - Recency >= 0
        - Frequency >= 1
        - Monetary > 0
        - RFM scores in range 1-5
        
        Returns:
            Dictionary with validation results
        """
        if self.rfm_df is None:
            log_message("ERROR: RFM features not computed yet.")
            return None
        
        log_message("="*60)
        log_message("Validating RFM Metrics")
        log_message("="*60)
        
        validation_results = {
            'total_customers': len(self.rfm_df),
            'valid_recency': (self.rfm_df['Recency'] >= 0).sum(),
            'valid_frequency': (self.rfm_df['Frequency'] >= 1).sum(),
            'valid_monetary': (self.rfm_df['Monetary'] > 0).sum(),
            'invalid_recency': (self.rfm_df['Recency'] < 0).sum(),
            'invalid_frequency': (self.rfm_df['Frequency'] < 1).sum(),
            'invalid_monetary': (self.rfm_df['Monetary'] <= 0).sum()
        }
        
        # Validate scores if they exist
        if 'R_Score' in self.rfm_df.columns:
            validation_results['valid_r_score'] = self.rfm_df['R_Score'].between(1, 5).sum()
            validation_results['valid_f_score'] = self.rfm_df['F_Score'].between(1, 5).sum()
            validation_results['valid_m_score'] = self.rfm_df['M_Score'].between(1, 5).sum()
        
        # Log validation results
        log_message("Validation Results:")
        for key, value in validation_results.items():
            log_message(f"  {key}: {value}")
        
        # Check if all validations passed
        all_valid = (
            validation_results['invalid_recency'] == 0 and
            validation_results['invalid_frequency'] == 0 and
            validation_results['invalid_monetary'] == 0
        )
        
        if all_valid:
            log_message("[PASS] All RFM metrics are valid")
        else:
            log_message("[FAIL] Some RFM metrics are invalid")
        
        return validation_results


if __name__ == "__main__":
    # Test RFM Analyzer
    log_message("Testing RFM Analyzer...")
    
    # Load clean data
    df = pd.read_csv('../data/clean_data.csv')
    log_message(f"Loaded clean data: {len(df)} rows")
    
    # Create RFM Analyzer
    analyzer = RFMAnalyzer(df)
    
    # Compute RFM features
    rfm_df = analyzer.compute_rfm_features()
    
    # Get summary
    summary = analyzer.get_rfm_summary()
    
    # Compute RFM scores
    rfm_df = analyzer.compute_rfm_scores()
    
    # Segment customers
    rfm_df = analyzer.segment_customers()
    
    # Validate RFM metrics
    validation = analyzer.validate_rfm_metrics()
    
    # Save RFM data
    rfm_df.to_csv('../data/rfm_analysis.csv', index=False)
    log_message(f"RFM analysis saved to: data/rfm_analysis.csv")
    
    print("\nRFM Analyzer test completed successfully!")
    print(f"RFM DataFrame shape: {rfm_df.shape}")
    print(f"\nFirst 5 customers:")
    print(rfm_df.head())
    print(f"\nSegment distribution:")
    print(rfm_df['Segment'].value_counts())
