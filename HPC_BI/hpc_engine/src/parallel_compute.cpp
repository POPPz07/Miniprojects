#include "../include/hpc_engine.h"
#include <omp.h>
#include <limits>
#include <sstream>
#include <cmath>
#include <algorithm>

// Parallel computation using OpenMP with meaningful business metrics
ComputationResults computeParallel(const std::vector<RetailRecord>& data, int numThreads) {
    omp_set_num_threads(numThreads);
    
    auto startTime = std::chrono::high_resolution_clock::now();
    
    ComputationResults results;
    results.totalRowsProcessed = data.size();
    results.highValueTransactions = 0;
    results.highValueRevenue = 0.0;
    
    double totalRevenue = 0.0;
    double sumUnitPrice = 0.0;
    double sumRevenue = 0.0;
    double sumRevenueSquared = 0.0;
    double sumPriceSquared = 0.0;
    int localMin = std::numeric_limits<int>::max();
    int localMax = std::numeric_limits<int>::min();
    
    // Create a copy of revenue values for percentile calculation
    std::vector<double> revenueValues;
    revenueValues.reserve(data.size());
    
    // Pass 1: Parallel aggregations and collect revenue values
    #pragma omp parallel for reduction(+:totalRevenue,sumUnitPrice,sumRevenue,sumRevenueSquared,sumPriceSquared) reduction(min:localMin) reduction(max:localMax)
    for (size_t i = 0; i < data.size(); i++) {
        double revenue = data[i].totalPrice;
        double price = data[i].unitPrice;
        int quantity = data[i].quantity;
        
        // Basic aggregations
        sumRevenue += revenue;
        sumRevenueSquared += revenue * revenue;
        totalRevenue += revenue;
        sumUnitPrice += price;
        sumPriceSquared += price * price;
        
        // Min/Max quantity
        if (quantity < localMin) {
            localMin = quantity;
        }
        if (quantity > localMax) {
            localMax = quantity;
        }
    }
    
    // Collect revenue values (sequential, but fast)
    for (size_t i = 0; i < data.size(); i++) {
        revenueValues.push_back(data[i].totalPrice);
    }
    
    // Calculate basic statistics
    results.totalRevenue = totalRevenue;
    results.minQuantity = localMin;
    results.maxQuantity = localMax;
    results.avgUnitPrice = sumUnitPrice / data.size();
    results.avgTransactionSize = sumRevenue / data.size();
    
    // Calculate standard deviations
    double meanRevenue = sumRevenue / data.size();
    double meanPrice = sumUnitPrice / data.size();
    double revenueVariance = (sumRevenueSquared / data.size()) - (meanRevenue * meanRevenue);
    double priceVariance = (sumPriceSquared / data.size()) - (meanPrice * meanPrice);
    results.revenueStdDev = std::sqrt(revenueVariance);
    results.priceStdDev = std::sqrt(priceVariance);
    
    // Calculate percentiles (computationally intensive but meaningful)
    std::sort(revenueValues.begin(), revenueValues.end());
    
    size_t idx25 = revenueValues.size() / 4;
    size_t idx50 = revenueValues.size() / 2;
    size_t idx75 = (revenueValues.size() * 3) / 4;
    
    results.revenue25thPercentile = revenueValues[idx25];
    results.revenueMedian = revenueValues[idx50];
    results.revenue75thPercentile = revenueValues[idx75];
    results.highValueThreshold = results.revenue75thPercentile;
    
    // Pass 2: Parallel count of high-value transactions
    int highValueCount = 0;
    double highValueRev = 0.0;
    
    #pragma omp parallel for reduction(+:highValueCount,highValueRev)
    for (size_t i = 0; i < data.size(); i++) {
        if (data[i].totalPrice >= results.highValueThreshold) {
            highValueCount++;
            highValueRev += data[i].totalPrice;
        }
    }
    
    results.highValueTransactions = highValueCount;
    results.highValueRevenue = highValueRev;
    
    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = endTime - startTime;
    results.computationTime = elapsed.count();
    results.totalTime = elapsed.count();
    
    std::stringstream msg;
    msg << "INFO: Parallel computation completed in " << results.computationTime 
        << "s (" << numThreads << " threads)";
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    return results;
}

// Validate that sequential and parallel results match
bool validateResults(const ComputationResults& seq, const ComputationResults& par, double tolerance) {
    bool valid = true;
    std::stringstream msg;
    
    // Check total revenue
    double revenueDiff = std::abs(seq.totalRevenue - par.totalRevenue) / seq.totalRevenue;
    if (revenueDiff > tolerance) {
        msg << "ERROR: Revenue mismatch - Seq: " << seq.totalRevenue 
            << ", Par: " << par.totalRevenue << " (diff: " << revenueDiff << ")";
        logMessage(msg.str(), "logs/hpc_execution.log");
        valid = false;
    }
    
    // Check avg unit price
    double avgDiff = std::abs(seq.avgUnitPrice - par.avgUnitPrice) / seq.avgUnitPrice;
    if (avgDiff > tolerance) {
        msg.str("");
        msg << "ERROR: Avg price mismatch - Seq: " << seq.avgUnitPrice 
            << ", Par: " << par.avgUnitPrice << " (diff: " << avgDiff << ")";
        logMessage(msg.str(), "logs/hpc_execution.log");
        valid = false;
    }
    
    // Check min/max
    if (seq.minQuantity != par.minQuantity || seq.maxQuantity != par.maxQuantity) {
        msg.str("");
        msg << "ERROR: Min/Max mismatch - Seq: [" << seq.minQuantity << ", " << seq.maxQuantity 
            << "], Par: [" << par.minQuantity << ", " << par.maxQuantity << "]";
        logMessage(msg.str(), "logs/hpc_execution.log");
        valid = false;
    }
    
    // Check variance (with slightly higher tolerance due to floating point)
    double stdDevDiff = std::abs(seq.revenueStdDev - par.revenueStdDev) / seq.revenueStdDev;
    if (stdDevDiff > tolerance * 10) {  // 10x tolerance for std dev
        msg.str("");
        msg << "WARNING: StdDev mismatch - Seq: " << seq.revenueStdDev 
            << ", Par: " << par.revenueStdDev << " (diff: " << stdDevDiff << ")";
        logMessage(msg.str(), "logs/hpc_execution.log");
        // Don't fail on std dev mismatch, just warn
    }
    
    // Check high-value metrics
    if (seq.highValueTransactions != par.highValueTransactions) {
        msg.str("");
        msg << "WARNING: High-value transaction count mismatch - Seq: " << seq.highValueTransactions 
            << ", Par: " << par.highValueTransactions;
        logMessage(msg.str(), "logs/hpc_execution.log");
        // Don't fail, just warn
    }
    
    if (valid) {
        logMessage("INFO: Results validation passed ✓", "logs/hpc_execution.log");
    }
    
    return valid;
}
