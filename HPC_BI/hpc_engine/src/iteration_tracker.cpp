#include "../include/hpc_engine.h"
#include <fstream>
#include <sstream>
#include <iomanip>
#include <ctime>
#include <algorithm>

// IterationTracker class implementation
class IterationTracker {
private:
    std::vector<IterationMetadata> history;
    IterationMetadata currentIteration;
    int nextIterationNumber;
    
    std::string getCurrentTimestamp() {
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        std::stringstream ss;
        ss << std::put_time(std::localtime(&time), "%Y-%m-%dT%H:%M:%S");
        return ss.str();
    }
    
    std::string escapeJson(const std::string& str) {
        std::string escaped;
        for (char c : str) {
            switch (c) {
                case '"': escaped += "\\\""; break;
                case '\\': escaped += "\\\\"; break;
                case '\n': escaped += "\\n"; break;
                case '\r': escaped += "\\r"; break;
                case '\t': escaped += "\\t"; break;
                default: escaped += c;
            }
        }
        return escaped;
    }
    
public:
    IterationTracker() : nextIterationNumber(1) {}
    
    void beginIteration(const std::string& description, const std::string& rationale) {
        currentIteration = IterationMetadata();
        currentIteration.iterationNumber = nextIterationNumber++;
        currentIteration.description = description;
        currentIteration.rationale = rationale;
        currentIteration.timestamp = getCurrentTimestamp();
        
        logMessage("Starting Iteration " + std::to_string(currentIteration.iterationNumber) + 
                  ": " + description, "logs/hpc_execution.log");
    }
    
    void setConfiguration(int threads, int dataSize, const std::vector<std::string>& computations) {
        currentIteration.threadCount = threads;
        currentIteration.dataSize = dataSize;
        currentIteration.computationsEnabled = computations;
    }
    
    void recordPerformance(double seqTime, double parTime, const PerformanceBreakdown& breakdown) {
        currentIteration.sequentialTime = seqTime;
        currentIteration.parallelTime = parTime;
        currentIteration.speedup = (parTime > 0) ? (seqTime / parTime) : 0.0;
        currentIteration.efficiency = (currentIteration.threadCount > 0) ? 
                                     (currentIteration.speedup / currentIteration.threadCount) : 0.0;
        currentIteration.breakdown = breakdown;
        
        // Copy Amdahl's Law analysis
        currentIteration.amdahlParallelizableFraction = breakdown.parallelizableFraction;
        currentIteration.amdahlTheoreticalMaxSpeedup = breakdown.theoreticalMaxSpeedup;
        currentIteration.amdahlActualSpeedup = breakdown.actualSpeedup;
        currentIteration.amdahlParallelizationEfficiency = breakdown.parallelizationEfficiency;
    }
    
    void setAnalysis(const std::string& performanceAnalysis, const std::string& limitingFactors) {
        currentIteration.performanceAnalysis = performanceAnalysis;
        currentIteration.limitingFactors = limitingFactors;
    }
    
    void addLearning(const std::string& learning) {
        currentIteration.learnings.push_back(learning);
    }
    
    void addNextStep(const std::string& nextStep) {
        currentIteration.nextSteps.push_back(nextStep);
    }
    
    void endIteration() {
        history.push_back(currentIteration);
        
        // Save to CSV
        saveIterationHistoryCSV(".kiro/specs/system-explainability-upgrade/metrics/iteration_metrics.csv");
        
        // Save to JSON
        saveIterationJSON(".kiro/specs/system-explainability-upgrade/evolution/iteration_" + 
                         std::to_string(currentIteration.iterationNumber) + ".json");
        
        logMessage("Completed Iteration " + std::to_string(currentIteration.iterationNumber) + 
                  " - Speedup: " + std::to_string(currentIteration.speedup) + "x, " +
                  "Efficiency: " + std::to_string(currentIteration.efficiency * 100) + "%",
                  "logs/hpc_execution.log");
    }
    
    void saveIterationHistoryCSV(const std::string& filename) {
        std::ofstream file(filename);
        if (!file.is_open()) {
            logMessage("ERROR: Could not open " + filename + " for writing", "logs/hpc_execution.log");
            return;
        }
        
        // Write header
        file << "iteration_number,timestamp,description,thread_count,data_size,"
             << "seq_time,par_time,speedup,efficiency,parallelizable_fraction,"
             << "theoretical_max_speedup,actual_speedup,parallelization_efficiency\n";
        
        // Write data
        for (const auto& iter : history) {
            file << iter.iterationNumber << ","
                 << iter.timestamp << ","
                 << "\"" << iter.description << "\","
                 << iter.threadCount << ","
                 << iter.dataSize << ","
                 << std::fixed << std::setprecision(6) << iter.sequentialTime << ","
                 << iter.parallelTime << ","
                 << iter.speedup << ","
                 << iter.efficiency << ","
                 << iter.amdahlParallelizableFraction << ","
                 << iter.amdahlTheoreticalMaxSpeedup << ","
                 << iter.amdahlActualSpeedup << ","
                 << iter.amdahlParallelizationEfficiency << "\n";
        }
        
        file.close();
        logMessage("Saved iteration history to " + filename, "logs/hpc_execution.log");
    }
    
