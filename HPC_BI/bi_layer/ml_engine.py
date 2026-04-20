"""
ML Engine Module
Machine Learning models for customer classification and segmentation
"""

import pandas as pd
import numpy as np
from datetime import datetime
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, silhouette_score

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


class MLEngine:
    """
    Machine Learning Engine for customer analytics
    Implements classification and clustering models
    """
    
    def __init__(self, df):
        """
        Initialize ML Engine
        
        Args:
            df: Clean transaction data
        """
        self.df = df.copy()
        self.classification_model = None
        self.clustering_model = None
        self.scaler = None
        self.classification_results = None
        self.clustering_results = None
        
        log_message("MLEngine initialized")
    
    def train_classification_model(self):
        """
        Train classification model for high-value customer prediction
        Uses behavioral features only (no direct monetary features) to avoid data leakage
        
        Returns:
            DataFrame with classification results and metrics
        """
        log_message("="*60)
        log_message("Training Classification Model for High-Value Customers")
        log_message("="*60)
        
        # Feature engineering at customer level
        customer_features = self.df.groupby('CustomerID').agg({
            'TotalPrice': 'sum',
            'InvoiceNo': 'nunique',
            'Quantity': ['mean', 'sum'],
            'UnitPrice': 'mean',
            'InvoiceDate': ['min', 'max']
        }).reset_index()
        
        customer_features.columns = ['CustomerID', 'total_spend', 'purchase_count', 
                                     'avg_quantity', 'total_quantity', 'avg_unit_price',
                                     'first_purchase', 'last_purchase']
        
        # Calculate customer lifetime (days)
        customer_features['customer_lifetime_days'] = (
            pd.to_datetime(customer_features['last_purchase']) - 
            pd.to_datetime(customer_features['first_purchase'])
        ).dt.days + 1  # Add 1 to avoid zero
        
        # Calculate purchase frequency rate (purchases per day)
        customer_features['purchase_frequency_rate'] = (
            customer_features['purchase_count'] / customer_features['customer_lifetime_days']
        )
        
        log_message(f"Engineered behavioral features for {len(customer_features)} customers")
        
        # Define high-value threshold at 75th percentile
        threshold = customer_features['total_spend'].quantile(0.75)
        customer_features['is_high_value'] = (customer_features['total_spend'] >= threshold).astype(int)
        
        high_value_count = customer_features['is_high_value'].sum()
        log_message(f"High-value threshold: ${threshold:.2f}")
        log_message(f"High-value customers: {high_value_count} ({(high_value_count/len(customer_features))*100:.1f}%)")
        
        # Prepare features and target (EXCLUDE total_spend to avoid data leakage)
        X = customer_features[['purchase_count', 'avg_quantity', 'total_quantity', 
                               'avg_unit_price', 'customer_lifetime_days', 'purchase_frequency_rate']]
        y = customer_features['is_high_value']
        
        log_message("Using behavioral features only (no direct monetary features):")
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        
        log_message(f"Training set: {len(X_train)} samples")
        log_message(f"Test set: {len(X_test)} samples")
        
        # Train RandomForestClassifier
        log_message("Training RandomForestClassifier with 100 estimators...")
        self.classification_model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5
        )
        
        self.classification_model.fit(X_train, y_train)
        
        # Predictions
        y_pred = self.classification_model.predict(X_test)
        
        # Compute metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        log_message(f"Classification Metrics:")
        log_message(f"  Accuracy:  {accuracy:.4f}")
        log_message(f"  Precision: {precision:.4f}")
        log_message(f"  Recall:    {recall:.4f}")
        log_message(f"  F1-Score:  {f1:.4f}")
        
        # Feature importance
        feature_names = ['purchase_count', 'avg_quantity', 'total_quantity', 
                        'avg_unit_price', 'customer_lifetime_days', 'purchase_frequency_rate']
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': self.classification_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        log_message("Feature Importance (behavioral features only):")
        for _, row in feature_importance.iterrows():
            log_message(f"  {row['feature']}: {row['importance']:.4f}")
        
        # Predict for all customers
        customer_features['predicted_high_value'] = self.classification_model.predict(X)
        customer_features['prediction_probability'] = self.classification_model.predict_proba(X)[:, 1]
        
        # Store results
        self.classification_results = {
            'customer_predictions': customer_features,
            'metrics': {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'high_value_threshold': threshold,
                'high_value_count': high_value_count
            },
            'feature_importance': feature_importance
        }
        
        log_message("Classification model training completed")
        
        return customer_features
    
    def train_clustering_model(self):
        """
        Train clustering model for customer segmentation
        
        Returns:
            DataFrame with clustering results
        """
        log_message("="*60)
        log_message("Training Clustering Model for Customer Segmentation")
        log_message("="*60)
        
        # Feature engineering: RFM-like features
        customer_features = self.df.groupby('CustomerID').agg({
            'TotalPrice': 'sum',
            'InvoiceNo': 'nunique',
            'InvoiceDate': 'max'
        }).reset_index()
        
        customer_features.columns = ['CustomerID', 'monetary', 'frequency', 'last_purchase']
        
        # Calculate recency
        reference_date = pd.to_datetime(self.df['InvoiceDate']).max()
        customer_features['recency'] = (reference_date - pd.to_datetime(customer_features['last_purchase'])).dt.days
        
        log_message(f"Engineered RFM features for {len(customer_features)} customers")
        
        # Prepare features for clustering
        X = customer_features[['monetary', 'frequency', 'recency']]
        
        # Standardize features
        log_message("Standardizing features using StandardScaler...")
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Determine optimal cluster count using elbow method and silhouette score
        log_message("Determining optimal cluster count...")
        inertias = []
        silhouette_scores = []
        K_range = range(2, 11)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
        
        # Log silhouette scores for key cluster counts
        log_message("Silhouette scores for different cluster counts:")
        for k in [2, 3, 4]:
            if k <= max(K_range):
                idx = k - min(K_range)
                log_message(f"  K={k}: {silhouette_scores[idx]:.4f}")
        
        # Evaluate cluster distributions for K=2, 3, 4
        log_message("Evaluating cluster distributions:")
        candidate_k = None
        best_balance_score = -1
        
        for k in [2, 3, 4]:
            kmeans_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels_temp = kmeans_temp.fit_predict(X_scaled)
            counts = pd.Series(labels_temp).value_counts()
            min_cluster_pct = (counts.min() / len(labels_temp)) * 100
            silh = silhouette_scores[k - min(K_range)]
            
            # Balance score: prefer higher silhouette but penalize extreme imbalance
            # Require at least 5% in smallest cluster for interpretability
            balance_score = silh if min_cluster_pct >= 5.0 else silh * 0.5
            
            log_message(f"  K={k}: silhouette={silh:.4f}, min_cluster={min_cluster_pct:.1f}%, balance_score={balance_score:.4f}")
            
            if balance_score > best_balance_score:
                best_balance_score = balance_score
                candidate_k = k
        
        # Select optimal K based on balance between silhouette score and interpretability
        optimal_k = candidate_k if candidate_k else K_range[np.argmax(silhouette_scores)]
        optimal_silhouette = silhouette_scores[optimal_k - min(K_range)]
        
        log_message(f"Selected cluster count: {optimal_k} (balanced and interpretable)")
        log_message(f"Silhouette score: {optimal_silhouette:.4f}")
        
        # Train final KMeans model
        log_message(f"Training KMeans with {optimal_k} clusters...")
        self.clustering_model = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        customer_features['cluster'] = self.clustering_model.fit_predict(X_scaled)
        
        # Cluster distribution
        cluster_counts = customer_features['cluster'].value_counts().sort_index()
        log_message("Cluster Distribution:")
        for cluster_id, count in cluster_counts.items():
            log_message(f"  Cluster {cluster_id}: {count} customers ({(count/len(customer_features))*100:.1f}%)")
        
        # Store results
        self.clustering_results = {
            'customer_clusters': customer_features,
            'metrics': {
                'optimal_k': optimal_k,
                'silhouette_score': optimal_silhouette,
                'inertias': inertias,
                'silhouette_scores': silhouette_scores
            }
        }
        
        log_message("Clustering model training completed")
        
        return customer_features
    
    def interpret_clusters(self):
        """
        Interpret clusters with business-meaningful names
        
        Returns:
            DataFrame with cluster profiles and interpretations
        """
        log_message("="*60)
        log_message("Interpreting Clusters")
        log_message("="*60)
        
        if self.clustering_results is None:
            log_message("ERROR: No clustering results available. Train clustering model first.")
            return None
        
        customer_clusters = self.clustering_results['customer_clusters']
        
        # Compute cluster profiles
        cluster_profiles = customer_clusters.groupby('cluster').agg({
            'CustomerID': 'count',
            'monetary': 'mean',
            'frequency': 'mean',
            'recency': 'mean'
        }).reset_index()
        
        cluster_profiles.columns = ['cluster', 'customer_count', 'avg_spend', 'avg_frequency', 'avg_recency']
        
        # Assign business-meaningful names based on profiles
        def assign_cluster_name(row):
            spend_high = row['avg_spend'] > cluster_profiles['avg_spend'].quantile(0.66)
            spend_low = row['avg_spend'] < cluster_profiles['avg_spend'].quantile(0.33)
            freq_high = row['avg_frequency'] > cluster_profiles['avg_frequency'].quantile(0.66)
            freq_low = row['avg_frequency'] < cluster_profiles['avg_frequency'].quantile(0.33)
            recency_recent = row['avg_recency'] < cluster_profiles['avg_recency'].quantile(0.33)
            recency_old = row['avg_recency'] > cluster_profiles['avg_recency'].quantile(0.66)
            
            # High spend clusters
            if spend_high:
                if freq_high:
                    return "High-Value Frequent"
                elif recency_recent:
                    return "High-Value Recent"
                else:
                    return "High-Value Occasional"
            # Low spend clusters
            elif spend_low:
                if recency_old:
                    return "Low-Value Dormant"
                elif freq_low:
                    return "Low-Value Infrequent"
                else:
                    return "Low-Value Active"
            # Medium spend clusters
            else:
                if recency_recent and freq_high:
                    return "Medium-Value Loyal"
                elif recency_old:
                    return "Medium-Value At-Risk"
                else:
                    return "Medium-Value Regular"
        
        cluster_profiles['cluster_name'] = cluster_profiles.apply(assign_cluster_name, axis=1)
        
        # Generate business meaning
        def generate_business_meaning(row):
            meanings = {
                "High-Value Frequent": "Premium customers with high spend and frequent purchases - prioritize retention and VIP treatment",
                "High-Value Recent": "High spenders with recent activity - maintain engagement and upsell opportunities",
                "High-Value Occasional": "High spenders with infrequent purchases - increase engagement to boost frequency",
                "Medium-Value Loyal": "Consistent mid-tier customers - upsell opportunities and loyalty rewards",
                "Medium-Value Regular": "Steady mid-tier customers - maintain relationship and explore growth",
                "Medium-Value At-Risk": "Mid-tier customers showing signs of churn - re-engagement campaigns needed",
                "Low-Value Dormant": "Inactive low-value customers - win-back campaigns or deprioritize",
                "Low-Value Infrequent": "Infrequent low-value customers - assess retention value",
                "Low-Value Active": "Active but low-spending customers - nurture for growth potential"
            }
            return meanings.get(row['cluster_name'], "Requires further analysis")
        
        cluster_profiles['business_meaning'] = cluster_profiles.apply(generate_business_meaning, axis=1)
        
        log_message("Cluster Profiles:")
        for _, row in cluster_profiles.iterrows():
            log_message(f"  Cluster {row['cluster']}: {row['cluster_name']}")
            log_message(f"    Customers: {row['customer_count']}")
            log_message(f"    Avg Spend: ${row['avg_spend']:.2f}")
            log_message(f"    Avg Frequency: {row['avg_frequency']:.1f}")
            log_message(f"    Avg Recency: {row['avg_recency']:.0f} days")
            log_message(f"    Meaning: {row['business_meaning']}")
        
        # Add cluster names to customer data
        cluster_name_map = cluster_profiles.set_index('cluster')['cluster_name'].to_dict()
        customer_clusters['cluster_name'] = customer_clusters['cluster'].map(cluster_name_map)
        
        self.clustering_results['cluster_profiles'] = cluster_profiles
        self.clustering_results['customer_clusters'] = customer_clusters
        
        log_message("Cluster interpretation completed")
        
        return cluster_profiles
    
    def validate_models(self):
        """
        Validate ML models against quality thresholds
        
        Returns:
            dict with validation results
        """
        log_message("="*60)
        log_message("Validating ML Models")
        log_message("="*60)
        
        validation_results = {
            'classification_valid': False,
            'clustering_valid': False,
            'customer_count_consistent': False
        }
        
        # Validate classification accuracy > 70%
        if self.classification_results is not None:
            accuracy = self.classification_results['metrics']['accuracy']
            if accuracy > 0.70:
                log_message(f"[PASS] Classification accuracy {accuracy:.4f} > 0.70")
                validation_results['classification_valid'] = True
            else:
                log_message(f"[FAIL] Classification accuracy {accuracy:.4f} <= 0.70")
        else:
            log_message("[SKIP] Classification model not trained")
        
        # Validate clustering silhouette score > 0.3
        if self.clustering_results is not None:
            silhouette = self.clustering_results['metrics']['silhouette_score']
            if silhouette > 0.3:
                log_message(f"[PASS] Clustering silhouette score {silhouette:.4f} > 0.30")
                validation_results['clustering_valid'] = True
            else:
                log_message(f"[FAIL] Clustering silhouette score {silhouette:.4f} <= 0.30")
        else:
            log_message("[SKIP] Clustering model not trained")
        
        # Validate customer counts match
        if self.classification_results is not None and self.clustering_results is not None:
            class_count = len(self.classification_results['customer_predictions'])
            cluster_count = len(self.clustering_results['customer_clusters'])
            
            if class_count == cluster_count:
                log_message(f"[PASS] Customer counts match: {class_count}")
                validation_results['customer_count_consistent'] = True
            else:
                log_message(f"[FAIL] Customer count mismatch: classification={class_count}, clustering={cluster_count}")
        else:
            log_message("[SKIP] Customer count validation (models not trained)")
        
        log_message("Model validation completed")
        
        return validation_results
    
    def get_results(self):
        """
        Get all ML results for export
        
        Returns:
            dict with classification and clustering results
        """
        return {
            'classification': self.classification_results,
            'clustering': self.clustering_results
        }


if __name__ == "__main__":
    # Test ML Engine
    log_message("Testing ML Engine...")
    
    # Load clean data
    df = pd.read_csv('../data/clean_data.csv')
    log_message(f"Loaded clean data: {len(df)} rows")
    
    # Create ML Engine
    ml_engine = MLEngine(df)
    
    # Train classification model
    classification_results = ml_engine.train_classification_model()
    
    # Train clustering model
    clustering_results = ml_engine.train_clustering_model()
    
    # Interpret clusters
    cluster_profiles = ml_engine.interpret_clusters()
    
    # Validate models
    validation = ml_engine.validate_models()
    
    print("\nML Engine test completed successfully!")
    print(f"Classification accuracy: {ml_engine.classification_results['metrics']['accuracy']:.4f}")
    print(f"Clustering silhouette score: {ml_engine.clustering_results['metrics']['silhouette_score']:.4f}")
    print(f"Optimal clusters: {ml_engine.clustering_results['metrics']['optimal_k']}")
