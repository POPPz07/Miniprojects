#include "../include/hpc_engine.h"
#include <fstream>
#include <sstream>
#include <iomanip>
#include <ctime>

// Experiment Logger - Captures all run configurations and results
class ExperimentLogger {
private:
    std::string logFilePath;
    std::ofstream logFile;
    
    std::string getCurrentTimestamp() {
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        std::stringstream ss;
        ss << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S");
        return ss.str();
    }
    
public:
    ExperimentLogger(const std::string& filepath) : logFilePath(filepath) {
        logFile.open(filepath, std::ios::app);
        if (!logFile.is_open()) {
            logMessage("ERROR: Could not open experiment log: " + filepath, "logs/hpc_execution.log");
        }
    }
    
    ~ExperimentLogger() {
        if (logFile.is_open()) {
            logFile.close();
        }
    }
    
    void logExperiment(const std::string& experimentName, 
                      int iterationNumber,
                      int threadCount,
                      int dataSize,
                      double seqTime,
                      double parTime,
                      double speedup,
                      double efficiency,
                      const std::map<std::string, double>& operationTimes,
                      const std::string& notes = "") {
        if (!logFile.is_open()) return;
        
        logFile << "========================================\n";
        logFile << "Experiment: " << experimentName << "\n";
        logFile << "Timestamp: " << getCurrentTimestamp() << "\n";
        logFile << "Iteration: " << iterationNumber << "\n";
        logFile << "Configuration:\n";
        logFile << "  Thread Count: " << threadCount << "\n";
        logFile << "  Data Size: " << dataSize << " rows\n";
        logFile << "Performance:\n";
        logFile << "  Sequential Time: " << std::fixed << std::setprecision(6) << seqTime << "s\n";
        logFile << "  Parallel Time: " << parTime << "s\n";
        logFile << "  Speedup: " << speedup << "x\n";
        logFile << "  Efficiency: " << (efficiency * 100) << "%\n";
        
        if (!operationTimes.empty()) {
            logFile << "Operation Times:\n";
            for (const auto& pair : operationTimes) {
                logFile << "  " << pair.first << ": " << pair.second << "s\n";
            }
        }
        
        if (!notes.empty()) {
            logFile << "Notes: " << notes << "\n";
        }
        
        logFile << "========================================\n\n";
        logFile.flush();
    }
    
    void logFailure(const std::string& experimentName,
                   int iterationNumber,
                   const std::string& failureReason,
                   const std::string& stackTrace = "") {
        if (!logFile.is_open()) return;
        
        logFile << "========================================\n";
        logFile << "FAILURE: " << experimentName << "\n";
        logFile << "Timestamp: " << getCurrentTimestamp() << "\n";
        logFile << "Iteration: " << iterationNumber << "\n";
        logFile << "Reason: " << failureReason << "\n";
        
        if (!stackTrace.empty()) {
            logFile << "Stack Trace:\n" << stackTrace << "\n";
        }
        
        logFile << "========================================\n\n";
        logFile.flush();
    }
    
    void logComputationIntensity(const std::string& operationName,
                                 double flops,
                                 double memoryAccesses,
                                 double computeTime,
                                 bool isParallelizable) {
        if (!logFile.is_open()) return;
        
        double intensity = (memoryAccesses > 0) ? (flops / memoryAccesses) : 0.0;
        
        logFile << "Computation Intensity Analysis:\n";
        logFile << "  Operation: " << operationName << "\n";
        logFile << "  FLOPs: " << flops << "\n";
        logFile << "  Memory Accesses: " << memoryAccesses << " bytes\n";
        logFile << "  Compute Time: " << computeTime << "s\n";
        logFile << "  Intensity (FLOPs/byte): " << intensity << "\n";
        logFile << "  Parallelizable: " << (isParallelizable ? "Yes" : "No") << "\n";
        logFile << "----------------------------------------\n";
        logFile.flush();
    }
};

// Global experiment logger
static ExperimentLogger* globalExperimentLogger = nullptr;

void initializeExperimentLogger(const std::string& filepath) {
    if (globalExperimentLogger == nullptr) {
        globalExperimentLogger = new ExperimentLogger(filepath);
    }
}

void logExperiment(const std::string& experimentName,
                  int iterationNumber,
                  int threadCount,
                  int dataSize,
                  double seqTime,
                  double parTime,
                  double speedup,
                  double efficiency,
                  const std::map<std::string, double>& operationTimes,
                  const std::string& notes) {
    if (globalExperimentLogger != nullptr) {
        globalExperimentLogger->logExperiment(experimentName, iterationNumber, threadCount,
                                             dataSize, seqTime, parTime, speedup, efficiency,
                                             operationTimes, notes);
    }
}

void logExperimentFailure(const std::string& experimentName,
                         int iterationNumber,
                         const std::string& failureReason,
                         const std::string& stackTrace) {
    if (globalExperimentLogger != nullptr) {
        globalExperimentLogger->logFailure(experimentName, iterationNumber, failureReason, stackTrace);
    }
}

void logComputationIntensity(const std::string& operationName,
                            double flops,
                            double memoryAccesses,
                            double computeTime,
                            bool isParallelizable) {
    if (globalExperimentLogger != nullptr) {
        globalExperimentLogger->logComputationIntensity(operationName, flops, memoryAccesses,
                                                       computeTime, isParallelizable);
    }
}

void cleanupExperimentLogger() {
    if (globalExperimentLogger != nullptr) {
        delete globalExperimentLogger;
        globalExperimentLogger = nullptr;
    }
}
