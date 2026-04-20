#include "../include/hpc_engine.h"
#include <fstream>
#include <iomanip>
#include <sstream>

// Save scalability metrics to CSV
void saveScalabilityMetrics(const std::vector<ScalabilityMetrics>& metrics, const std::string& filename) {
    std::ofstream file(filename);
    
    if (!file.is_open()) {
        logMessage("ERROR: Cannot create file: " + filename, "logs/hpc_execution.log");
        return;
    }
    
    // Write header
    file << "data_size,seq_time,par_time,speedup,efficiency,threads\n";
    
    // Write data
    for (const auto& m : metrics) {
        file << m.dataSize << ","
             << std::fixed << std::setprecision(6) << m.seqTime << ","
             << std::fixed << std::setprecision(6) << m.parTime << ","
             << std::fixed << std::setprecision(4) << m.speedup << ","
             << std::fixed << std::setprecision(4) << m.efficiency << ","
             << m.threads << "\n";
    }
    
    file.close();
    
    // Log interpretation
    std::stringstream msg;
    msg << "INFO: Scalability metrics saved to: " << filename;
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    // Log speedup analysis
    if (!metrics.empty()) {
        const auto& lastMetric = metrics.back();
        msg.str("");
        msg << "INFO: Final speedup: " << lastMetric.speedup << "x with " << lastMetric.threads << " threads";
        logMessage(msg.str(), "logs/hpc_execution.log");
        
        if (lastMetric.speedup > 2.5) {
            logMessage("INFO: ✓ Strong parallelization achieved", "logs/hpc_execution.log");
        } else if (lastMetric.speedup > 1.5) {
            logMessage("INFO: ✓ Moderate parallelization achieved", "logs/hpc_execution.log");
        } else {
            logMessage("WARNING: Limited parallelization - overhead may dominate", "logs/hpc_execution.log");
        }
    }
}

// Save computation results summary to CSV
void saveResultsSummary(const ComputationResults& results, const std::string& filename) {
    std::ofstream file(filename);
    
    if (!file.is_open()) {
        logMessage("ERROR: Cannot create file: " + filename, "logs/hpc_execution.log");
        return;
    }
    
    // Write header
    file << "metric,value\n";
    
    // Write data
    file << "total_revenue," << std::fixed << std::setprecision(2) << results.totalRevenue << "\n";
    file << "avg_unit_price," << std::fixed << std::setprecision(2) << results.avgUnitPrice << "\n";
    file << "avg_transaction_size," << std::fixed << std::setprecision(2) << results.avgTransactionSize << "\n";
    file << "min_quantity," << results.minQuantity << "\n";
    file << "max_quantity," << results.maxQuantity << "\n";
    file << "total_rows_processed," << results.totalRowsProcessed << "\n";
    file << "revenue_std_dev," << std::fixed << std::setprecision(2) << results.revenueStdDev << "\n";
    file << "price_std_dev," << std::fixed << std::setprecision(2) << results.priceStdDev << "\n";
    file << "revenue_median," << std::fixed << std::setprecision(2) << results.revenueMedian << "\n";
    file << "revenue_25th_percentile," << std::fixed << std::setprecision(2) << results.revenue25thPercentile << "\n";
    file << "revenue_75th_percentile," << std::fixed << std::setprecision(2) << results.revenue75thPercentile << "\n";
    file << "high_value_threshold," << std::fixed << std::setprecision(2) << results.highValueThreshold << "\n";
    file << "high_value_transactions," << results.highValueTransactions << "\n";
    file << "high_value_revenue," << std::fixed << std::setprecision(2) << results.highValueRevenue << "\n";
    file << "computation_time," << std::fixed << std::setprecision(6) << results.computationTime << "\n";
    
    file.close();
    logMessage("INFO: Results summary saved to: " + filename, "logs/hpc_execution.log");
}

// Save RFM analysis results to CSV
void saveRFMAnalysis(const std::map<std::string, RFMMetrics>& rfmMetrics, const std::string& filename) {
    std::ofstream file(filename);
    
    if (!file.is_open()) {
        logMessage("ERROR: Cannot create file: " + filename, "logs/hpc_execution.log");
        return;
    }
    
    // Write header
    file << "customer_id,recency,frequency,monetary,r_score,f_score,m_score,rfm_score,segment\n";
    
    // Write data
    for (const auto& pair : rfmMetrics) {
        const RFMMetrics& rfm = pair.second;
        file << rfm.customerID << ","
             << rfm.recency << ","
             << rfm.frequency << ","
             << std::fixed << std::setprecision(2) << rfm.monetary << ","
             << rfm.rScore << ","
             << rfm.fScore << ","
             << rfm.mScore << ","
             << rfm.rfmScore << ","
             << rfm.segment << "\n";
    }
    
    file.close();
    
    std::stringstream msg;
    msg << "INFO: RFM analysis saved to: " << filename << " (" << rfmMetrics.size() << " customers)";
    logMessage(msg.str(), "logs/hpc_execution.log");
}

