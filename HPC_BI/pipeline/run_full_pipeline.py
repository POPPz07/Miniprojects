"""
Full Pipeline Orchestration
Executes HPC Engine, BI Layer, and Cross-Module Validation
"""

import subprocess
import sys
import os
from datetime import datetime
import logging

# Setup logging
log_dir = '../logs'
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename='../logs/pipeline_execution.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_message(message):
    """Log message to both console and file"""
    logging.info(message)
    print(f"[INFO] {message}")


class PipelineOrchestrator:
    """
    Pipeline Orchestration Engine
    Manages execution of HPC Engine, BI Layer, and Validation
    """
    
    def __init__(self):
        """Initialize orchestrator"""
        self.start_time = datetime.now()
        self.execution_log = []
        log_message("PipelineOrchestrator initialized")
    
    def run_hpc_engine(self):
        """
        Execute HPC Engine
        
        Returns:
            bool: True if successful, False otherwise
        """
        log_message("="*60)
        log_message("STEP 1: Running HPC Engine")
        log_message("="*60)
        
        try:
            # Change to HPC engine directory and run
            hpc_dir = '../hpc_engine'
            
            # Check if executable exists
            if os.name == 'nt':  # Windows
                executable = os.path.join(hpc_dir, 'bin', 'hpc_engine.exe')
            else:  # Unix-like
                executable = os.path.join(hpc_dir, 'bin', 'hpc_engine')
            
            if not os.path.exists(executable):
                log_message(f"[WARNING] HPC Engine executable not found at {executable}")
                log_message("[INFO] Attempting to compile HPC Engine...")
                
                # Try to compile
                compile_result = subprocess.run(
                    ['make'],
                    cwd=hpc_dir,
                    capture_output=True,
                    text=True
                )
                
                if compile_result.returncode != 0:
                    log_message(f"[ERROR] HPC Engine compilation failed")
                    log_message(f"STDERR: {compile_result.stderr}")
                    self.execution_log.append({
                        'step': 'HPC Engine',
                        'status': 'FAILED',
                        'message': 'Compilation failed'
                    })
                    return False
                
                log_message("[SUCCESS] HPC Engine compiled successfully")
            
            # Run HPC Engine
            log_message("Executing HPC Engine...")
            result = subprocess.run(
                [executable],
                cwd=hpc_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                log_message("[SUCCESS] HPC Engine completed successfully")
                self.execution_log.append({
                    'step': 'HPC Engine',
                    'status': 'SUCCESS',
                    'message': 'Execution completed'
                })
                return True
            else:
                log_message(f"[ERROR] HPC Engine failed with return code {result.returncode}")
                log_message(f"STDERR: {result.stderr}")
                self.execution_log.append({
                    'step': 'HPC Engine',
                    'status': 'FAILED',
                    'message': f'Return code: {result.returncode}'
                })
                return False
                
        except Exception as e:
            log_message(f"[ERROR] HPC Engine execution failed: {str(e)}")
            self.execution_log.append({
                'step': 'HPC Engine',
                'status': 'ERROR',
                'message': str(e)
            })
            return False
    
    def run_bi_layer(self):
        """
        Execute BI Layer ETL
        
        Returns:
            bool: True if successful, False otherwise
        """
        log_message("="*60)
        log_message("STEP 2: Running BI Layer ETL")
        log_message("="*60)
        
        try:
            bi_dir = '../bi_layer'
            
            # Run ETL
            log_message("Executing BI Layer ETL...")
            result = subprocess.run(
                [sys.executable, 'etl.py'],
                cwd=bi_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                log_message("[SUCCESS] BI Layer ETL completed successfully")
                self.execution_log.append({
                    'step': 'BI Layer ETL',
                    'status': 'SUCCESS',
                    'message': 'ETL completed'
                })
                return True
            else:
                log_message(f"[ERROR] BI Layer ETL failed with return code {result.returncode}")
                log_message(f"STDERR: {result.stderr}")
                self.execution_log.append({
                    'step': 'BI Layer ETL',
                    'status': 'FAILED',
                    'message': f'Return code: {result.returncode}'
                })
                return False
                
        except Exception as e:
            log_message(f"[ERROR] BI Layer ETL execution failed: {str(e)}")
            self.execution_log.append({
                'step': 'BI Layer ETL',
                'status': 'ERROR',
                'message': str(e)
            })
            return False
    
    def run_validation(self):
        """
        Execute Cross-Module Validation
        
        Returns:
            bool: True if validation passes, False otherwise
        """
        log_message("="*60)
        log_message("STEP 3: Running Cross-Module Validation")
        log_message("="*60)
        
        try:
            # Import validation module
            from validation import run_validation
            
            # Run validation
            log_message("Executing validation checks...")
            results, report = run_validation()
            
            # Check overall status
            if results['overall_status'] == 'PASS':
                log_message("[SUCCESS] All validation checks passed")
                self.execution_log.append({
                    'step': 'Cross-Module Validation',
                    'status': 'SUCCESS',
                    'message': f"All {len(results['checks'])} checks passed"
                })
                return True
            elif results['overall_status'] == 'FAIL':
                log_message("[WARNING] Some validation checks failed")
                failed_checks = [c['check_name'] for c in results['checks'] if c['status'] == 'FAIL']
                log_message(f"Failed checks: {', '.join(failed_checks)}")
                self.execution_log.append({
                    'step': 'Cross-Module Validation',
                    'status': 'FAILED',
                    'message': f"Failed checks: {', '.join(failed_checks)}"
                })
                return False
            else:
                log_message("[ERROR] Validation encountered errors")
                self.execution_log.append({
                    'step': 'Cross-Module Validation',
                    'status': 'ERROR',
                    'message': 'Validation errors occurred'
                })
                return False
                
        except Exception as e:
            log_message(f"[ERROR] Validation execution failed: {str(e)}")
            self.execution_log.append({
                'step': 'Cross-Module Validation',
                'status': 'ERROR',
                'message': str(e)
            })
            return False
    
    def run_full_pipeline(self, skip_hpc=False):
        """
        Execute complete pipeline
        
        Args:
            skip_hpc: Skip HPC Engine execution if output files exist
            
        Returns:
            dict with execution summary
        """
        log_message("="*60)
        log_message("FULL PIPELINE EXECUTION STARTED")
        log_message(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        log_message("="*60)
        
        # Step 1: HPC Engine (optional if files exist)
        if skip_hpc:
            log_message("[INFO] Skipping HPC Engine (using existing output files)")
            self.execution_log.append({
                'step': 'HPC Engine',
                'status': 'SKIPPED',
                'message': 'Using existing output files'
            })
            hpc_success = True
        else:
            hpc_success = self.run_hpc_engine()
            
            if not hpc_success:
                log_message("[CRITICAL] HPC Engine failed. Stopping pipeline.")
                return self._generate_summary(success=False)
        
        # Step 2: BI Layer
        bi_success = self.run_bi_layer()
        
        if not bi_success:
            log_message("[CRITICAL] BI Layer failed. Stopping pipeline.")
            return self._generate_summary(success=False)
        
        # Step 3: Validation
        validation_success = self.run_validation()
        
        if not validation_success:
            log_message("[WARNING] Validation failed, but pipeline completed.")
        
        # Generate summary
        return self._generate_summary(success=True)
    
    def _generate_summary(self, success):
        """
        Generate execution summary
        
        Args:
            success: Overall pipeline success status
            
        Returns:
            dict with summary
        """
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        summary = {
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration_seconds': duration,
            'overall_success': success,
            'execution_log': self.execution_log
        }
        
        log_message("="*60)
        log_message("PIPELINE EXECUTION SUMMARY")
        log_message("="*60)
        log_message(f"Start Time: {summary['start_time']}")
        log_message(f"End Time: {summary['end_time']}")
        log_message(f"Duration: {duration:.2f} seconds")
        log_message(f"Overall Status: {'SUCCESS' if success else 'FAILED'}")
        log_message("")
        log_message("Step-by-Step Results:")
        for entry in self.execution_log:
            log_message(f"  [{entry['status']}] {entry['step']}: {entry['message']}")
        log_message("="*60)
        
        return summary


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run full HPC+BI pipeline')
    parser.add_argument('--skip-hpc', action='store_true', 
                       help='Skip HPC Engine execution (use existing output files)')
    args = parser.parse_args()
    
    orchestrator = PipelineOrchestrator()
    summary = orchestrator.run_full_pipeline(skip_hpc=args.skip_hpc)
    
    # Print summary
    print("\n" + "="*60)
    print("PIPELINE EXECUTION COMPLETE")
    print("="*60)
    print(f"Overall Status: {'SUCCESS' if summary['overall_success'] else 'FAILED'}")
    print(f"Duration: {summary['duration_seconds']:.2f} seconds")
    print(f"Steps Completed: {len(summary['execution_log'])}")
    print("="*60)
    
    # Exit with appropriate code
    sys.exit(0 if summary['overall_success'] else 1)


if __name__ == "__main__":
    main()
