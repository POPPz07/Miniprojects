# Makefile for HPC Engine

CXX = g++
CXXFLAGS = -std=c++11 -O3 -fopenmp -Wall
INCLUDES = -Iinclude
SRCDIR = src
OBJDIR = obj
BINDIR = bin

# Source files
SOURCES = $(SRCDIR)/main.cpp \
          $(SRCDIR)/data_loader.cpp \
          $(SRCDIR)/sequential_compute.cpp \
          $(SRCDIR)/parallel_compute.cpp \
          $(SRCDIR)/output_generator.cpp \
          $(SRCDIR)/iteration_tracker.cpp \
          $(SRCDIR)/performance_analyzer.cpp \
          $(SRCDIR)/rfm_compute.cpp \
          $(SRCDIR)/correlation_compute.cpp \
          $(SRCDIR)/topk_compute.cpp \
          $(SRCDIR)/percentile_compute.cpp \
          $(SRCDIR)/moving_average_compute.cpp \
          $(SRCDIR)/experiment_logger.cpp \
          $(SRCDIR)/validation.cpp

# Object files
OBJECTS = $(SOURCES:$(SRCDIR)/%.cpp=$(OBJDIR)/%.o)

# Target executable
TARGET = $(BINDIR)/hpc_engine.exe

# Default target
all: directories $(TARGET)

# Create necessary directories
directories:
	@if not exist "$(OBJDIR)" mkdir $(OBJDIR)
	@if not exist "$(BINDIR)" mkdir $(BINDIR)
	@if not exist "..\logs" mkdir ..\logs
	@if not exist "..\data" mkdir ..\data

# Link object files to create executable
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $(OBJECTS) -o $(TARGET)
	@echo Build complete: $(TARGET)

# Compile source files to object files
$(OBJDIR)/%.o: $(SRCDIR)/%.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# Clean build artifacts
clean:
	@if exist "$(OBJDIR)" rmdir /s /q $(OBJDIR)
	@if exist "$(BINDIR)" rmdir /s /q $(BINDIR)
	@echo Clean complete

# Run the program
run: $(TARGET)
	@cd .. && hpc_engine\$(TARGET)

.PHONY: all directories clean run
