#include "../include/hpc_engine.h"
#include <cmath>
#include <sstream>
#include <iomanip>

// PerformanceAnalyzer class implementation
class PerformanceAnalyzer {
public:
    PerformanceBreakdown analyzePerformance(
        double seqTime,
        double parTime,
        int threadCount,
        const std::map<std::string, double>& operationTimes,
        const std::map<std::string, bool>& operationParallelizable
    ) {
        PerformanceBreakdown breakdown;
        
        // Calculate time breakdown
        breakdown.dataLoadingTime = operationTimes.count("data_loading") ? 
                                    operationTimes.at("data_loading") : 0.0;
        breakdown.outputGenerationTime = operationTimes.count("output_generation") ? 
                                         operationTimes.at("output_generation") : 0.0;
        
        // Calculate parallelizable vs sequential computation time
        breakdown.parallelizableComputationTime = 0.0;
        breakdown.sequentialComputationTime = 0.0;
        
        for (const auto& pair : operationTimes) {
            if (pair.first != "data_loading" && pair.first != "output_generation") {
                if (operationParallelizable.count(pair.first) && operationParallelizable.at(pair.first)) {
                    breakdown.parallelizableComputationTime += pair.second;
                } else {
                    breakdown.sequentialComputationTime += pair.second;
                }
            }
        }
        
        // Calculate Amdahl's Law parameters
        double totalComputation = breakdown.parallelizableComputationTime + 
                                 breakdown.sequentialComputationTime;
        
        if (totalComputation > 0) {
            breakdown.parallelizableFraction = breakdown.parallelizableComputationTime / totalComputation;
        } else {
            breakdown.parallelizableFraction = 0.0;
        }
        
        // Theoretical max speedup (Amdahl's Law)
        if (breakdown.parallelizableFraction < 1.0) {
            breakdown.theoreticalMaxSpeedup = 1.0 / (1.0 - breakdown.parallelizableFraction);
        } else {
            breakdown.theoreticalMaxSpeedup = threadCount; // Perfect parallelization
        }
        
        // Actual speedup
        breakdown.actualSpeedup = (parTime > 0) ? (seqTime / parTime) : 0.0;
        
        // Parallelization efficiency
        if (breakdown.theoreticalMaxSpeedup > 0) {
            breakdown.parallelizationEfficiency = breakdown.actualSpeedup / breakdown.theoreticalMaxSpeedup;
        } else {
            breakdown.parallelizationEfficiency = 0.0;
        }
        
        // Overhead analysis
        // OpenMP overhead = (parallel time - (sequential time / threads))
        double idealParallelTime = seqTime / threadCount;
        breakdown.openmpOverhead = std::max(0.0, parTime - idealParallelTime);
        
        // Estimate synchronization time (rough approximation)
        breakdown.synchronizationTime = breakdown.openmpOverhead * 0.3; // ~30% of overhead
        
        // Estimate memory contention time
        breakdown.memoryContentionTime = breakdown.openmpOverhead * 0.4; // ~40% of overhead
        
        // Store operation times and classifications
        breakdown.operationTimes = operationTimes;
        breakdown.operationParallelizable = operationParallelizable;
        
        return breakdown;
    }
    
    std::string generatePerformanceExplanation(
        const PerformanceBreakdown& breakdown,
        double speedup,
        int threadCount
    ) {
        std::stringstream ss;
        
        if (speedup < 1.0) {
            ss << "Parallel execution is slower than sequential (speedup " 
               << std::fixed << std::setprecision(2) << speedup << "x). ";
            ss << "This occurs because OpenMP overhead (" 
               << std::fixed << std::setprecision(4) << breakdown.openmpOverhead << "s) ";
            ss << "exceeds the computation time savings. ";
            ss << "Fast operations with small workloads do not benefit from parallelization.";
        } else if (speedup < 2.0) {
            ss << "Moderate speedup achieved (" 
               << std::fixed << std::setprecision(2) << speedup << "x with " 
               << threadCount << " threads). ";
            ss << "Parallelizable fraction is " 
               << std::fixed << std::setprecision(1) << (breakdown.parallelizableFraction * 100) << "%, ";
            ss << "limiting theoretical max speedup to " 
               << std::fixed << std::setprecision(2) << breakdown.theoreticalMaxSpeedup << "x. ";
            
            if (breakdown.sequentialComputationTime > breakdown.parallelizableComputationTime * 0.3) {
                ss << "Sequential operations (sorting, I/O) limit overall speedup.";
            } else {
                ss << "Memory bandwidth and synchronization overhead reduce efficiency.";
            }
        } else {
            ss << "Good speedup achieved (" 
               << std::fixed << std::setprecision(2) << speedup << "x with " 
               << threadCount << " threads). ";
            ss << "Workload is sufficiently large to amortize OpenMP overhead. ";
            ss << "Parallelizable fraction of " 
               << std::fixed << std::setprecision(1) << (breakdown.parallelizableFraction * 100) 
               << "% enables effective parallelization.";
        }
        
        return ss.str();
    }
    
