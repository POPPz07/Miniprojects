#ifndef HPC_ENGINE_H
#define HPC_ENGINE_H

#include <string>
#include <vector>
#include <chrono>
#include <map>

// Data structure to hold parsed retail data
struct RetailRecord {
    std::string invoiceNo;
    std::string stockCode;
    std::string customerID;
    std::string invoiceDate;  // ISO 8601 format YYYY-MM-DD HH:MM:SS
    int quantity;
    double unitPrice;
    double totalPrice;
};

// Structure to hold computation results
struct ComputationResults {
    // Basic aggregations
    double totalRevenue;
    double avgUnitPrice;
    int minQuantity;
    int maxQuantity;
    int totalRowsProcessed;
    
    // Statistical metrics (useful for BI)
    double revenueStdDev;
    double priceStdDev;
    double revenueMedian;
    double revenue25thPercentile;
    double revenue75thPercentile;
    
    // Business metrics (useful for dashboard)
    double highValueThreshold;  // 75th percentile for classification
    int highValueTransactions;
    double highValueRevenue;
    double avgTransactionSize;
    
    // Timing breakdown
    double dataLoadTime;
    double computationTime;
    double totalTime;
};

// RFM Metrics structure
struct RFMMetrics {
    std::string customerID;
    int recency;              // Days since last purchase (>= 0)
    int frequency;            // Number of purchases (>= 1)
    double monetary;          // Total spend (> 0)
    int rScore;               // Recency score 1-5 (5 = most recent)
    int fScore;               // Frequency score 1-5 (5 = most frequent)
    int mScore;               // Monetary score 1-5 (5 = highest spend)
    std::string rfmScore;     // Combined "555" format
    std::string segment;      // Champions, Loyal, At Risk, Lost, Other
};

// Customer Metric structure for Top-K analysis
struct CustomerMetric {
    std::string customerID;
    double totalSpend;
    int purchaseCount;
    double avgOrderValue;
};

// Product Metric structure for Top-K analysis
struct ProductMetric {
    std::string stockCode;
    int totalQuantitySold;
    double totalRevenue;
    int uniqueCustomers;
};

// Structure to hold scalability metrics
struct ScalabilityMetrics {
    int dataSize;
    double seqTime;
    double parTime;
    double speedup;
    double efficiency;
    int threads;
};

// Structure for detailed performance breakdown
struct PerformanceBreakdown {
    // Time breakdown
    double dataLoadingTime;
    double parallelizableComputationTime;
    double sequentialComputationTime;
    double outputGenerationTime;
    
    // Parallelization analysis
    double parallelizableFraction;      // Amdahl's Law parameter
    double theoreticalMaxSpeedup;       // 1 / (1 - parallelizableFraction)
    double actualSpeedup;
    double parallelizationEfficiency;   // actualSpeedup / theoreticalMaxSpeedup
    
    // Overhead analysis
    double openmpOverhead;
    double synchronizationTime;
    double memoryContentionTime;
    
    // Operation timing map
    std::map<std::string, double> operationTimes;
    std::map<std::string, bool> operationParallelizable;
};

// Structure for iteration metadata
struct IterationMetadata {
    int iterationNumber;
    std::string timestamp;
    std::string description;
    std::string rationale;
    
    // Configuration
    int threadCount;
    int dataSize;
    std::vector<std::string> computationsEnabled;
    std::map<std::string, std::string> parameters;
    
    // Performance
    double sequentialTime;
    double parallelTime;
    double speedup;
    double efficiency;
    
    // Performance breakdown
    PerformanceBreakdown breakdown;
    
    // Technical explanation
    std::string performanceAnalysis;
    std::string limitingFactors;
    
    // Amdahl's Law analysis
    double amdahlParallelizableFraction;
    double amdahlTheoreticalMaxSpeedup;
    double amdahlActualSpeedup;
    double amdahlParallelizationEfficiency;
    
    // Learnings and next steps
    std::vector<std::string> learnings;
    std::vector<std::string> nextSteps;
};

