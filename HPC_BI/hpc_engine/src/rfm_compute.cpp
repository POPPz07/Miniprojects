#include "../include/hpc_engine.h"
#include <map>
#include <unordered_map>
#include <algorithm>
#include <sstream>
#include <ctime>
#include <iomanip>
#include <vector>
#include <omp.h>

// Helper function to parse date string and get days since epoch
int dateToEpochDays(const std::string& dateStr) {
    // Expected format: "DD/MM/YYYY HH:MM" or similar
    // Simplified: extract day, month, year
    std::tm tm = {};
    std::istringstream ss(dateStr);
    
    // Try parsing format: DD/MM/YYYY HH:MM
    char delimiter;
    ss >> tm.tm_mday >> delimiter >> tm.tm_mon >> delimiter >> tm.tm_year;
    
    if (ss.fail()) {
        return 0;  // Return 0 for invalid dates
    }
    
    tm.tm_mon -= 1;  // Month is 0-indexed
    tm.tm_year -= 1900;  // Year since 1900
    tm.tm_hour = 0;
    tm.tm_min = 0;
    tm.tm_sec = 0;
    
    std::time_t time = std::mktime(&tm);
    return static_cast<int>(time / 86400);  // Convert to days
}

// Get most recent date from dataset
std::string getMostRecentDate(const std::vector<RetailRecord>& data) {
    if (data.empty()) return "";
    
    std::string mostRecent = data[0].invoiceDate;
    int mostRecentDays = dateToEpochDays(mostRecent);
    
    for (const auto& record : data) {
        int days = dateToEpochDays(record.invoiceDate);
        if (days > mostRecentDays) {
            mostRecentDays = days;
            mostRecent = record.invoiceDate;
        }
    }
    
    return mostRecent;
}

// Calculate days between two dates
int daysBetween(const std::string& date1, const std::string& date2) {
    int days1 = dateToEpochDays(date1);
    int days2 = dateToEpochDays(date2);
    return std::abs(days2 - days1);
}

// Compute RFM scores using quintile-based scoring
void computeRFMScores(std::map<std::string, RFMMetrics>& rfmMap) {
    if (rfmMap.empty()) return;
    
    // Collect all values for quintile calculation
    std::vector<int> recencyValues;
    std::vector<int> frequencyValues;
    std::vector<double> monetaryValues;
    
    for (const auto& pair : rfmMap) {
        recencyValues.push_back(pair.second.recency);
        frequencyValues.push_back(pair.second.frequency);
        monetaryValues.push_back(pair.second.monetary);
    }
    
    // Sort for quintile calculation
    std::sort(recencyValues.begin(), recencyValues.end());
    std::sort(frequencyValues.begin(), frequencyValues.end());
    std::sort(monetaryValues.begin(), monetaryValues.end());
    
    // Calculate quintile thresholds
    size_t n = recencyValues.size();
    int r20 = recencyValues[n / 5];
    int r40 = recencyValues[2 * n / 5];
    int r60 = recencyValues[3 * n / 5];
    int r80 = recencyValues[4 * n / 5];
    
    int f20 = frequencyValues[n / 5];
    int f40 = frequencyValues[2 * n / 5];
    int f60 = frequencyValues[3 * n / 5];
    int f80 = frequencyValues[4 * n / 5];
    
    double m20 = monetaryValues[n / 5];
    double m40 = monetaryValues[2 * n / 5];
    double m60 = monetaryValues[3 * n / 5];
    double m80 = monetaryValues[4 * n / 5];
    
    // Assign scores (1-5) to each customer
    for (auto& pair : rfmMap) {
        RFMMetrics& rfm = pair.second;
        
        // Recency: Lower is better (5 = most recent)
        if (rfm.recency <= r20) rfm.rScore = 5;
        else if (rfm.recency <= r40) rfm.rScore = 4;
        else if (rfm.recency <= r60) rfm.rScore = 3;
        else if (rfm.recency <= r80) rfm.rScore = 2;
        else rfm.rScore = 1;
        
        // Frequency: Higher is better (5 = most frequent)
        if (rfm.frequency >= f80) rfm.fScore = 5;
        else if (rfm.frequency >= f60) rfm.fScore = 4;
        else if (rfm.frequency >= f40) rfm.fScore = 3;
        else if (rfm.frequency >= f20) rfm.fScore = 2;
        else rfm.fScore = 1;
        
        // Monetary: Higher is better (5 = highest spend)
        if (rfm.monetary >= m80) rfm.mScore = 5;
        else if (rfm.monetary >= m60) rfm.mScore = 4;
        else if (rfm.monetary >= m40) rfm.mScore = 3;
        else if (rfm.monetary >= m20) rfm.mScore = 2;
        else rfm.mScore = 1;
        
        // Create combined RFM score string
        rfm.rfmScore = std::to_string(rfm.rScore) + std::to_string(rfm.fScore) + std::to_string(rfm.mScore);
        
        // Assign segment based on RFM scores
        if (rfm.rScore >= 4 && rfm.fScore >= 4 && rfm.mScore >= 4) {
            rfm.segment = "Champions";
        } else if (rfm.fScore >= 4 && rfm.mScore >= 4) {
            rfm.segment = "Loyal Customers";
        } else if (rfm.rScore >= 4 && rfm.fScore <= 3) {
            rfm.segment = "Potential Loyalists";
        } else if (rfm.rScore <= 2 && rfm.fScore >= 3) {
            rfm.segment = "At Risk";
        } else if (rfm.rScore <= 2 && rfm.fScore <= 2) {
            rfm.segment = "Lost";
        } else {
            rfm.segment = "Other";
        }
    }
}