    std::string identifyLimitingFactors(
        const PerformanceBreakdown& breakdown,
        double speedup,
        int threadCount
    ) {
        std::stringstream ss;
        std::vector<std::string> factors;
        
        // Check for OpenMP overhead dominance
        if (breakdown.openmpOverhead > breakdown.parallelizableComputationTime) {
            factors.push_back("OpenMP overhead exceeds computation time");
        }
        
        // Check for low parallelizable fraction (Amdahl's Law)
        if (breakdown.parallelizableFraction < 0.7) {
            factors.push_back("Low parallelizable fraction (" + 
                            std::to_string((int)(breakdown.parallelizableFraction * 100)) + 
                            "%) limits speedup per Amdahl's Law");
        }
        
        // Check for memory contention
        if (breakdown.memoryContentionTime > breakdown.parallelizableComputationTime * 0.2) {
            factors.push_back("Memory bandwidth contention with " + 
                            std::to_string(threadCount) + " threads");
        }
        
        // Check for synchronization overhead
        if (breakdown.synchronizationTime > breakdown.parallelizableComputationTime * 0.15) {
            factors.push_back("Synchronization overhead in parallel reductions");
        }
        
        // Check for sequential bottlenecks
        if (breakdown.sequentialComputationTime > breakdown.parallelizableComputationTime * 0.3) {
            factors.push_back("Sequential operations (sorting, I/O) create bottlenecks");
        }
        
        // Check for poor scaling efficiency
        double efficiency = speedup / threadCount;
        if (efficiency < 0.5 && threadCount >= 4) {
            factors.push_back("Poor scaling efficiency (" + 
                            std::to_string((int)(efficiency * 100)) + 
                            "%) indicates diminishing returns with more threads");
        }
        
        // Combine factors
        if (factors.empty()) {
            ss << "No significant limiting factors identified. Performance is near optimal for this workload.";
        } else {
            ss << "Limiting factors: ";
            for (size_t i = 0; i < factors.size(); i++) {
                ss << factors[i];
                if (i < factors.size() - 1) ss << "; ";
            }
            ss << ".";
        }
        
        return ss.str();
    }
    
    void classifyOperations(
        std::vector<std::string>& parallelizable,
        std::vector<std::string>& sequential,
        const std::map<std::string, bool>& operationParallelizable
    ) {
        parallelizable.clear();
        sequential.clear();
        
        for (const auto& pair : operationParallelizable) {
            if (pair.second) {
                parallelizable.push_back(pair.first);
            } else {
                sequential.push_back(pair.first);
            }
        }
    }
    
    std::string generateAmdahlAnalysis(const PerformanceBreakdown& breakdown, int threadCount) {
        std::stringstream ss;
        
        ss << "Amdahl's Law Analysis:\n";
        ss << "  Parallelizable Fraction (P): " 
           << std::fixed << std::setprecision(3) << breakdown.parallelizableFraction << "\n";
        ss << "  Sequential Fraction (1-P): " 
           << std::fixed << std::setprecision(3) << (1.0 - breakdown.parallelizableFraction) << "\n";
        ss << "  Theoretical Max Speedup: " 
           << std::fixed << std::setprecision(2) << breakdown.theoreticalMaxSpeedup << "x\n";
        ss << "  Actual Speedup: " 
           << std::fixed << std::setprecision(2) << breakdown.actualSpeedup << "x\n";
        ss << "  Parallelization Efficiency: " 
           << std::fixed << std::setprecision(1) << (breakdown.parallelizationEfficiency * 100) << "%\n";
        ss << "\n";
        ss << "Interpretation: ";
        
        if (breakdown.parallelizationEfficiency > 0.8) {
            ss << "Excellent parallelization efficiency. Actual speedup is close to theoretical maximum.";
        } else if (breakdown.parallelizationEfficiency > 0.5) {
            ss << "Good parallelization efficiency. Some overhead reduces actual speedup below theoretical maximum.";
        } else {
            ss << "Low parallelization efficiency. Significant overhead or sequential bottlenecks limit speedup.";
        }
        
        return ss.str();
    }
};

// Global instance
static PerformanceAnalyzer globalAnalyzer;

// Public interface functions
PerformanceBreakdown analyzePerformance(
    double seqTime,
    double parTime,
    int threadCount,
    const std::map<std::string, double>& operationTimes,
    const std::map<std::string, bool>& operationParallelizable
) {
    return globalAnalyzer.analyzePerformance(seqTime, parTime, threadCount, 
                                            operationTimes, operationParallelizable);
}

std::string generatePerformanceExplanation(const PerformanceBreakdown& breakdown, 
                                          double speedup, int threadCount) {
    return globalAnalyzer.generatePerformanceExplanation(breakdown, speedup, threadCount);
}

std::string identifyLimitingFactors(const PerformanceBreakdown& breakdown, 
                                    double speedup, int threadCount) {
    return globalAnalyzer.identifyLimitingFactors(breakdown, speedup, threadCount);
}

void classifyOperations(std::vector<std::string>& parallelizable,
                       std::vector<std::string>& sequential,
                       const std::map<std::string, bool>& operationParallelizable) {
    globalAnalyzer.classifyOperations(parallelizable, sequential, operationParallelizable);
}

std::string generateAmdahlAnalysis(const PerformanceBreakdown& breakdown, int threadCount) {
    return globalAnalyzer.generateAmdahlAnalysis(breakdown, threadCount);
}
