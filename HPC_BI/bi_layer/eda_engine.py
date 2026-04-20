"""
EDA Engine Module
Enhanced Exploratory Data Analysis with RFM integration
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


class EDAEngine:
    """
    Enhanced Exploratory Data Analysis Engine
    Integrates deeply with RFM segmentation for meaningful insights
    """
    
    def __init__(self, df, rfm_df=None):
        """
        Initialize EDA Engine
        
        Args:
            df: Clean transaction data
            rfm_df: RFM analysis results (optional but recommended)
        """
        self.df = df.copy()
        self.rfm_df = rfm_df.copy() if rfm_df is not None else None
        self.insights = []
        
        # Merge RFM data if available
        if self.rfm_df is not None:
            # Ensure CustomerID types match
            self.df['CustomerID'] = self.df['CustomerID'].astype(str)
            self.rfm_df['CustomerID'] = self.rfm_df['CustomerID'].astype(str)
            
            self.df = self.df.merge(
                self.rfm_df[['CustomerID', 'Segment', 'RFM_Score']],
                on='CustomerID',
                how='left'
            )
        
        log_message("EDAEngine initialized")
    
    def analyze_revenue_patterns(self):
        """
        Comprehensive revenue analysis with RFM integration
        
        Returns:
            DataFrame with revenue insights by segment, country, and time
        """
        log_message("="*60)
        log_message("Analyzing Revenue Patterns")
        log_message("="*60)
        
        results = []
        
        # 1. Overall revenue metrics
        total_revenue = self.df['TotalPrice'].sum()
        avg_transaction = self.df['TotalPrice'].mean()
        median_transaction = self.df['TotalPrice'].median()
        
        results.append({
            'analysis_type': 'overall',
            'dimension': 'total',
            'segment': 'All',
            'metric': 'total_revenue',
            'value': total_revenue,
            'percentage': 100.0,
            'insight': f'Total revenue: ${total_revenue:,.2f}',
            'business_meaning': 'Baseline for all revenue comparisons'
        })
        
        # 2. Revenue by RFM Segment (if available)
        if 'Segment' in self.df.columns:
            segment_revenue = self.df.groupby('Segment').agg({
                'TotalPrice': ['sum', 'mean', 'count']
            }).reset_index()
            segment_revenue.columns = ['Segment', 'total_revenue', 'avg_transaction', 'transaction_count']
            segment_revenue['percentage'] = (segment_revenue['total_revenue'] / total_revenue) * 100
            segment_revenue = segment_revenue.sort_values('total_revenue', ascending=False)
            
            for _, row in segment_revenue.iterrows():
                # Only include meaningful insights (>1% contribution or top segments)
                if row['percentage'] > 1.0 or row['Segment'] in ['Champions', 'Loyal Customers']:
                    results.append({
                        'analysis_type': 'segment',
                        'dimension': 'rfm_segment',
                        'segment': row['Segment'],
                        'metric': 'revenue_contribution',
                        'value': row['total_revenue'],
                        'percentage': row['percentage'],
                        'insight': f"{row['Segment']} contribute ${row['total_revenue']:,.2f} ({row['percentage']:.1f}%)",
                        'business_meaning': self._interpret_segment_revenue(row['Segment'], row['percentage'])
                    })
            
            # Save segment revenue breakdown
            segment_revenue.to_csv('../data/eda_revenue_by_segment.csv', index=False)
            log_message(f"Saved revenue by segment analysis")
        
        # 3. Revenue by Country (top 10)
        country_revenue = self.df.groupby('Country').agg({
            'TotalPrice': 'sum',
            'CustomerID': 'nunique'
        }).reset_index()
        country_revenue.columns = ['Country', 'total_revenue', 'unique_customers']
        country_revenue['percentage'] = (country_revenue['total_revenue'] / total_revenue) * 100
        country_revenue = country_revenue.sort_values('total_revenue', ascending=False).head(10)
        
        for idx, row in country_revenue.iterrows():
            if row['percentage'] > 5.0:  # Only significant markets
                results.append({
                    'analysis_type': 'geographic',
                    'dimension': 'country',
                    'segment': row['Country'],
                    'metric': 'revenue_contribution',
                    'value': row['total_revenue'],
                    'percentage': row['percentage'],
                    'insight': f"{row['Country']}: ${row['total_revenue']:,.2f} ({row['percentage']:.1f}%) from {row['unique_customers']} customers",
                    'business_meaning': f"{'Major' if row['percentage'] > 50 else 'Significant'} market requiring focused strategy"
                })
        
        country_revenue.to_csv('../data/eda_revenue_by_country.csv', index=False)
        log_message(f"Saved revenue by country analysis (top 10)")
        
        # 4. Revenue concentration (Pareto analysis)
        customer_revenue = self.df.groupby('CustomerID')['TotalPrice'].sum().sort_values(ascending=False)
        cumulative_pct = (customer_revenue.cumsum() / total_revenue) * 100
        
        top_10_pct_customers = (cumulative_pct <= 10).sum()
        top_20_pct_customers = (cumulative_pct <= 20).sum()
        top_50_pct_revenue_customers = (cumulative_pct <= 50).sum()
        
        total_customers = len(customer_revenue)
        
        results.append({
            'analysis_type': 'concentration',
            'dimension': 'customer_pareto',
            'segment': 'Top 10% Revenue',
            'metric': 'customer_count',
            'value': top_10_pct_customers,
            'percentage': (top_10_pct_customers / total_customers) * 100,
            'insight': f"Top {top_10_pct_customers} customers ({(top_10_pct_customers/total_customers)*100:.1f}%) generate 10% of revenue",
            'business_meaning': 'High revenue concentration indicates dependency on few customers'
        })
        
        results.append({
            'analysis_type': 'concentration',
            'dimension': 'customer_pareto',
            'segment': 'Top 50% Revenue',
            'metric': 'customer_count',
            'value': top_50_pct_revenue_customers,
            'percentage': (top_50_pct_revenue_customers / total_customers) * 100,
            'insight': f"{top_50_pct_revenue_customers} customers ({(top_50_pct_revenue_customers/total_customers)*100:.1f}%) generate 50% of revenue",
            'business_meaning': 'Core customer base driving half of business'
        })
        
        # 5. Revenue by time period (monthly)
        self.df['YearMonth'] = pd.to_datetime(self.df['InvoiceDate']).dt.to_period('M')
        monthly_revenue = self.df.groupby('YearMonth')['TotalPrice'].sum().reset_index()
        monthly_revenue['YearMonth'] = monthly_revenue['YearMonth'].astype(str)
        monthly_revenue.columns = ['year_month', 'total_revenue']
        
        # Identify peak and low months
        peak_month = monthly_revenue.loc[monthly_revenue['total_revenue'].idxmax()]
        low_month = monthly_revenue.loc[monthly_revenue['total_revenue'].idxmin()]
        
        results.append({
            'analysis_type': 'temporal',
            'dimension': 'monthly',
            'segment': peak_month['year_month'],
            'metric': 'peak_revenue',
            'value': peak_month['total_revenue'],
            'percentage': (peak_month['total_revenue'] / monthly_revenue['total_revenue'].mean()) * 100 - 100,
            'insight': f"Peak month {peak_month['year_month']}: ${peak_month['total_revenue']:,.2f}",
            'business_meaning': 'Seasonal peak or promotional success - analyze for replication'
        })
        
        monthly_revenue.to_csv('../data/eda_revenue_by_month.csv', index=False)
        log_message(f"Saved monthly revenue analysis")
        
        log_message(f"Generated {len(results)} revenue insights")
        
        return pd.DataFrame(results)
    
    def _interpret_segment_revenue(self, segment, percentage):
        """Provide business interpretation for segment revenue"""
        interpretations = {
            'Champions': 'Highest value customers - prioritize retention and upsell',
            'Loyal Customers': 'Consistent revenue source - maintain engagement',
            'Potential Loyalists': 'Growth opportunity - convert to loyal through targeted campaigns',
            'At Risk': 'Declining revenue - immediate intervention needed',
            'Lost': 'Revenue leakage - analyze churn reasons and win-back strategy',
            'Other': 'Mixed behavior - segment further for targeted approach'
        }
        
        base_interpretation = interpretations.get(segment, 'Requires further analysis')
        
        if percentage > 30:
            return f"{base_interpretation}. CRITICAL: {percentage:.1f}% revenue dependency"
        elif percentage > 15:
            return f"{base_interpretation}. SIGNIFICANT: {percentage:.1f}% revenue contribution"
        else:
            return base_interpretation
    
    def get_insights(self):
        """Return all collected insights"""
        return self.insights
    
    def analyze_customer_behavior(self):
        """
        Customer behavior analysis with RFM integration
        
        Returns:
            DataFrame with customer behavior insights
        """
        log_message("="*60)
        log_message("Analyzing Customer Behavior")
        log_message("="*60)
        
        results = []
        
        # Customer-level aggregation
        customer_metrics = self.df.groupby('CustomerID').agg({
            'InvoiceNo': 'nunique',
            'TotalPrice': ['sum', 'mean'],
            'Quantity': 'sum',
            'InvoiceDate': ['min', 'max']
        }).reset_index()
        
        customer_metrics.columns = ['CustomerID', 'purchase_frequency', 'total_spend', 
                                    'avg_order_value', 'total_quantity', 'first_purchase', 'last_purchase']
        
        # Calculate customer lifetime (days)
        customer_metrics['lifetime_days'] = (
            pd.to_datetime(customer_metrics['last_purchase']) - 
            pd.to_datetime(customer_metrics['first_purchase'])
        ).dt.days
        
        # Top customers by spend
        top_customers = customer_metrics.nlargest(10, 'total_spend')
        
        results.append({
            'analysis_type': 'customer',
            'dimension': 'top_spenders',
            'metric': 'count',
            'value': 10,
            'insight': f"Top 10 customers contribute ${top_customers['total_spend'].sum():,.2f}",
            'business_meaning': 'VIP customers requiring dedicated account management'
        })
        
        # Customer lifetime value distribution
        total_spend_median = customer_metrics['total_spend'].median()
        total_spend_mean = customer_metrics['total_spend'].mean()
        total_spend_90th = customer_metrics['total_spend'].quantile(0.9)
        
        results.append({
            'analysis_type': 'customer',
            'dimension': 'total_spend',
            'metric': 'median_total_spend',
            'value': total_spend_median,
            'insight': f"Median Customer Total Spend: ${total_spend_median:.2f}, Mean: ${total_spend_mean:.2f}, 90th percentile: ${total_spend_90th:.2f}",
            'business_meaning': 'Customer spend distribution shows value stratification'
        })
        
        # Purchase frequency patterns
        freq_median = customer_metrics['purchase_frequency'].median()
        freq_mean = customer_metrics['purchase_frequency'].mean()
        
        results.append({
            'analysis_type': 'customer',
            'dimension': 'purchase_frequency',
            'metric': 'median_frequency',
            'value': freq_median,
            'insight': f"Median purchases: {freq_median:.0f}, Mean: {freq_mean:.1f}",
            'business_meaning': 'Most customers are occasional buyers - opportunity for loyalty programs'
        })
        
        # Save customer metrics
        customer_metrics.to_csv('../data/eda_customer_metrics.csv', index=False)
        top_customers.to_csv('../data/eda_top_customers.csv', index=False)
        log_message(f"Saved customer behavior analysis")
        
        log_message(f"Generated {len(results)} customer behavior insights")
        
        return pd.DataFrame(results)
    
    def analyze_temporal_trends(self):
        """
        Temporal trend analysis with business interpretation
        
        Returns:
            DataFrame with temporal insights
        """
        log_message("="*60)
        log_message("Analyzing Temporal Trends")
        log_message("="*60)
        
        results = []
        
        # Ensure datetime
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])
        
        # Day of week analysis
        dow_revenue = self.df.groupby('DayOfWeek').agg({
            'TotalPrice': 'sum',
            'InvoiceNo': 'nunique'
        }).reset_index()
        dow_revenue.columns = ['day_of_week', 'total_revenue', 'transaction_count']
        dow_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_revenue['day_name'] = dow_revenue['day_of_week'].apply(lambda x: dow_names[x])
        
        peak_dow = dow_revenue.loc[dow_revenue['total_revenue'].idxmax()]
        low_dow = dow_revenue.loc[dow_revenue['total_revenue'].idxmin()]
        
        results.append({
            'analysis_type': 'temporal',
            'dimension': 'day_of_week',
            'metric': 'peak_day',
            'value': peak_dow['total_revenue'],
            'insight': f"Peak day: {peak_dow['day_name']} (${peak_dow['total_revenue']:,.2f})",
            'business_meaning': 'Staff and inventory planning should prioritize this day'
        })
        
        results.append({
            'analysis_type': 'temporal',
            'dimension': 'day_of_week',
            'metric': 'low_day',
            'value': low_dow['total_revenue'],
            'insight': f"Lowest day: {low_dow['day_name']} (${low_dow['total_revenue']:,.2f})",
            'business_meaning': 'Opportunity for promotional campaigns to boost sales'
        })
        
        dow_revenue.to_csv('../data/eda_revenue_by_dow.csv', index=False)
        
        # Hour of day analysis
        hour_revenue = self.df.groupby('Hour')['TotalPrice'].sum().reset_index()
        hour_revenue.columns = ['hour', 'total_revenue']
        
        peak_hour = hour_revenue.loc[hour_revenue['total_revenue'].idxmax()]
        
        results.append({
            'analysis_type': 'temporal',
            'dimension': 'hour_of_day',
            'metric': 'peak_hour',
            'value': peak_hour['total_revenue'],
            'insight': f"Peak hour: {int(peak_hour['hour'])}:00 (${peak_hour['total_revenue']:,.2f})",
            'business_meaning': 'Optimize staffing and system capacity for peak hours'
        })
        
        hour_revenue.to_csv('../data/eda_revenue_by_hour.csv', index=False)
        
        # Month-over-month growth
        if 'YearMonth' in self.df.columns:
            monthly = self.df.groupby('YearMonth')['TotalPrice'].sum().reset_index()
            monthly['YearMonth'] = monthly['YearMonth'].astype(str)
            monthly['mom_growth'] = monthly['TotalPrice'].pct_change() * 100
            
            avg_growth = monthly['mom_growth'].mean()
            
            results.append({
                'analysis_type': 'temporal',
                'dimension': 'monthly_growth',
                'metric': 'avg_mom_growth',
                'value': avg_growth,
                'insight': f"Average month-over-month growth: {avg_growth:.1f}%",
                'business_meaning': 'Positive growth' if avg_growth > 0 else 'Declining trend requires intervention'
            })
            
            monthly.to_csv('../data/eda_monthly_growth.csv', index=False)
        
        log_message(f"Saved temporal trend analysis")
        log_message(f"Generated {len(results)} temporal insights")
        
        return pd.DataFrame(results)
    
    def identify_outliers(self):
        """
        Outlier detection with reason, impact, and action
        Includes business-relevant outliers: quantity, price, high-value transactions, high spenders, abnormal frequency
        
        Returns:
            DataFrame with outlier analysis
        """
        log_message("="*60)
        log_message("Identifying Outliers")
        log_message("="*60)
        
        outliers = []
        
        # 1. Quantity outliers
        q1 = self.df['Quantity'].quantile(0.25)
        q3 = self.df['Quantity'].quantile(0.75)
        iqr = q3 - q1
        quantity_outliers = self.df[
            (self.df['Quantity'] < q1 - 3*iqr) | (self.df['Quantity'] > q3 + 3*iqr)
        ]
        
        if len(quantity_outliers) > 0:
            outliers.append({
                'outlier_type': 'quantity',
                'count': len(quantity_outliers),
                'total_value': quantity_outliers['TotalPrice'].sum(),
                'reason': f"Quantities outside 3*IQR range ({q1-3*iqr:.0f} to {q3+3*iqr:.0f})",
                'impact': f"${quantity_outliers['TotalPrice'].sum():,.2f} in unusual transactions",
                'action': 'Review for bulk orders, data errors, or fraud',
                'business_meaning': 'Potential wholesale customers or data quality issues'
            })
        
        # 2. Unit price outliers
        price_q1 = self.df['UnitPrice'].quantile(0.25)
        price_q3 = self.df['UnitPrice'].quantile(0.75)
        price_iqr = price_q3 - price_q1
        price_outliers = self.df[
            (self.df['UnitPrice'] < price_q1 - 3*price_iqr) | (self.df['UnitPrice'] > price_q3 + 3*price_iqr)
        ]
        
        if len(price_outliers) > 0:
            outliers.append({
                'outlier_type': 'unit_price',
                'count': len(price_outliers),
                'total_value': price_outliers['TotalPrice'].sum(),
                'reason': f"Prices outside 3*IQR range (${price_q1-3*price_iqr:.2f} to ${price_q3+3*price_iqr:.2f})",
                'impact': f"{len(price_outliers)} transactions with unusual pricing",
                'action': 'Verify pricing strategy, check for premium products or errors',
                'business_meaning': 'Luxury items or pricing inconsistencies'
            })
        
        # 3. Total price outliers (high-value transactions)
        total_q3 = self.df['TotalPrice'].quantile(0.75)
        total_iqr = self.df['TotalPrice'].quantile(0.75) - self.df['TotalPrice'].quantile(0.25)
        high_value_threshold = total_q3 + 3*total_iqr
        high_value_txns = self.df[self.df['TotalPrice'] > high_value_threshold]
        
        if len(high_value_txns) > 0:
            outliers.append({
                'outlier_type': 'high_value_transaction',
                'count': len(high_value_txns),
                'total_value': high_value_txns['TotalPrice'].sum(),
                'reason': f"Transactions above ${high_value_threshold:.2f}",
                'impact': f"${high_value_txns['TotalPrice'].sum():,.2f} from {len(high_value_txns)} transactions",
                'action': 'Identify VIP customers, ensure excellent service',
                'business_meaning': 'High-value customers driving significant revenue'
            })
        
        # 4. High spenders (customer-level outliers)
        customer_spend = self.df.groupby('CustomerID')['TotalPrice'].sum()
        spend_q3 = customer_spend.quantile(0.75)
        spend_iqr = customer_spend.quantile(0.75) - customer_spend.quantile(0.25)
        high_spender_threshold = spend_q3 + 3*spend_iqr
        high_spenders = customer_spend[customer_spend > high_spender_threshold]
        
        if len(high_spenders) > 0:
            outliers.append({
                'outlier_type': 'high_spender_customer',
                'count': len(high_spenders),
                'total_value': high_spenders.sum(),
                'reason': f"Customer total spend above ${high_spender_threshold:.2f}",
                'impact': f"${high_spenders.sum():,.2f} from {len(high_spenders)} customers ({(len(high_spenders)/len(customer_spend))*100:.1f}%)",
                'action': 'Assign dedicated account managers, VIP treatment, retention programs',
                'business_meaning': 'Ultra-high-value customers requiring special attention'
            })
        
        # 5. Abnormal purchase frequency (customer-level outliers)
        customer_frequency = self.df.groupby('CustomerID')['InvoiceNo'].nunique()
        freq_q3 = customer_frequency.quantile(0.75)
        freq_iqr = customer_frequency.quantile(0.75) - customer_frequency.quantile(0.25)
        high_freq_threshold = freq_q3 + 3*freq_iqr
        high_freq_customers = customer_frequency[customer_frequency > high_freq_threshold]
        
        if len(high_freq_customers) > 0:
            outliers.append({
                'outlier_type': 'abnormal_frequency',
                'count': len(high_freq_customers),
                'total_value': self.df[self.df['CustomerID'].isin(high_freq_customers.index)]['TotalPrice'].sum(),
                'reason': f"Purchase frequency above {high_freq_threshold:.0f} transactions",
                'impact': f"{len(high_freq_customers)} customers with {high_freq_customers.sum()} total purchases",
                'action': 'Analyze for business customers, resellers, or loyalty program optimization',
                'business_meaning': 'Highly engaged customers or potential B2B relationships'
            })
        
        outliers_df = pd.DataFrame(outliers)
        
        if len(outliers_df) > 0:
            outliers_df.to_csv('../data/eda_outliers.csv', index=False)
            log_message(f"Saved outlier analysis: {len(outliers)} outlier types identified")
        else:
            log_message("No significant outliers detected")
        
        return outliers_df
    
    def generate_insights_summary(self):
        """
        Generate comprehensive insights summary with business meaning
        
        Returns:
            DataFrame with all insights
        """
        log_message("="*60)
        log_message("Generating Comprehensive Insights Summary")
        log_message("="*60)
        
        all_insights = []
        
        # Run all analyses
        revenue_insights = self.analyze_revenue_patterns()
        customer_insights = self.analyze_customer_behavior()
        temporal_insights = self.analyze_temporal_trends()
        outlier_insights = self.identify_outliers()
        
        # Combine all insights
        for df in [revenue_insights, customer_insights, temporal_insights]:
            if len(df) > 0:
                all_insights.append(df)
        
        # Add outlier insights with proper structure
        if len(outlier_insights) > 0:
            outlier_formatted = outlier_insights.rename(columns={
                'outlier_type': 'dimension',
                'total_value': 'value'
            })
            outlier_formatted['analysis_type'] = 'outlier'
            outlier_formatted['metric'] = 'outlier_count'
            outlier_formatted['insight'] = outlier_formatted.apply(
                lambda x: f"{x['dimension']}: {x['count']} outliers, {x['reason']}", axis=1
            )
            all_insights.append(outlier_formatted[['analysis_type', 'dimension', 'metric', 'value', 'insight', 'business_meaning']])
        
        # Combine all
        if all_insights:
            insights_df = pd.concat(all_insights, ignore_index=True)
            
            # Add metadata
            insights_df['generated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insights_df['insight_id'] = range(1, len(insights_df) + 1)
            
            # Save comprehensive insights
            insights_df.to_csv('../data/bi_insights_summary.csv', index=False)
            log_message(f"Saved comprehensive insights summary: {len(insights_df)} insights")
            
            return insights_df
        else:
            log_message("No insights generated")
            return pd.DataFrame()


if __name__ == "__main__":
    # Test EDA Engine
    log_message("Testing EDA Engine...")
    
    # Load clean data and RFM results
    df = pd.read_csv('../data/clean_data.csv')
    rfm_df = pd.read_csv('../data/rfm_analysis.csv')
    
    log_message(f"Loaded clean data: {len(df)} rows")
    log_message(f"Loaded RFM data: {len(rfm_df)} customers")
    
    # Create EDA Engine
    eda = EDAEngine(df, rfm_df)
    
    # Run comprehensive analysis
    insights_summary = eda.generate_insights_summary()
    
    print("\nEDA Engine test completed successfully!")
    print(f"Total insights generated: {len(insights_summary)}")
    print(f"\nInsight categories:")
    print(insights_summary['analysis_type'].value_counts())
    print(f"\nSample insights:")
    print(insights_summary[['analysis_type', 'dimension', 'insight', 'business_meaning']].head(10))
