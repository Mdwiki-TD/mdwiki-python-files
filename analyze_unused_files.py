#!/usr/bin/env python3
"""
Dependency Analysis Script for Python Repository

This script analyzes a Python repository to identify unused files and folders.
It traces all imports from entry point files and builds a complete dependency graph.
"""

import ast
import os
import sys
from pathlib import Path
from collections import defaultdict
from typing import Set, Dict, List, Tuple
import json


class DependencyAnalyzer:
    def __init__(self, base_path: Path, entry_points: List[str], exclude_folders: List[str] = None):
        self.base_path = base_path
        self.entry_points = entry_points
        self.exclude_folders = exclude_folders or []
        
        # Track all Python files in the repo
        self.all_python_files: Set[Path] = set()
        
        # Track used files (those that are imported)
        self.used_files: Set[Path] = set()
        
        # Track the dependency graph
        self.dependencies: Dict[Path, Set[Path]] = defaultdict(set)
        
        # Track errors and warnings
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def find_all_python_files(self) -> Set[Path]:
        """Find all Python files in the repository."""
        python_files = set()
        
        for file_path in self.base_path.rglob("*.py"):
            # Skip excluded folders
            relative_path = file_path.relative_to(self.base_path)
            if any(exclude in str(relative_path) for exclude in self.exclude_folders):
                continue
                
            # Skip special directories
            if any(part in str(file_path) for part in ['.git', '__pycache__', '.venv', 'venv']):
                continue
                
            python_files.add(file_path)
        
        return python_files
    
    def resolve_import(self, import_name: str, current_file: Path) -> List[Path]:
        """
        Resolve an import statement to file path(s).
        
        Args:
            import_name: The imported module name (e.g., 'md_core.mdpy.utils')
            current_file: The file containing the import statement
            
        Returns:
            List of Paths to the imported file(s), or empty list if not found
        """
        resolved = []
        
        # Handle relative imports
        if import_name.startswith('.'):
            # Count leading dots for relative import level
            level = len(import_name) - len(import_name.lstrip('.'))
            import_name = import_name.lstrip('.')
            
            # Get the directory of the current file
            current_dir = current_file.parent
            
            # Go up 'level - 1' directories
            for _ in range(level - 1):
                current_dir = current_dir.parent
            
            # Build the potential path
            if import_name:
                parts = import_name.split('.')
                potential_path = current_dir / '/'.join(parts)
            else:
                potential_path = current_dir
            
            # Check if it's a file
            if potential_path.suffix != '.py':
                py_file = potential_path.with_suffix('.py')
                if py_file.exists() and py_file in self.all_python_files:
                    resolved.append(py_file)
            
            # Check if it's a package (__init__.py)
            init_file = potential_path / '__init__.py'
            if init_file.exists() and init_file in self.all_python_files:
                resolved.append(init_file)
        else:
            # Absolute import - try multiple strategies
            parts = import_name.split('.')
            
            # Strategy 1: Direct from base path
            potential_path = self.base_path / '/'.join(parts)
            
            # Check if it's a file
            if potential_path.suffix != '.py':
                py_file = potential_path.with_suffix('.py')
                if py_file.exists() and py_file in self.all_python_files:
                    resolved.append(py_file)
            
            # Check if it's a package (__init__.py)
            init_file = potential_path / '__init__.py'
            if init_file.exists() and init_file in self.all_python_files:
                resolved.append(init_file)
            
            # Strategy 2: Search for matching files in the repository
            # This handles cases where imports don't use the full path from base
            if not resolved:
                # Try to find files that match the import pattern
                for py_file in self.all_python_files:
                    rel_path = py_file.relative_to(self.base_path)
                    # Remove .py extension and convert to module path
                    if py_file.name == '__init__.py':
                        module_path = str(rel_path.parent).replace('/', '.')
                    else:
                        module_path = str(rel_path.with_suffix('')).replace('/', '.')
                    
                    # Check if this file matches the import
                    if module_path == import_name or module_path.endswith('.' + import_name):
                        resolved.append(py_file)
        
        return resolved
    
    def extract_imports(self, file_path: Path) -> Set[str]:
        """Extract all import statements from a Python file."""
        imports = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        # Handle 'from X import Y'
                        module = node.module
                        if node.level > 0:
                            # Relative import
                            module = '.' * node.level + (module if module else '')
                        imports.add(module)
                        
                        # Also add 'from X import Y' as 'X.Y' if Y might be a module
                        for alias in node.names:
                            if alias.name != '*':
                                full_name = f"{module}.{alias.name}" if module and not module.startswith('.') else alias.name
                                imports.add(full_name)
                    else:
                        # Handle 'from . import Y' (relative import with no module)
                        module = '.' * node.level
                        for alias in node.names:
                            if alias.name != '*':
                                imports.add(f"{module}{alias.name}")
        
        except SyntaxError as e:
            self.errors.append(f"Syntax error in {file_path}: {e}")
        except Exception as e:
            self.errors.append(f"Error parsing {file_path}: {e}")
        
        return imports
    
    def trace_dependencies(self, file_path: Path, visited: Set[Path] = None) -> None:
        """Recursively trace all dependencies of a file."""
        if visited is None:
            visited = set()
        
        if file_path in visited:
            return
        
        visited.add(file_path)
        self.used_files.add(file_path)
        
        # Extract imports from this file
        imports = self.extract_imports(file_path)
        
        # Resolve each import
        for import_name in imports:
            resolved_paths = self.resolve_import(import_name, file_path)
            
            for resolved_path in resolved_paths:
                self.dependencies[file_path].add(resolved_path)
                # Recursively trace dependencies
                self.trace_dependencies(resolved_path, visited)
    
    def analyze(self) -> None:
        """Run the complete dependency analysis."""
        print("Finding all Python files in the repository...")
        self.all_python_files = self.find_all_python_files()
        print(f"Found {len(self.all_python_files)} Python files")
        
        print("\nResolving entry points...")
        resolved_entry_points = []
        
        for entry_point in self.entry_points:
            # Try to find the entry point file
            matches = [f for f in self.all_python_files if str(f).endswith(entry_point)]
            
            if matches:
                resolved_entry_points.append(matches[0])
                print(f"  ✓ {entry_point} -> {matches[0].relative_to(self.base_path)}")
            else:
                self.warnings.append(f"Entry point not found: {entry_point}")
                print(f"  ✗ {entry_point} NOT FOUND")
        
        print(f"\nTracing dependencies from {len(resolved_entry_points)} entry points...")
        
        for i, entry_point in enumerate(resolved_entry_points, 1):
            print(f"  [{i}/{len(resolved_entry_points)}] Analyzing {entry_point.name}...")
            self.trace_dependencies(entry_point)
        
        print(f"\nAnalysis complete!")
        print(f"  Total files: {len(self.all_python_files)}")
        print(f"  Used files: {len(self.used_files)}")
        print(f"  Unused files: {len(self.all_python_files - self.used_files)}")
    
    def get_unused_files(self) -> Set[Path]:
        """Get all unused Python files."""
        return self.all_python_files - self.used_files
    
    def get_unused_folders(self) -> Set[Path]:
        """Get all folders that contain only unused files."""
        unused_files = self.get_unused_files()
        
        # Get all unique folders containing Python files
        all_folders = set()
        for file_path in self.all_python_files:
            folder = file_path.parent
            while folder != self.base_path:
                all_folders.add(folder)
                folder = folder.parent
        
        # Find folders that contain only unused files
        unused_folders = set()
        
        for folder in all_folders:
            # Get all Python files in this folder (non-recursive)
            files_in_folder = [f for f in self.all_python_files if f.parent == folder]
            
            if files_in_folder:
                # Check if all files in this folder are unused
                if all(f in unused_files for f in files_in_folder):
                    # Check if all subdirectories are also unused
                    has_used_subdir = False
                    for subdir in folder.iterdir():
                        if subdir.is_dir() and subdir in all_folders and subdir not in unused_folders:
                            has_used_subdir = True
                            break
                    
                    if not has_used_subdir:
                        unused_folders.add(folder)
        
        return unused_folders
    
    def generate_report(self) -> str:
        """Generate a detailed report of the analysis."""
        unused_files = sorted(self.get_unused_files())
        unused_folders = sorted(self.get_unused_folders())
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("DEPENDENCY ANALYSIS REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("EXECUTIVE SUMMARY")
        report_lines.append("-" * 80)
        report_lines.append(f"Total Python files in repository: {len(self.all_python_files)}")
        report_lines.append(f"Used files (imported directly or transitively): {len(self.used_files)}")
        report_lines.append(f"Unused files: {len(unused_files)}")
        report_lines.append(f"Usage rate: {len(self.used_files) / len(self.all_python_files) * 100:.1f}%")
        report_lines.append("")
        
        # Get all folders containing Python files
        all_folders_with_py = set()
        for file_path in self.all_python_files:
            folder = file_path.parent
            while folder != self.base_path:
                all_folders_with_py.add(folder)
                folder = folder.parent
        
        report_lines.append(f"Total folders with Python files: {len(all_folders_with_py)}")
        report_lines.append(f"Completely unused folders: {len(unused_folders)}")
        report_lines.append("")
        
        # Errors and Warnings
        if self.warnings:
            report_lines.append("WARNINGS")
            report_lines.append("-" * 80)
            for warning in self.warnings:
                report_lines.append(f"  ⚠ {warning}")
            report_lines.append("")
        
        if self.errors:
            report_lines.append("ERRORS")
            report_lines.append("-" * 80)
            for error in self.errors:
                report_lines.append(f"  ✗ {error}")
            report_lines.append("")
        
        # Unused Files
        report_lines.append("UNUSED FILES")
        report_lines.append("-" * 80)
        
        if unused_files:
            # Group by folder
            files_by_folder = defaultdict(list)
            for file_path in unused_files:
                folder = file_path.parent.relative_to(self.base_path)
                files_by_folder[folder].append(file_path.name)
            
            for folder in sorted(files_by_folder.keys()):
                report_lines.append(f"\n{folder}/")
                for filename in sorted(files_by_folder[folder]):
                    report_lines.append(f"  - {filename}")
        else:
            report_lines.append("No unused files found!")
        
        report_lines.append("")
        
        # Completely Unused Folders
        report_lines.append("COMPLETELY UNUSED FOLDERS")
        report_lines.append("-" * 80)
        
        if unused_folders:
            for folder in unused_folders:
                rel_folder = folder.relative_to(self.base_path)
                # Count files in this folder
                files_count = len([f for f in self.all_python_files if f.parent == folder])
                report_lines.append(f"  - {rel_folder}/ ({files_count} file(s))")
        else:
            report_lines.append("No completely unused folders found!")
        
        report_lines.append("")
        
        # Recommendations
        report_lines.append("RECOMMENDATIONS")
        report_lines.append("-" * 80)
        
        if unused_files:
            report_lines.append("Consider removing or archiving the unused files and folders identified above.")
            report_lines.append("Before deletion, verify that:")
            report_lines.append("  1. These files are not used by external tools or scripts")
            report_lines.append("  2. They are not loaded dynamically at runtime")
            report_lines.append("  3. They are not configuration files or data files")
            report_lines.append("  4. They are not used in documentation or examples")
        else:
            report_lines.append("All Python files are in use! No cleanup needed.")
        
        report_lines.append("")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def generate_dependency_tree(self, max_depth: int = 3) -> str:
        """Generate a dependency tree for verification (limited depth)."""
        lines = []
        lines.append("DEPENDENCY TREE (Entry Points)")
        lines.append("-" * 80)
        
        # Get entry points that were successfully resolved
        resolved_entry_points = []
        for entry_point in self.entry_points:
            matches = [f for f in self.used_files if str(f).endswith(entry_point)]
            if matches:
                resolved_entry_points.append(matches[0])
        
        for entry_point in sorted(resolved_entry_points)[:10]:  # Limit to first 10 for readability
            lines.append(f"\n{entry_point.relative_to(self.base_path)}")
            self._add_dependency_tree(entry_point, lines, depth=1, max_depth=max_depth, visited=set())
        
        if len(resolved_entry_points) > 10:
            lines.append(f"\n... and {len(resolved_entry_points) - 10} more entry points")
        
        return "\n".join(lines)
    
    def _add_dependency_tree(self, file_path: Path, lines: List[str], depth: int, max_depth: int, visited: Set[Path]) -> None:
        """Helper method to recursively build dependency tree."""
        if depth > max_depth or file_path in visited:
            return
        
        visited.add(file_path)
        
        deps = sorted(self.dependencies.get(file_path, []))
        for dep in deps[:5]:  # Limit to 5 deps per file
            indent = "  " * depth
            lines.append(f"{indent}└─ {dep.relative_to(self.base_path)}")
            self._add_dependency_tree(dep, lines, depth + 1, max_depth, visited)
        
        if len(deps) > 5:
            indent = "  " * depth
            lines.append(f"{indent}└─ ... and {len(deps) - 5} more dependencies")


def main():
    # Configuration
    base_path = Path("/home/runner/work/mdwiki-python-files/mdwiki-python-files")
    
    entry_points = [
        "mdpy/find_replace_bot/bot.py",
        "db_work/days_7.py",
        "mdpyget/sqlviews_new.py",
        "mdpyget/getas.py",
        "mdpyget/enwiki_views.py",
        "updates/io.py",
        "updates/listo.py",
        "updates/Medicine_articles.py",
        "mdpy/fix_duplicate.py",
        "add_rtt/pup.py",
        "fix_user_pages/bot.py",
        "fix_cs1/bot.py",
        "fix_cs1/fix_cs_params/bot.py",
        "mdpages/cashwd.py",
        "copy_data/by_qid/sitelinks.py",
        "apis/cat_cach.py",
        "copy_data/by_title/all_articles.py",
        "copy_data/by_title/exists_db.py",
        "wd_works/recheck.py",
        "db_work/check_titles.py",
        "copy_to_en/revid.py",
        "mdcount/countref.py",
        "mdcount/words.py",
        "mass/radio/cases_in_ids.py",
        "mass/radio/st3/count.py",
    ]
    
    exclude_folders = ["newupdater", ".git", "__pycache__", ".venv", "venv"]
    
    # Run analysis
    analyzer = DependencyAnalyzer(base_path, entry_points, exclude_folders)
    analyzer.analyze()
    
    # Generate and print report
    report = analyzer.generate_report()
    print("\n" + report)
    
    # Save report to file
    report_file = base_path / "unused_files_report.txt"
    with open(report_file, 'w') as f:
        f.write(report)
        f.write("\n\n")
        f.write(analyzer.generate_dependency_tree())
    
    print(f"\nFull report saved to: {report_file}")
    
    # Also save as JSON for programmatic access
    unused_files = [str(f.relative_to(base_path)) for f in sorted(analyzer.get_unused_files())]
    unused_folders = [str(f.relative_to(base_path)) for f in sorted(analyzer.get_unused_folders())]
    
    json_report = {
        "summary": {
            "total_files": len(analyzer.all_python_files),
            "used_files": len(analyzer.used_files),
            "unused_files": len(unused_files),
            "unused_folders": len(unused_folders),
        },
        "unused_files": unused_files,
        "unused_folders": unused_folders,
        "warnings": analyzer.warnings,
        "errors": analyzer.errors,
    }
    
    json_file = base_path / "unused_files_report.json"
    with open(json_file, 'w') as f:
        json.dump(json_report, f, indent=2)
    
    print(f"JSON report saved to: {json_file}")


if __name__ == "__main__":
    main()
