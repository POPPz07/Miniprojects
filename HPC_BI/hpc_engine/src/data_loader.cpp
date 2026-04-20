#include "../include/hpc_engine.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <ctime>
#include <iomanip>

// Utility function to get current timestamp
std::string getCurrentTimestamp() {
    auto now = std::chrono::system_clock::now();
    auto time = std::chrono::system_clock::to_time_t(now);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S");
    return ss.str();
}

// Log message to file
void logMessage(const std::string& message, const std::string& logFile) {
    std::ofstream log(logFile, std::ios::app);
    if (log.is_open()) {
        log << "[" << getCurrentTimestamp() << "] " << message << std::endl;
        log.close();
    }
}

// Load dataset from CSV file
std::vector<RetailRecord> loadDataset(const std::string& filename, int maxRows) {
    auto startTime = std::chrono::high_resolution_clock::now();
    
    std::vector<RetailRecord> data;
    std::ifstream file(filename);
    
    if (!file.is_open()) {
        logMessage("ERROR: Cannot open file: " + filename, "logs/hpc_execution.log");
        return data;
    }
    
    logMessage("INFO: Loading dataset: " + filename, "logs/hpc_execution.log");
    
    std::string line;
    std::getline(file, line); // Skip header
    
    int rowCount = 0;
    int skippedRows = 0;
    
    while (std::getline(file, line) && (maxRows == -1 || rowCount < maxRows)) {
        std::stringstream ss(line);
        std::string field;
        std::vector<std::string> fields;
        
        // Parse CSV line (handle quoted fields)
        bool inQuotes = false;
        std::string currentField;
        for (char c : line) {
            if (c == '"') {
                inQuotes = !inQuotes;
            } else if (c == ',' && !inQuotes) {
                fields.push_back(currentField);
                currentField.clear();
            } else {
                currentField += c;
            }
        }
        fields.push_back(currentField);  // Add last field
        
        // Check if we have enough fields
        // Expected: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
        if (fields.size() < 8) {
            skippedRows++;
            continue;
        }
        
        try {
            // Extract fields
            std::string invoiceNo = fields[0];
            std::string stockCode = fields[1];
            std::string customerID = fields[6];
            std::string invoiceDate = fields[4];
            int quantity = std::stoi(fields[3]);
            double unitPrice = std::stod(fields[5]);
            
            // Skip invalid records
            if (quantity <= 0 || unitPrice <= 0 || customerID.empty()) {
                skippedRows++;
                continue;
            }
            
            // Create record
            RetailRecord record;
            record.invoiceNo = invoiceNo;
            record.stockCode = stockCode;
            record.customerID = customerID;
            record.invoiceDate = invoiceDate;
            record.quantity = quantity;
            record.unitPrice = unitPrice;
            record.totalPrice = quantity * unitPrice;
            
            data.push_back(record);
            rowCount++;
            
        } catch (const std::exception& e) {
            skippedRows++;
            continue;
        }
    }
    
    file.close();
    
    auto endTime = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = endTime - startTime;
    
    std::stringstream msg;
    msg << "INFO: Dataset loaded: " << rowCount << " valid rows, " << skippedRows 
        << " rows skipped (Load time: " << elapsed.count() << "s)";
    logMessage(msg.str(), "logs/hpc_execution.log");
    
    return data;
}
