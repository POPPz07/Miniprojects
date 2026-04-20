#include "../include/hpc_engine.h"
#include <cmath>
#include <sstream>
#include <omp.h>

// Compute Pearson correlation coefficient between Quantity and UnitPrice
double computeCorrelation(const std::vector<RetailRecord>& data, bool parallel) {
    auto startTime = std::chrono::high_resolution_clock::now();
    
    if (data.empty()) {
        logMessage("WARNING: Empty dataset for correlation computation", "logs/hpc_execution.log");
        return 0.0;
    }
    
    size_t n = data.size();
    double sumX = 0.0, sumY = 0.0, sumXY = 0.0, sumX2 = 0.0, sumY2 = 0.0;
    
    if (parallel) {
        // Parallel reduction for sum components
        #pragma omp parallel for reduction(+:sumX,sumY,sumXY,sumX2,sumY2)
        for (size_t i = 0; i < n; i++) {
            double x = static_cast<double>(data[i].quantity);
            double y = data[i].unitPrice;
            
            sumX += x;
            sumY += y;
            sumXY += x * y;
            sumX2 += x * x;
            sumY2 += y * y;
        }
    } else {
        // Sequential computation
        for (size_t i = 0; i < n; i++) {
            double x = static_cast<double>(data[i].quantity);
            double y = data[i].unitPrice;
            
            sumX += x;
            sumY += y;
            sumXY += x * y;
            sumX2 += x * x;
            sumY2 += y * y;
        }
    }
    
    // Compute correlation coefficient
    // r = (n*sumXY - sumX*sumY) / sqrt((n*sumX2 - sumX^2) * (n*sumY2 - sumY^2))
    double numerator = n * sumXY - sumX * sumY;
    double denomX = n * sumX2 - sumX * sumX;
    double denomY = n * sumY2 - sumY * sumY;
    
    // Check for numerical stability
    if (denomX <= 0 || denomY <= 0) {
        logMessage("WARNING: Invalid denominator in correlation computation", "logs/hpc_execution.log");
        return 0.0;
    }
    
    double denominator = std::sqrt(denomX * denomY);
    
    if (denominator == 0) {
        logMessage("WARNING: Zero denominator in correlation computation", "logs/hpc_execution.log");
        return 0.0;
    }
    
    double correlation = numerator / denominator;
    
    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = endTime - startTime;
    
    std::stringstream msg;
    msg << "INFO: Correlation computation completed in " << elapsed.count() << "s ("
        << (parallel ? "parallel" : "sequential") << ") - Correlation: " << correlation;
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    return correlation;
}
