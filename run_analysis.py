#!/usr/bin/env python3
"""
Quick Analysis Runner

This script runs the dependency analysis and displays a summary.
For full details, see unused_files_report.txt and UNUSED_FILES_ANALYSIS.md
"""

import subprocess
import json
from pathlib import Path


def main():
    print("=" * 80)
    print("RUNNING DEPENDENCY ANALYSIS")
    print("=" * 80)
    print()
    
    # Run the analysis
    result = subprocess.run(
        ["python3", "analyze_unused_files.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("Error running analysis:")
        print(result.stderr)
        return
    
    # Load the JSON report
    json_file = Path("unused_files_report.json")
    if not json_file.exists():
        print("Report file not found!")
        return
    
    with open(json_file) as f:
        data = json.load(f)
    
    # Display summary
    print("\n" + "=" * 80)
    print("QUICK SUMMARY")
    print("=" * 80)
    print(f"\nTotal Python files:    {data['summary']['total_files']}")
    print(f"Used files:            {data['summary']['used_files']} ({data['summary']['used_files']/data['summary']['total_files']*100:.1f}%)")
    print(f"Unused files:          {data['summary']['unused_files']} ({data['summary']['unused_files']/data['summary']['total_files']*100:.1f}%)")
    print(f"Unused folders:        {data['summary']['unused_folders']}")
    
    if data.get('warnings'):
        print(f"\nWarnings:              {len(data['warnings'])}")
        for warning in data['warnings']:
            print(f"  ⚠  {warning}")
    
    print("\n" + "=" * 80)
    print("SAMPLE OF UNUSED FILES (First 20)")
    print("=" * 80)
    for i, file in enumerate(data['unused_files'][:20], 1):
        print(f"  {i:2d}. {file}")
    
    if len(data['unused_files']) > 20:
        print(f"\n  ... and {len(data['unused_files']) - 20} more")
    
    print("\n" + "=" * 80)
    print("SAMPLE OF UNUSED FOLDERS (First 10)")
    print("=" * 80)
    for i, folder in enumerate(data['unused_folders'][:10], 1):
        print(f"  {i:2d}. {folder}/")
    
    if len(data['unused_folders']) > 10:
        print(f"\n  ... and {len(data['unused_folders']) - 10} more")
    
    print("\n" + "=" * 80)
    print("FULL REPORTS AVAILABLE:")
    print("=" * 80)
    print("  - unused_files_report.txt  (detailed text report)")
    print("  - unused_files_report.json (machine-readable format)")
    print("  - UNUSED_FILES_ANALYSIS.md (comprehensive documentation)")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