    void saveIterationJSON(const std::string& filename) {
        std::ofstream file(filename);
        if (!file.is_open()) {
            logMessage("ERROR: Could not open " + filename + " for writing", "logs/hpc_execution.log");
            return;
        }
        
        const auto& iter = currentIteration;
        
        file << "{\n";
        file << "  \"iterationNumber\": " << iter.iterationNumber << ",\n";
        file << "  \"timestamp\": \"" << iter.timestamp << "\",\n";
        file << "  \"description\": \"" << escapeJson(iter.description) << "\",\n";
        file << "  \"rationale\": \"" << escapeJson(iter.rationale) << "\",\n";
        
        // Configuration
        file << "  \"configuration\": {\n";
        file << "    \"threadCount\": " << iter.threadCount << ",\n";
        file << "    \"dataSize\": " << iter.dataSize << ",\n";
        file << "    \"computationsEnabled\": [";
        for (size_t i = 0; i < iter.computationsEnabled.size(); i++) {
            file << "\"" << iter.computationsEnabled[i] << "\"";
            if (i < iter.computationsEnabled.size() - 1) file << ", ";
        }
        file << "]\n";
        file << "  },\n";
        
        // Performance
        file << "  \"performance\": {\n";
        file << "    \"sequentialTime\": " << std::fixed << std::setprecision(6) << iter.sequentialTime << ",\n";
        file << "    \"parallelTime\": " << iter.parallelTime << ",\n";
        file << "    \"speedup\": " << iter.speedup << ",\n";
        file << "    \"efficiency\": " << iter.efficiency << ",\n";
        file << "    \"breakdown\": {\n";
        file << "      \"dataLoading\": " << iter.breakdown.dataLoadingTime << ",\n";
        file << "      \"parallelizableComputation\": " << iter.breakdown.parallelizableComputationTime << ",\n";
        file << "      \"sequentialComputation\": " << iter.breakdown.sequentialComputationTime << ",\n";
        file << "      \"outputGeneration\": " << iter.breakdown.outputGenerationTime << "\n";
        file << "    }\n";
        file << "  },\n";
        
        // Technical Analysis
        file << "  \"technicalAnalysis\": {\n";
        file << "    \"performanceAnalysis\": \"" << escapeJson(iter.performanceAnalysis) << "\",\n";
        file << "    \"limitingFactors\": \"" << escapeJson(iter.limitingFactors) << "\",\n";
        file << "    \"amdahlAnalysis\": {\n";
        file << "      \"parallelizableFraction\": " << iter.amdahlParallelizableFraction << ",\n";
        file << "      \"theoreticalMaxSpeedup\": " << iter.amdahlTheoreticalMaxSpeedup << ",\n";
        file << "      \"actualSpeedup\": " << iter.amdahlActualSpeedup << ",\n";
        file << "      \"parallelizationEfficiency\": " << iter.amdahlParallelizationEfficiency << "\n";
        file << "    }\n";
        file << "  },\n";
        
        // Learnings
        file << "  \"learnings\": [";
        for (size_t i = 0; i < iter.learnings.size(); i++) {
            file << "\"" << escapeJson(iter.learnings[i]) << "\"";
            if (i < iter.learnings.size() - 1) file << ", ";
        }
        file << "],\n";
        
        // Next Steps
        file << "  \"nextSteps\": [";
        for (size_t i = 0; i < iter.nextSteps.size(); i++) {
            file << "\"" << escapeJson(iter.nextSteps[i]) << "\"";
            if (i < iter.nextSteps.size() - 1) file << ", ";
        }
        file << "]\n";
        
        file << "}\n";
        
        file.close();
        logMessage("Saved iteration details to " + filename, "logs/hpc_execution.log");
    }
    
    std::vector<IterationMetadata> getIterationHistory() const {
        return history;
    }
    
    IterationMetadata getCurrentIteration() const {
        return currentIteration;
    }
};

// Global instance
static IterationTracker globalTracker;

// Public interface functions
void beginIteration(const std::string& description, const std::string& rationale) {
    globalTracker.beginIteration(description, rationale);
}

void setIterationConfiguration(int threads, int dataSize, const std::vector<std::string>& computations) {
    globalTracker.setConfiguration(threads, dataSize, computations);
}

void recordIterationPerformance(double seqTime, double parTime, const PerformanceBreakdown& breakdown) {
    globalTracker.recordPerformance(seqTime, parTime, breakdown);
}

void setIterationAnalysis(const std::string& performanceAnalysis, const std::string& limitingFactors) {
    globalTracker.setAnalysis(performanceAnalysis, limitingFactors);
}

void addIterationLearning(const std::string& learning) {
    globalTracker.addLearning(learning);
}

void addIterationNextStep(const std::string& nextStep) {
    globalTracker.addNextStep(nextStep);
}

void endIteration() {
    globalTracker.endIteration();
}
