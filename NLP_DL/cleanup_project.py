"""
Project Cleanup Script
Removes unused files and folders for production deployment
"""

import os
import shutil

# Files and folders to delete
TO_DELETE = [
    # Unused Python scripts
    'check_duplicates.py',
    'preprocessing/demo_preprocessing.py',
    
    # Old training modules (replaced by notebook)
    'nlp_module/',
    'dl_module/',
    
    # Results and specs (documentation only)
    'results/',
    'specs/',
    
    # Multiple README files (consolidated into one)
    'APP_SCREENSHOTS_GUIDE.md',
    'STREAMLIT_APP_SUMMARY.md',
    'STREAMLIT_README.md',
    'QUICK_START.md',
    'KAGGLE_SETUP.md',
    
    # Shell scripts (not needed for cloud deployment)
    'run_app.ps1',
    'run_app.bat',
    'restart_app.ps1',
    
    # Old notebook
    'notebooks/README_COLAB.md',
    'notebooks/dl_pipeline_colab.ipynb',
    
    # Temporary files
    'generate_notebook.py',
    'notebooks/complete_training_pipeline_part2.json',
    
    # Python cache
    'preprocessing/__pycache__',
    '__pycache__',
]

def cleanup():
    """Remove unused files and folders"""
    print('='*60)
    print('PROJECT CLEANUP')
    print('='*60)
    
    deleted_count = 0
    skipped_count = 0
    
    for item in TO_DELETE:
        if os.path.exists(item):
            try:
                if os.path.isfile(item):
                    os.remove(item)
                    print(f'✓ Deleted file: {item}')
                elif os.path.isdir(item):
                    shutil.rmtree(item)
                    print(f'✓ Deleted folder: {item}')
                deleted_count += 1
            except Exception as e:
                print(f'❌ Error deleting {item}: {e}')
                skipped_count += 1
        else:
            print(f'⊘ Not found: {item}')
            skipped_count += 1
    
    print('\\n' + '='*60)
    print('CLEANUP SUMMARY')
    print('='*60)
    print(f'Deleted: {deleted_count} items')
    print(f'Skipped: {skipped_count} items')
    print('\\n✅ Cleanup complete!')
    
    # Show remaining structure
    print('\\n' + '='*60)
    print('REMAINING PROJECT STRUCTURE')
    print('='*60)
    print('''
project/
├── data/
│   ├── prepare_dataset.py
│   ├── train.csv
│   └── test.csv
├── models/
│   └── (all model files)
├── notebooks/
│   └── complete_training_pipeline.ipynb
├── preprocessing/
│   └── text_cleaner.py
├── .streamlit/
│   └── config.toml
├── app.py
├── requirements.txt
├── README.md
├── APP_UPDATE_GUIDE.md
├── NOTEBOOK_INSTRUCTIONS.md
└── cleanup_project.py (this file)
    ''')
    
    print('\\n📦 Ready for deployment!')
    print('\\nNext steps:')
    print('1. Train models using complete_training_pipeline.ipynb')
    print('2. Download models to models/ directory')
    print('3. Update app.py following APP_UPDATE_GUIDE.md')
    print('4. Test locally: streamlit run app.py')
    print('5. Deploy to Streamlit Cloud')

if __name__ == '__main__':
    # Confirm before cleanup
    print('This script will delete unused files and folders.')
    print('\\nFiles/folders to be deleted:')
    for item in TO_DELETE:
        print(f'  - {item}')
    
    response = input('\\nProceed with cleanup? (yes/no): ')
    
    if response.lower() in ['yes', 'y']:
        cleanup()
    else:
        print('\\n❌ Cleanup cancelled.')
