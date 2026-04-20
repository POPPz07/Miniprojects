#include "../include/hpc_engine.h"
#include <map>
#include <set>
#include <algorithm>
#include <sstream>
#include <omp.h>

// Compute Top-K customers by total spend
std::vector<CustomerMetric> computeTopKCustomers(const std::vector<RetailRecord>& data, int k, bool parallel) {
    auto startTime = std::chrono::high_resolution_clock::now();
    
    std::map<std::string, CustomerMetric> customerMap;
    
    if (data.empty()) {
        logMessage("WARNING: Empty dataset for Top-K customers computation", "logs/hpc_execution.log");
        return std::vector<CustomerMetric>();
    }
    
    if (parallel) {
        // Parallel aggregation using thread-local maps
        #pragma omp parallel
        {
            std::map<std::string, CustomerMetric> localMap;
            
            #pragma omp for nowait
            for (size_t i = 0; i < data.size(); i++) {
                const auto& record = data[i];
                std::string custID = record.customerID;
                
                if (localMap.find(custID) == localMap.end()) {
                    CustomerMetric metric;
                    metric.customerID = custID;
                    metric.totalSpend = 0.0;
                    metric.purchaseCount = 0;
                    metric.avgOrderValue = 0.0;
                    localMap[custID] = metric;
                }
                
                localMap[custID].totalSpend += record.totalPrice;
                localMap[custID].purchaseCount++;
            }
            
            // Merge thread-local maps into global map
            #pragma omp critical
            {
                for (auto& pair : localMap) {
                    std::string custID = pair.first;
                    if (customerMap.find(custID) == customerMap.end()) {
                        customerMap[custID] = pair.second;
                    } else {
                        customerMap[custID].totalSpend += pair.second.totalSpend;
                        customerMap[custID].purchaseCount += pair.second.purchaseCount;
                    }
                }
            }
        }
    } else {
        // Sequential aggregation
        for (const auto& record : data) {
            std::string custID = record.customerID;
            
            if (customerMap.find(custID) == customerMap.end()) {
                CustomerMetric metric;
                metric.customerID = custID;
                metric.totalSpend = 0.0;
                metric.purchaseCount = 0;
                metric.avgOrderValue = 0.0;
                customerMap[custID] = metric;
            }
            
            customerMap[custID].totalSpend += record.totalPrice;
            customerMap[custID].purchaseCount++;
        }
    }
    
    // Calculate average order value
    for (auto& pair : customerMap) {
        pair.second.avgOrderValue = pair.second.totalSpend / pair.second.purchaseCount;
    }
    
    // Convert map to vector for sorting
    std::vector<CustomerMetric> customers;
    customers.reserve(customerMap.size());
    for (const auto& pair : customerMap) {
        customers.push_back(pair.second);
    }
    
    // Sequential sorting (cannot be easily parallelized)
    std::sort(customers.begin(), customers.end(), 
              [](const CustomerMetric& a, const CustomerMetric& b) {
                  return a.totalSpend > b.totalSpend;
              });
    
    // Select top K
    int actualK = std::min(k, static_cast<int>(customers.size()));
    std::vector<CustomerMetric> topK(customers.begin(), customers.begin() + actualK);
    
    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = endTime - startTime;
    
    std::stringstream msg;
    msg << "INFO: Top-K customers computation completed in " << elapsed.count() << "s ("
        << (parallel ? "parallel" : "sequential") << ") - Top " << actualK << " of " << customers.size();
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    return topK;
}

// Compute Top-K products by total revenue
std::vector<ProductMetric> computeTopKProducts(const std::vector<RetailRecord>& data, int k, bool parallel) {
    auto startTime = std::chrono::high_resolution_clock::now();
    
    std::map<std::string, ProductMetric> productMap;
    
    if (data.empty()) {
        logMessage("WARNING: Empty dataset for Top-K products computation", "logs/hpc_execution.log");
        return std::vector<ProductMetric>();
    }
    
    if (parallel) {
        // Parallel aggregation using thread-local maps
        #pragma omp parallel
        {
            std::map<std::string, ProductMetric> localMap;
            std::map<std::string, std::set<std::string>> localCustomers;  // Track unique customers per product
            
            #pragma omp for nowait
            for (size_t i = 0; i < data.size(); i++) {
                const auto& record = data[i];
                std::string stockCode = record.stockCode;
                
                if (localMap.find(stockCode) == localMap.end()) {
                    ProductMetric metric;
                    metric.stockCode = stockCode;
                    metric.totalQuantitySold = 0;
                    metric.totalRevenue = 0.0;
                    metric.uniqueCustomers = 0;
                    localMap[stockCode] = metric;
                }
                
                localMap[stockCode].totalQuantitySold += record.quantity;
                localMap[stockCode].totalRevenue += record.totalPrice;
                localCustomers[stockCode].insert(record.customerID);
            }
            
            // Merge thread-local maps into global map
            #pragma omp critical
            {
                for (auto& pair : localMap) {
                    std::string stockCode = pair.first;
                    if (productMap.find(stockCode) == productMap.end()) {
                        productMap[stockCode] = pair.second;
                    } else {
                        productMap[stockCode].totalQuantitySold += pair.second.totalQuantitySold;
                        productMap[stockCode].totalRevenue += pair.second.totalRevenue;
                    }
                }
            }
        }
        
        // Count unique customers (sequential, but necessary)
        std::map<std::string, std::set<std::string>> allCustomers;
        for (const auto& record : data) {
            allCustomers[record.stockCode].insert(record.customerID);
        }
        for (auto& pair : productMap) {
            pair.second.uniqueCustomers = allCustomers[pair.first].size();
        }
        
    } else {
        // Sequential aggregation
        std::map<std::string, std::set<std::string>> customerSets;
        
        for (const auto& record : data) {
            std::string stockCode = record.stockCode;
            
            if (productMap.find(stockCode) == productMap.end()) {
                ProductMetric metric;
                metric.stockCode = stockCode;
                metric.totalQuantitySold = 0;
                metric.totalRevenue = 0.0;
                metric.uniqueCustomers = 0;
                productMap[stockCode] = metric;
            }
            
            productMap[stockCode].totalQuantitySold += record.quantity;
            productMap[stockCode].totalRevenue += record.totalPrice;
            customerSets[stockCode].insert(record.customerID);
        }
        
        // Count unique customers
        for (auto& pair : productMap) {
            pair.second.uniqueCustomers = customerSets[pair.first].size();
        }
    }
    
    // Convert map to vector for sorting
    std::vector<ProductMetric> products;
    products.reserve(productMap.size());
    for (const auto& pair : productMap) {
        products.push_back(pair.second);
    }
    
    // Sequential sorting
    std::sort(products.begin(), products.end(), 
              [](const ProductMetric& a, const ProductMetric& b) {
                  return a.totalRevenue > b.totalRevenue;
              });
    
    // Select top K
    int actualK = std::min(k, static_cast<int>(products.size()));
    std::vector<ProductMetric> topK(products.begin(), products.begin() + actualK);
    
    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = endTime - startTime;
    
    std::stringstream msg;
    msg << "INFO: Top-K products computation completed in " << elapsed.count() << "s ("
        << (parallel ? "parallel" : "sequential") << ") - Top " << actualK << " of " << products.size();
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    return topK;
}
