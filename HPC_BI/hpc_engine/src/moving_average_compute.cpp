#include "../include/hpc_engine.h"
#include <map>
#include <algorithm>
#include <sstream>
#include <omp.h>

// Helper structure for time-series data
struct TimeSeriesPoint {
    std::string date;
    double revenue;
    int epochDays;
};

// Helper function to parse date (from rfm_compute.cpp)
extern int dateToEpochDays(const std::string& dateStr);

// Compute moving average for revenue time series
std::vector<double> computeMovingAverage(const std::vector<RetailRecord>& data, int windowSize, bool parallel) {
    auto startTime = std::chrono::high_resolution_clock::now();
    
    std::vector<double> movingAverages;
    
    if (data.empty()) {
        logMessage("WARNING: Empty dataset for moving average computation", "logs/hpc_execution.log");
        return movingAverages;
    }
    
    if (windowSize <= 0) {
        logMessage("WARNING: Invalid window size for moving average", "logs/hpc_execution.log");
        return movingAverages;
    }
    
    // Aggregate revenue by date
    std::map<int, double> dailyRevenue;  // epochDays -> total revenue
    
    if (parallel) {
        // Parallel aggregation using thread-local maps
        #pragma omp parallel
        {
            std::map<int, double> localRevenue;
            
            #pragma omp for nowait
            for (size_t i = 0; i < data.size(); i++) {
                int days = dateToEpochDays(data[i].invoiceDate);
                localRevenue[days] += data[i].totalPrice;
            }
            
            // Merge into global map
            #pragma omp critical
            {
                for (const auto& pair : localRevenue) {
                    dailyRevenue[pair.first] += pair.second;
                }
            }
        }
    } else {
        // Sequential aggregation
        for (const auto& record : data) {
            int days = dateToEpochDays(record.invoiceDate);
            dailyRevenue[days] += record.totalPrice;
        }
    }
    
    // Convert to sorted time series
    std::vector<TimeSeriesPoint> timeSeries;
    for (const auto& pair : dailyRevenue) {
        TimeSeriesPoint point;
        point.epochDays = pair.first;
        point.revenue = pair.second;
        timeSeries.push_back(point);
    }
    
    // Sort by date (should already be sorted due to map, but ensure)
    std::sort(timeSeries.begin(), timeSeries.end(),
              [](const TimeSeriesPoint& a, const TimeSeriesPoint& b) {
                  return a.epochDays < b.epochDays;
              });
    
    // Compute moving averages
    movingAverages.reserve(timeSeries.size());
    
    if (parallel && timeSeries.size() > 100) {
        // Parallel window computation (for large datasets)
        movingAverages.resize(timeSeries.size());
        
        #pragma omp parallel for
        for (size_t i = 0; i < timeSeries.size(); i++) {
            double sum = 0.0;
            int count = 0;
            
            // Calculate window bounds
            int startIdx = std::max(0, static_cast<int>(i) - windowSize + 1);
            int endIdx = i + 1;
            
            for (int j = startIdx; j < endIdx; j++) {
                sum += timeSeries[j].revenue;
                count++;
            }
            
            movingAverages[i] = sum / count;
        }
    } else {
        // Sequential computation (simpler and faster for small datasets)
        for (size_t i = 0; i < timeSeries.size(); i++) {
            double sum = 0.0;
            int count = 0;
            
            // Calculate window bounds
            int startIdx = std::max(0, static_cast<int>(i) - windowSize + 1);
            int endIdx = i + 1;
            
            for (int j = startIdx; j < endIdx; j++) {
                sum += timeSeries[j].revenue;
                count++;
            }
            
            movingAverages.push_back(sum / count);
        }
    }
    
    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = endTime - startTime;
    
    std::stringstream msg;
    msg << "INFO: Moving average computation completed in " << elapsed.count() << "s ("
        << (parallel ? "parallel" : "sequential") << ") - Window size: " << windowSize
        << ", Time series length: " << timeSeries.size();
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    return movingAverages;
}