// Compute RFM metrics for all customers
std::map<std::string, RFMMetrics> computeRFMMetrics(const std::vector<RetailRecord>& data, bool parallel) {
    auto startTime = std::chrono::high_resolution_clock::now();
    
    std::map<std::string, RFMMetrics> rfmMap;
    
    if (data.empty()) {
        logMessage("WARNING: Empty dataset for RFM computation", "logs/hpc_execution.log");
        return rfmMap;
    }
    
    // Get reference date (most recent date in dataset)
    std::string referenceDate = getMostRecentDate(data);
    int referenceDays = dateToEpochDays(referenceDate);
    
    logMessage("INFO: Computing RFM metrics with reference date: " + referenceDate, "logs/hpc_execution.log");
    
    if (parallel) {
        // OPTIMIZATION 1: Use unordered_map for better cache performance
        // OPTIMIZATION 2: Collect thread-local results in vectors to reduce critical section time
        std::vector<std::unordered_map<std::string, RFMMetrics>> threadMaps;
        int numThreads = omp_get_max_threads();
        threadMaps.resize(numThreads);
        
        #pragma omp parallel
        {
            int threadID = omp_get_thread_num();
            std::unordered_map<std::string, RFMMetrics>& localMap = threadMaps[threadID];
            
            // OPTIMIZATION 3: Reserve space to reduce rehashing
            localMap.reserve(data.size() / numThreads + 100);
            
            #pragma omp for nowait schedule(static)
            for (size_t i = 0; i < data.size(); i++) {
                const auto& record = data[i];
                const std::string& custID = record.customerID;
                
                // OPTIMIZATION 4: Use find once and reuse iterator
                auto it = localMap.find(custID);
                if (it == localMap.end()) {
                    // Initialize new customer
                    RFMMetrics rfm;
                    rfm.customerID = custID;
                    rfm.recency = 999999;  // Start with large value for min comparison
                    rfm.frequency = 0;
                    rfm.monetary = 0.0;
                    it = localMap.insert({custID, rfm}).first;
                }
                
                // Update metrics
                int recordDays = dateToEpochDays(record.invoiceDate);
                int daysSincePurchase = referenceDays - recordDays;
                
                // Recency: minimum days since last purchase
                if (daysSincePurchase < it->second.recency) {
                    it->second.recency = daysSincePurchase;
                }
                
                // Frequency: count of purchases
                it->second.frequency++;
                
                // Monetary: total spend
                it->second.monetary += record.totalPrice;
            }
        }
        
        // OPTIMIZATION 5: Optimized merging strategy - merge thread maps sequentially
        // This reduces contention and is more cache-friendly
        std::unordered_map<std::string, RFMMetrics> mergedMap;
        
        // Estimate total size for better memory allocation
        size_t estimatedSize = 0;
        for (const auto& threadMap : threadMaps) {
            estimatedSize += threadMap.size();
        }
        mergedMap.reserve(estimatedSize / 2);  // Estimate unique customers
        
        for (const auto& threadMap : threadMaps) {
            for (const auto& pair : threadMap) {
                const std::string& custID = pair.first;
                const RFMMetrics& threadRFM = pair.second;
                
                auto it = mergedMap.find(custID);
                if (it == mergedMap.end()) {
                    mergedMap[custID] = threadRFM;
                } else {
                    // Merge: min recency, sum frequency and monetary
                    if (threadRFM.recency < it->second.recency) {
                        it->second.recency = threadRFM.recency;
                    }
                    it->second.frequency += threadRFM.frequency;
                    it->second.monetary += threadRFM.monetary;
                }
            }
        }
        
        // Convert unordered_map to map for consistent ordering
        for (const auto& pair : mergedMap) {
            rfmMap[pair.first] = pair.second;
        }
        
    } else {
        // Sequential aggregation
        for (const auto& record : data) {
            std::string custID = record.customerID;
            
            if (rfmMap.find(custID) == rfmMap.end()) {
                // Initialize new customer
                RFMMetrics rfm;
                rfm.customerID = custID;
                rfm.recency = 0;
                rfm.frequency = 0;
                rfm.monetary = 0.0;
                rfmMap[custID] = rfm;
            }
            
            // Update metrics
            int recordDays = dateToEpochDays(record.invoiceDate);
            int daysSincePurchase = referenceDays - recordDays;
            
            // Recency: minimum days since last purchase
            if (rfmMap[custID].recency == 0 || daysSincePurchase < rfmMap[custID].recency) {
                rfmMap[custID].recency = daysSincePurchase;
            }
            
            // Frequency: count of purchases
            rfmMap[custID].frequency++;
            
            // Monetary: total spend
            rfmMap[custID].monetary += record.totalPrice;
        }
    }
    
    // Compute RFM scores and segments
    computeRFMScores(rfmMap);
    
    // Validate RFM metrics
    for (const auto& pair : rfmMap) {
        const RFMMetrics& rfm = pair.second;
        if (rfm.recency < 0 || rfm.frequency < 1 || rfm.monetary <= 0) {
            std::stringstream msg;
            msg << "WARNING: Invalid RFM metrics for customer " << rfm.customerID
                << " (R=" << rfm.recency << ", F=" << rfm.frequency << ", M=" << rfm.monetary << ")";
            logMessage(msg.str(), "logs/hpc_execution.log");
        }
    }
    
    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = endTime - startTime;
    
    std::stringstream msg;
    msg << "INFO: RFM computation completed in " << elapsed.count() << "s ("
        << (parallel ? "parallel" : "sequential") << ") - " << rfmMap.size() << " customers";
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    // Log segment distribution
    std::map<std::string, int> segmentCounts;
    for (const auto& pair : rfmMap) {
        segmentCounts[pair.second.segment]++;
    }
    
    for (const auto& pair : segmentCounts) {
        std::stringstream segMsg;
        segMsg << "INFO:   " << pair.first << ": " << pair.second << " customers";
        logMessage(segMsg.str(), "logs/hpc_execution.log");
    }
    
    return rfmMap;
}
