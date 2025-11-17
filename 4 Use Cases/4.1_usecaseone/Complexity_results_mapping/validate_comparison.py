#!/usr/bin/env python3
"""
Validation script to verify the quality and consistency of comparison files.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class ComparisonValidator:
    """Validates comparison files for correctness and consistency."""
    
    def __init__(self, comparison_dir: str):
        self.comparison_dir = Path(comparison_dir)
        self.issues = []
        self.stats = {
            "total_files": 0,
            "total_fields": 0,
            "total_comparisons": 0,
            "missing_data": 0,
            "inconsistencies": 0
        }
    
    def validate_comparison_file(self, filepath: Path) -> Dict[str, Any]:
        """Validate a single comparison file."""
        print(f"\n{'='*80}")
        print(f"Validating: {filepath.name}")
        print(f"{'='*80}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            issue = f"❌ ERROR: Could not read {filepath.name}: {e}"
            print(issue)
            self.issues.append(issue)
            return {}
        
        self.stats["total_files"] += 1
        issues_found = []
        
        # Check required top-level keys
        required_keys = ["api_name", "total_fields", "files_analyzed", "fields_comparison"]
        for key in required_keys:
            if key not in data:
                issue = f"  ❌ Missing required key: {key}"
                print(issue)
                issues_found.append(issue)
        
        # Check files_analyzed
        if "files_analyzed" in data:
            sources = ["ground_truth", "single_prompt", "rag", "enhanced_rag", "complete_arch"]
            for source in sources:
                if source not in data["files_analyzed"]:
                    issue = f"  ⚠️  Missing source file: {source}"
                    print(issue)
                    issues_found.append(issue)
        
        # Check fields_comparison
        if "fields_comparison" in data:
            fields = data["fields_comparison"]
            self.stats["total_fields"] += len(fields)
            
            print(f"\n  Total fields to compare: {len(fields)}")
            
            for field_name, field_data in fields.items():
                self.stats["total_comparisons"] += 5  # 5 sources per field
                
                # Check each source has required keys
                for source in ["ground_truth", "single_prompt", "rag", "enhanced_rag", "complete_arch"]:
                    if source not in field_data:
                        issue = f"  ❌ Field '{field_name}' missing source: {source}"
                        print(issue)
                        issues_found.append(issue)
                        self.stats["missing_data"] += 1
                    else:
                        source_data = field_data[source]
                        if "target_field" not in source_data:
                            issue = f"  ❌ Field '{field_name}' -> {source} missing 'target_field'"
                            print(issue)
                            issues_found.append(issue)
                            self.stats["missing_data"] += 1
        
        # Check accuracy_metrics if present
        if "accuracy_metrics" in data:
            metrics = data["accuracy_metrics"]
            print(f"\n  Accuracy Metrics:")
            for approach, scores in metrics.items():
                if "accuracy" in scores:
                    print(f"    {approach:20s}: {scores['accuracy']:6.2f}% "
                          f"({scores.get('correct', 0)}/{scores.get('total_evaluated', 0)})")
        
        if not issues_found:
            print(f"\n  ✅ All checks passed!")
        else:
            print(f"\n  ⚠️  Found {len(issues_found)} issues")
            self.issues.extend(issues_found)
        
        return data
    
    def validate_summary(self, summary_path: Path):
        """Validate the summary comparison file."""
        print(f"\n{'='*80}")
        print(f"Validating Summary: {summary_path.name}")
        print(f"{'='*80}")
        
        try:
            with open(summary_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            issue = f"❌ ERROR: Could not read {summary_path.name}: {e}"
            print(issue)
            self.issues.append(issue)
            return
        
        # Check required keys
        if "total_apis_analyzed" not in data:
            print("  ❌ Missing 'total_apis_analyzed'")
        else:
            print(f"  ✅ Total APIs analyzed: {data['total_apis_analyzed']}")
        
        if "overall_metrics" not in data:
            print("  ❌ Missing 'overall_metrics'")
        else:
            print(f"\n  Overall Accuracy Metrics:")
            for approach, metrics in data["overall_metrics"].items():
                if "overall_accuracy" in metrics:
                    print(f"    {approach:20s}: {metrics['overall_accuracy']:6.2f}% "
                          f"({metrics['total_correct']}/{metrics['total_evaluated']})")
        
        if "per_api_summary" not in data:
            print("  ❌ Missing 'per_api_summary'")
        else:
            print(f"\n  ✅ Per-API summary contains {len(data['per_api_summary'])} APIs")
    
    def validate_all(self):
        """Validate all comparison files."""
        print("="*80)
        print("COMPARISON FILES VALIDATION")
        print("="*80)
        
        # Get all comparison files (exclude summary and README)
        comparison_files = sorted([
            f for f in self.comparison_dir.glob("*_comparison.json")
            if f.name != "SUMMARY_COMPARISON.json"
        ])
        
        print(f"\nFound {len(comparison_files)} API comparison files")
        
        # Validate each file
        for filepath in comparison_files:
            self.validate_comparison_file(filepath)
        
        # Validate summary
        summary_path = self.comparison_dir / "SUMMARY_COMPARISON.json"
        if summary_path.exists():
            self.validate_summary(summary_path)
        else:
            print(f"\n  ⚠️  Summary file not found: {summary_path}")
        
        # Print final stats
        print(f"\n{'='*80}")
        print("VALIDATION SUMMARY")
        print(f"{'='*80}")
        print(f"  Total files validated:     {self.stats['total_files']}")
        print(f"  Total fields compared:     {self.stats['total_fields']}")
        print(f"  Total comparisons made:    {self.stats['total_comparisons']}")
        print(f"  Missing data points:       {self.stats['missing_data']}")
        print(f"  Total issues found:        {len(self.issues)}")
        
        if len(self.issues) == 0:
            print(f"\n  ✅ ALL VALIDATION CHECKS PASSED!")
        else:
            print(f"\n  ⚠️  {len(self.issues)} issues need attention")
        
        print(f"{'='*80}\n")
        
        return len(self.issues) == 0


def main():
    """Main entry point."""
    comparison_dir = "/Users/marcbaumholz/Library/CloudStorage/OneDrive-FlipGmbH/github_repo/4 Use Cases/4.1_usecaseone/Complexity_results_mapping/comparison_results"
    
    validator = ComparisonValidator(comparison_dir)
    success = validator.validate_all()
    
    # Exit with appropriate code
    exit(0 if success else 1)


if __name__ == "__main__":
    main()