// Function declarations
std::vector<RetailRecord> loadDataset(const std::string& filename, int maxRows = -1);
ComputationResults computeSequential(const std::vector<RetailRecord>& data);
ComputationResults computeParallel(const std::vector<RetailRecord>& data, int numThreads);
void saveScalabilityMetrics(const std::vector<ScalabilityMetrics>& metrics, const std::string& filename);
void saveResultsSummary(const ComputationResults& results, const std::string& filename);
void logMessage(const std::string& message, const std::string& logFile);
bool validateResults(const ComputationResults& seq, const ComputationResults& par, double tolerance = 0.01);

// New output functions
void saveRFMAnalysis(const std::map<std::string, RFMMetrics>& rfmMetrics, const std::string& filename);
void saveCorrelationResults(double correlation, const std::string& filename);
void saveTopKResults(const std::vector<CustomerMetric>& topCustomers,
                     const std::vector<ProductMetric>& topProducts,
                     const std::string& filename);
void savePercentileResults(const std::map<int, double>& percentiles, const std::string& filename);
void saveMovingAverageResults(const std::vector<double>& movingAvg7,
                              const std::vector<double>& movingAvg30,
                              const std::string& filename);

// New meaningful computation functions
std::map<std::string, RFMMetrics> computeRFMMetrics(const std::vector<RetailRecord>& data, bool parallel = false);
double computeCorrelation(const std::vector<RetailRecord>& data, bool parallel = false);
std::vector<CustomerMetric> computeTopKCustomers(const std::vector<RetailRecord>& data, int k, bool parallel = false);
std::vector<ProductMetric> computeTopKProducts(const std::vector<RetailRecord>& data, int k, bool parallel = false);
std::map<int, double> computePercentiles(const std::vector<RetailRecord>& data, const std::vector<int>& percentiles, bool parallel = false);
std::vector<double> computeMovingAverage(const std::vector<RetailRecord>& data, int windowSize, bool parallel = false);

// Helper functions
std::string getCurrentTimestamp();
int daysBetween(const std::string& date1, const std::string& date2);
std::string getMostRecentDate(const std::vector<RetailRecord>& data);

// Iteration Tracker functions
void beginIteration(const std::string& description, const std::string& rationale);
void setIterationConfiguration(int threads, int dataSize, const std::vector<std::string>& computations);
void recordIterationPerformance(double seqTime, double parTime, const PerformanceBreakdown& breakdown);
void setIterationAnalysis(const std::string& performanceAnalysis, const std::string& limitingFactors);
void addIterationLearning(const std::string& learning);
void addIterationNextStep(const std::string& nextStep);
void endIteration();

// Performance Analyzer functions
PerformanceBreakdown analyzePerformance(
    double seqTime,
    double parTime,
    int threadCount,
    const std::map<std::string, double>& operationTimes,
    const std::map<std::string, bool>& operationParallelizable
);
std::string generatePerformanceExplanation(const PerformanceBreakdown& breakdown, 
                                          double speedup, int threadCount);
std::string identifyLimitingFactors(const PerformanceBreakdown& breakdown, 
                                    double speedup, int threadCount);
void classifyOperations(std::vector<std::string>& parallelizable,
                       std::vector<std::string>& sequential,
                       const std::map<std::string, bool>& operationParallelizable);
std::string generateAmdahlAnalysis(const PerformanceBreakdown& breakdown, int threadCount);

// Experiment Logger functions
void initializeExperimentLogger(const std::string& filepath);
void logExperiment(const std::string& experimentName,
                  int iterationNumber,
                  int threadCount,
                  int dataSize,
                  double seqTime,
                  double parTime,
                  double speedup,
                  double efficiency,
                  const std::map<std::string, double>& operationTimes,
                  const std::string& notes = "");
void logExperimentFailure(const std::string& experimentName,
                         int iterationNumber,
                         const std::string& failureReason,
                         const std::string& stackTrace = "");
void logComputationIntensity(const std::string& operationName,
                            double flops,
                            double memoryAccesses,
                            double computeTime,
                            bool isParallelizable);
void cleanupExperimentLogger();

// Validation functions
bool validateNumericalTolerance(double value1, double value2, double tolerance = 1e-6);
bool validateGroundTruth(const std::vector<RetailRecord>& sampleData,
                        const ComputationResults& results,
                        double tolerance = 0.01);

#endif // HPC_ENGINE_H
