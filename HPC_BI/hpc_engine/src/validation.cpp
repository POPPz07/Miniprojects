#include "../include/hpc_engine.h"
#include <cmath>
#include <sstream>

// Numerical tolerance validation for floating-point accuracy
bool validateNumericalTolerance(double value1, double value2, double tolerance) {
    if (std::isnan(value1) || std::isnan(value2)) {
        return false;
    }
    
    if (std::isinf(value1) || std::isinf(value2)) {
        return value1 == value2;  // Both must be same infinity
    }
    
    double diff = std::abs(value1 - value2);
    double maxVal = std::max(std::abs(value1), std::abs(value2));
    
    // Use relative tolerance for large values, absolute for small values
    if (maxVal > 1.0) {
        return (diff / maxVal) <= tolerance;
    } else {
        return diff <= tolerance;
    }
}

// Ground truth validation on small dataset sample
bool validateGroundTruth(const std::vector<RetailRecord>& sampleData,
                        const ComputationResults& results,
                        double tolerance) {
    if (sampleData.empty()) {
        logMessage("WARNING: Empty sample data for ground truth validation", "logs/hpc_execution.log");
        return false;
    }
    
    logMessage("============================================================", "logs/hpc_execution.log");
    logMessage("Ground Truth Validation", "logs/hpc_execution.log");
    logMessage("============================================================", "logs/hpc_execution.log");
    
    // Compute ground truth manually
    double groundTruthRevenue = 0.0;
    double groundTruthPriceSum = 0.0;
    int groundTruthMinQty = INT_MAX;
    int groundTruthMaxQty = INT_MIN;
    int groundTruthCount = 0;
    
    for (const auto& record : sampleData) {
        groundTruthRevenue += record.totalPrice;
        groundTruthPriceSum += record.unitPrice;
        groundTruthMinQty = std::min(groundTruthMinQty, record.quantity);
        groundTruthMaxQty = std::max(groundTruthMaxQty, record.quantity);
        groundTruthCount++;
    }
    
    double groundTruthAvgPrice = groundTruthPriceSum / groundTruthCount;
    
    // Validate against results (scaled to sample size)
    double sampleRatio = static_cast<double>(groundTruthCount) / results.totalRowsProcessed;
    double expectedRevenue = results.totalRevenue * sampleRatio;
    
    bool revenueValid = validateNumericalTolerance(groundTruthRevenue, expectedRevenue, tolerance);
    bool avgPriceValid = validateNumericalTolerance(groundTruthAvgPrice, results.avgUnitPrice, tolerance);
    bool minQtyValid = (groundTruthMinQty >= results.minQuantity);  // Sample min >= global min
    bool maxQtyValid = (groundTruthMaxQty <= results.maxQuantity);  // Sample max <= global max
    
    // Log validation results
    std::stringstream msg;
    msg << "Ground Truth Validation Results (sample size: " << groundTruthCount << "):";
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    msg.str("");
    msg << "  Revenue: " << (revenueValid ? "PASS" : "FAIL") 
        << " (expected: " << expectedRevenue << ", actual: " << groundTruthRevenue << ")";
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    msg.str("");
    msg << "  Avg Price: " << (avgPriceValid ? "PASS" : "FAIL")
        << " (expected: " << results.avgUnitPrice << ", actual: " << groundTruthAvgPrice << ")";
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    msg.str("");
    msg << "  Min Quantity: " << (minQtyValid ? "PASS" : "FAIL")
        << " (global: " << results.minQuantity << ", sample: " << groundTruthMinQty << ")";
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    msg.str("");
    msg << "  Max Quantity: " << (maxQtyValid ? "PASS" : "FAIL")
        << " (global: " << results.maxQuantity << ", sample: " << groundTruthMaxQty << ")";
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    bool allValid = revenueValid && avgPriceValid && minQtyValid && maxQtyValid;
    
    if (allValid) {
        logMessage("[PASS] Ground truth validation passed", "logs/hpc_execution.log");
    } else {
        logMessage("[FAIL] Ground truth validation failed", "logs/hpc_execution.log");
    }
    
    return allValid;
}
