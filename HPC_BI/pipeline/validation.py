"""
Cross-Module Validation
Validates consistency between HPC Engine and BI Layer results
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
import os

# Setup logging
log_dir = '../logs'
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename='../logs/validation.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_message(message):
    """Log message to both console and file"""
    logging.info(message)
    print(f"[INFO] {message}")


class CrossModuleValidator:
    """
    Cross-Module Validation Engine
    Validates consistency between HPC and BI results
    """
    
    def __init__(self):
        """Initialize validator"""
        self.validation_results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'checks': [],
            'overall_status': 'PENDING'
        }
        log_message("CrossModuleValidator initialized")
    
    def validate_revenue_consistency(self, tolerance_pct=1.0):
        """
        Validate revenue consistency between HPC and BI
        
        Args:
            tolerance_pct: Acceptable percentage difference (default 1%)
            
        Returns:
            dict with validation result
        """
        log_message("="*60)
        log_message("Validating Revenue Consistency (HPC vs BI)")
        log_message("="*60)
        
        try:
            # Load HPC results
            hpc_results = pd.read_csv('../data/hpc_results_summary.csv')
            hpc_revenue = hpc_results[hpc_results['metric'] == 'total_revenue']['value'].values[0]
            
            # Load BI clean data
            bi_data = pd.read_csv('../data/clean_data.csv')
            bi_revenue = bi_data['TotalPrice'].sum()
            
            # Calculate difference
            diff = abs(hpc_revenue - bi_revenue)
            diff_pct = (diff / hpc_revenue) * 100
            
            # Determine status
            status = 'PASS' if diff_pct <= tolerance_pct else 'FAIL'
            
            result = {
                'check_name': 'Revenue Consistency',
                'status': status,
                'hpc_value': hpc_revenue,
                'bi_value': bi_revenue,
                'difference': diff,
                'difference_pct': diff_pct,
                'tolerance_pct': tolerance_pct,
                'message': f"Revenue difference: ${diff:,.2f} ({diff_pct:.4f}%)"
            }
            
            log_message(f"HPC Total Revenue: ${hpc_revenue:,.2f}")
            log_message(f"BI Total Revenue:  ${bi_revenue:,.2f}")
            log_message(f"Difference: ${diff:,.2f} ({diff_pct:.4f}%)")
            log_message(f"Tolerance: {tolerance_pct}%")
            log_message(f"Status: [{status}]")
            
            self.validation_results['checks'].append(result)
            return result
            
        except Exception as e:
            error_result = {
                'check_name': 'Revenue Consistency',
                'status': 'ERROR',
                'message': f"Validation failed: {str(e)}"
            }
            log_message(f"[ERROR] {str(e)}")
            self.validation_results['checks'].append(error_result)
            return error_result
    
    def validate_customer_count_consistency(self):
        """
        Validate customer count consistency across BI, RFM, and ML
        
        Returns:
            dict with validation result
        """
        log_message("="*60)
        log_message("Validating Customer Count Consistency")
        log_message("="*60)
        
        try:
            # Load datasets
            bi_data = pd.read_csv('../data/clean_data.csv')
            rfm_data = pd.read_csv('../data/rfm_analysis.csv')
            ml_classification = pd.read_csv('../data/ml_classification_results.csv')
            ml_clustering = pd.read_csv('../data/ml_clustering_results.csv')
            
            # Count unique customers
            bi_customers = bi_data['CustomerID'].nunique()
            rfm_customers = len(rfm_data)
            ml_class_customers = len(ml_classification)
            ml_cluster_customers = len(ml_clustering)
            
            # Check consistency
            all_counts = [bi_customers, rfm_customers, ml_class_customers, ml_cluster_customers]
            all_equal = len(set(all_counts)) == 1
            
            status = 'PASS' if all_equal else 'FAIL'
            
            result = {
                'check_name': 'Customer Count Consistency',
                'status': status,
                'bi_customers': bi_customers,
                'rfm_customers': rfm_customers,
                'ml_classification_customers': ml_class_customers,
                'ml_clustering_customers': ml_cluster_customers,
                'message': f"All modules have {bi_customers} customers" if all_equal else "Customer count mismatch detected"
            }
            
            log_message(f"BI Unique Customers:        {bi_customers}")
            log_message(f"RFM Customers:              {rfm_customers}")
            log_message(f"ML Classification Customers: {ml_class_customers}")
            log_message(f"ML Clustering Customers:     {ml_cluster_customers}")
            log_message(f"Status: [{status}]")
            
            if not all_equal:
                log_message("[WARNING] Customer count mismatch detected!")
                log_message(f"  Discrepancy: {max(all_counts) - min(all_counts)} customers")
            
            self.validation_results['checks'].append(result)
            return result
            
        except Exception as e:
            error_result = {
                'check_name': 'Customer Count Consistency',
                'status': 'ERROR',
                'message': f"Validation failed: {str(e)}"
            }
            log_message(f"[ERROR] {str(e)}")
            self.validation_results['checks'].append(error_result)
            return error_result
    
    def validate_rfm_count_consistency(self):
        """
        Validate RFM customer count consistency between HPC and BI
        
        Returns:
            dict with validation result
        """
        log_message("="*60)
        log_message("Validating RFM Count Consistency (HPC vs BI)")
        log_message("="*60)
        
        try:
            # Load HPC RFM results
            hpc_rfm = pd.read_csv('../data/hpc_rfm_analysis.csv')
            hpc_rfm_count = len(hpc_rfm)
            
            # Load BI RFM results
            bi_rfm = pd.read_csv('../data/rfm_analysis.csv')
            bi_rfm_count = len(bi_rfm)
            
            # Check consistency
            counts_match = hpc_rfm_count == bi_rfm_count
            diff = abs(hpc_rfm_count - bi_rfm_count)
            
            status = 'PASS' if counts_match else 'FAIL'
            
            result = {
                'check_name': 'RFM Count Consistency',
                'status': status,
                'hpc_rfm_count': hpc_rfm_count,
                'bi_rfm_count': bi_rfm_count,
                'difference': diff,
                'message': f"RFM customer counts match: {bi_rfm_count}" if counts_match else f"RFM count mismatch: {diff} customers"
            }
            
            log_message(f"HPC RFM Customers: {hpc_rfm_count}")
            log_message(f"BI RFM Customers:  {bi_rfm_count}")
            log_message(f"Difference: {diff}")
            log_message(f"Status: [{status}]")
            
            if not counts_match:
                log_message("[WARNING] RFM customer count mismatch detected!")
            
            self.validation_results['checks'].append(result)
            return result
            
        except Exception as e:
            error_result = {
                'check_name': 'RFM Count Consistency',
                'status': 'ERROR',
                'message': f"Validation failed: {str(e)}"
            }
            log_message(f"[ERROR] {str(e)}")
            self.validation_results['checks'].append(error_result)
            return error_result
    
    def validate_data_integrity(self):
        """
        Validate data integrity checks
        
        Returns:
            dict with validation result
        """
        log_message("="*60)
        log_message("Validating Data Integrity")
        log_message("="*60)
        
        try:
            # Load BI clean data
            bi_data = pd.read_csv('../data/clean_data.csv')
            
            # Check for invalid values
            invalid_quantity = (bi_data['Quantity'] <= 0).sum()
            invalid_price = (bi_data['UnitPrice'] <= 0).sum()
            invalid_total = (bi_data['TotalPrice'] <= 0).sum()
            missing_customer = bi_data['CustomerID'].isna().sum()
            
            all_valid = (invalid_quantity == 0 and invalid_price == 0 and 
                        invalid_total == 0 and missing_customer == 0)
            
            status = 'PASS' if all_valid else 'FAIL'
            
            result = {
                'check_name': 'Data Integrity',
                'status': status,
                'invalid_quantity': invalid_quantity,
                'invalid_price': invalid_price,
                'invalid_total': invalid_total,
                'missing_customer': missing_customer,
                'total_rows': len(bi_data),
                'message': "All data integrity checks passed" if all_valid else "Data integrity issues detected"
            }
            
            log_message(f"Total Rows: {len(bi_data)}")
            log_message(f"Invalid Quantity: {invalid_quantity}")
            log_message(f"Invalid UnitPrice: {invalid_price}")
            log_message(f"Invalid TotalPrice: {invalid_total}")
            log_message(f"Missing CustomerID: {missing_customer}")
            log_message(f"Status: [{status}]")
            
            if not all_valid:
                log_message("[WARNING] Data integrity issues detected!")
            
            self.validation_results['checks'].append(result)
            return result
            
        except Exception as e:
            error_result = {
                'check_name': 'Data Integrity',
                'status': 'ERROR',
                'message': f"Validation failed: {str(e)}"
            }
            log_message(f"[ERROR] {str(e)}")
            self.validation_results['checks'].append(error_result)
            return error_result
    
    def run_all_validations(self):
        """
        Run all validation checks
        
        Returns:
            dict with complete validation results
        """
        log_message("="*60)
        log_message("CROSS-MODULE VALIDATION STARTED")
        log_message("="*60)
        
        # Run all checks
        self.validate_revenue_consistency()
        self.validate_customer_count_consistency()
        self.validate_rfm_count_consistency()
        self.validate_data_integrity()
        
        # Determine overall status
        statuses = [check['status'] for check in self.validation_results['checks']]
        
        if 'ERROR' in statuses:
            self.validation_results['overall_status'] = 'ERROR'
        elif 'FAIL' in statuses:
            self.validation_results['overall_status'] = 'FAIL'
        else:
            self.validation_results['overall_status'] = 'PASS'
        
        # Summary
        log_message("="*60)
        log_message("VALIDATION SUMMARY")
        log_message("="*60)
        
        for check in self.validation_results['checks']:
            log_message(f"[{check['status']}] {check['check_name']}: {check['message']}")
        
        log_message("="*60)
        log_message(f"OVERALL STATUS: [{self.validation_results['overall_status']}]")
        log_message("="*60)
        
        return self.validation_results
    
    def generate_validation_report(self, output_path='../data/validation_report.csv'):
        """
        Generate validation report CSV
        
        Args:
            output_path: Path to save validation report
        """
        log_message("Generating validation report...")
        
        # Convert results to DataFrame
        report_data = []
        for check in self.validation_results['checks']:
            report_data.append({
                'timestamp': self.validation_results['timestamp'],
                'check_name': check['check_name'],
                'status': check['status'],
                'message': check['message']
            })
        
        report_df = pd.DataFrame(report_data)
        report_df.to_csv(output_path, index=False)
        
        log_message(f"Validation report saved to: {output_path}")
        
        return report_df


def run_validation():
    """Main validation entry point"""
    validator = CrossModuleValidator()
    results = validator.run_all_validations()
    report = validator.generate_validation_report()
    
    return results, report


if __name__ == "__main__":
    # Run validation
    results, report = run_validation()
    
    print("\n" + "="*60)
    print("VALIDATION COMPLETE")
    print("="*60)
    print(f"Overall Status: {results['overall_status']}")
    print(f"Total Checks: {len(results['checks'])}")
    print(f"Passed: {sum(1 for c in results['checks'] if c['status'] == 'PASS')}")
    print(f"Failed: {sum(1 for c in results['checks'] if c['status'] == 'FAIL')}")
    print(f"Errors: {sum(1 for c in results['checks'] if c['status'] == 'ERROR')}")
    print("="*60)
    
    # Display report
    print("\nValidation Report:")
    print(report.to_string(index=False))
