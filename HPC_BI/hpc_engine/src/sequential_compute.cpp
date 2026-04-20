#include "../include/hpc_engine.h"
#include <limits>
#include <sstream>
#include <cmath>
#include <algorithm>

// Sequential computation with meaningful business metrics
ComputationResults computeSequential(const std::vector<RetailRecord>& data) {
    auto startTime = std::chrono::high_resolution_clock::now();
    
    ComputationResults results;
    results.totalRevenue = 0.0;
    results.avgUnitPrice = 0.0;
    results.minQuantity = std::numeric_limits<int>::max();
    results.maxQuantity = std::numeric_limits<int>::min();
    results.totalRowsProcessed = data.size();
    results.highValueTransactions = 0;
    results.highValueRevenue = 0.0;
    
    double sumUnitPrice = 0.0;
    double sumRevenue = 0.0;
    double sumRevenueSquared = 0.0;
    double sumPriceSquared = 0.0;
    
    // Create a copy of revenue values for percentile calculation
    std::vector<double> revenueValues;
    revenueValues.reserve(data.size());
    
    // Pass 1: Basic aggregations and collect revenue values
    for (size_t i = 0; i < data.size(); i++) {
        double revenue = data[i].totalPrice;
        double price = data[i].unitPrice;
        int quantity = data[i].quantity;
        
        // Basic aggregations
        sumRevenue += revenue;
        sumRevenueSquared += revenue * revenue;
        sumUnitPrice += price;
        sumPriceSquared += price * price;
        
        revenueValues.push_back(revenue);
        
        // Min/Max quantity
        if (quantity < results.minQuantity) {
            results.minQuantity = quantity;
        }
        if (quantity > results.maxQuantity) {
            results.maxQuantity = quantity;
        }
    }
    
    // Calculate basic statistics
    results.totalRevenue = sumRevenue;
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
    
    // Pass 2: Count high-value transactions (above 75th percentile)
    for (size_t i = 0; i < data.size(); i++) {
        if (data[i].totalPrice >= results.highValueThreshold) {
            results.highValueTransactions++;
            results.highValueRevenue += data[i].totalPrice;
        }
    }
    
    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = endTime - startTime;
    results.computationTime = elapsed.count();
    results.totalTime = elapsed.count();
    
    std::stringstream msg;
    msg << "INFO: Sequential computation completed in " << results.computationTime << "s";
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    return results;
}
