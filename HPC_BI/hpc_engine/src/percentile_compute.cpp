#include "../include/hpc_engine.h"
#include <algorithm>
#include <sstream>
#include <omp.h>

// Compute percentiles for revenue distribution
std::map<int, double> computePercentiles(const std::vector<RetailRecord>& data, const std::vector<int>& percentiles, bool parallel) {
    auto startTime = std::chrono::high_resolution_clock::now();
    
    std::map<int, double> results;
    
    if (data.empty()) {
        logMessage("WARNING: Empty dataset for percentile computation", "logs/hpc_execution.log");
        return results;
    }
    
    // Collect revenue values
    std::vector<double> revenueValues;
    revenueValues.reserve(data.size());
    
    if (parallel) {
        // Parallel data collection
        revenueValues.resize(data.size());
        #pragma omp parallel for
        for (size_t i = 0; i < data.size(); i++) {
            revenueValues[i] = data[i].totalPrice;
        }
    } else {
        // Sequential data collection
        for (const auto& record : data) {
            revenueValues.push_back(record.totalPrice);
        }
    }
    
    // Sequential sorting (required for percentiles)
    std::sort(revenueValues.begin(), revenueValues.end());
    
    // Compute requested percentiles
    size_t n = revenueValues.size();
    for (int p : percentiles) {
        if (p < 0 || p > 100) {
            std::stringstream msg;
            msg << "WARNING: Invalid percentile value: " << p << " (must be 0-100)";
            logMessage(msg.str(), "logs/hpc_execution.log");
            continue;
        }
        
        // Calculate index for percentile
        size_t idx = (n * p) / 100;
        if (idx >= n) idx = n - 1;
        
        results[p] = revenueValues[idx];
    }
    
    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = endTime - startTime;
    
    std::stringstream msg;
    msg << "INFO: Percentile computation completed in " << elapsed.count() << "s ("
        << (parallel ? "parallel" : "sequential") << ") - " << percentiles.size() << " percentiles";
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    // Log percentile values
    for (const auto& pair : results) {
        std::stringstream pMsg;
        pMsg << "INFO:   P" << pair.first << " = " << pair.second;
        logMessage(pMsg.str(), "logs/hpc_execution.log");
    }
    
    return results;
}