// Save correlation results to CSV
void saveCorrelationResults(double correlation, const std::string& filename) {
    std::ofstream file(filename);
    
    if (!file.is_open()) {
        logMessage("ERROR: Cannot create file: " + filename, "logs/hpc_execution.log");
        return;
    }
    
    // Write header
    file << "metric,value\n";
    
    // Write data
    file << "quantity_unitprice_correlation," << std::fixed << std::setprecision(6) << correlation << "\n";
    
    file.close();
    logMessage("INFO: Correlation results saved to: " + filename, "logs/hpc_execution.log");
}

// Save Top-K analysis results to CSV
void saveTopKResults(const std::vector<CustomerMetric>& topCustomers,
                     const std::vector<ProductMetric>& topProducts,
                     const std::string& filename) {
    std::ofstream file(filename);
    
    if (!file.is_open()) {
        logMessage("ERROR: Cannot create file: " + filename, "logs/hpc_execution.log");
        return;
    }
    
    // Write Top-K Customers
    file << "=== TOP CUSTOMERS ===\n";
    file << "customer_id,total_spend,purchase_count,avg_order_value\n";
    for (const auto& customer : topCustomers) {
        file << customer.customerID << ","
             << std::fixed << std::setprecision(2) << customer.totalSpend << ","
             << customer.purchaseCount << ","
             << std::fixed << std::setprecision(2) << customer.avgOrderValue << "\n";
    }
    
    file << "\n=== TOP PRODUCTS ===\n";
    file << "stock_code,total_quantity_sold,total_revenue,unique_customers\n";
    for (const auto& product : topProducts) {
        file << product.stockCode << ","
             << product.totalQuantitySold << ","
             << std::fixed << std::setprecision(2) << product.totalRevenue << ","
             << product.uniqueCustomers << "\n";
    }
    
    file.close();
    
    std::stringstream msg;
    msg << "INFO: Top-K analysis saved to: " << filename 
        << " (Top " << topCustomers.size() << " customers, Top " << topProducts.size() << " products)";
    logMessage(msg.str(), "logs/hpc_execution.log");
}

// Save percentile results to CSV
void savePercentileResults(const std::map<int, double>& percentiles, const std::string& filename) {
    std::ofstream file(filename);
    
    if (!file.is_open()) {
        logMessage("ERROR: Cannot create file: " + filename, "logs/hpc_execution.log");
        return;
    }
    
    // Write header
    file << "percentile,value\n";
    
    // Write data
    for (const auto& pair : percentiles) {
        file << pair.first << ","
             << std::fixed << std::setprecision(2) << pair.second << "\n";
    }
    
    file.close();
    logMessage("INFO: Percentile results saved to: " + filename, "logs/hpc_execution.log");
}

// Save moving average results to CSV
void saveMovingAverageResults(const std::vector<double>& movingAvg7,
                              const std::vector<double>& movingAvg30,
                              const std::string& filename) {
    std::ofstream file(filename);
    
    if (!file.is_open()) {
        logMessage("ERROR: Cannot create file: " + filename, "logs/hpc_execution.log");
        return;
    }
    
    // Write header
    file << "day_index,moving_avg_7day,moving_avg_30day\n";
    
    // Write data (use the longer vector's size)
    size_t maxSize = std::max(movingAvg7.size(), movingAvg30.size());
    for (size_t i = 0; i < maxSize; i++) {
        file << i << ",";
        
        if (i < movingAvg7.size()) {
            file << std::fixed << std::setprecision(2) << movingAvg7[i];
        } else {
            file << "NA";
        }
        file << ",";
        
        if (i < movingAvg30.size()) {
            file << std::fixed << std::setprecision(2) << movingAvg30[i];
        } else {
            file << "NA";
        }
        file << "\n";
    }
    
    file.close();
    
    std::stringstream msg;
    msg << "INFO: Moving average results saved to: " << filename 
        << " (" << movingAvg7.size() << " 7-day points, " << movingAvg30.size() << " 30-day points)";
    logMessage(msg.str(), "logs/hpc_execution.log");
}
