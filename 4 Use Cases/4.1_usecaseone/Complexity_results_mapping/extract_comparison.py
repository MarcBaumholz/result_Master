#!/usr/bin/env python3
"""
Script to extract and compare target fields from ground truth and various mapping approaches.
Creates comparison files for each API showing ground truth vs actual mappings.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class MappingComparison:
    """Extracts and compares target field mappings across different approaches."""
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.ground_truth_dir = self.base_dir / "ground_truth"
        self.single_prompt_dir = self.base_dir / "singel_prompt"
        self.rag_dir = self.base_dir / "rag"
        self.enhanced_rag_dir = self.base_dir / "enhanced_rag"
        self.complete_arch_dir = self.base_dir / "complete_arch"
        self.output_dir = self.base_dir / "comparison_results"
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
    
    def read_json_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Read and parse JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    
    def extract_mapped_fields(self, data: Dict[str, Any], source: str) -> Dict[str, Dict[str, str]]:
        """Extract target_field and notes from mapped_fields."""
        if not data or 'mapped_fields' not in data:
            return {}
        
        result = {}
        mapped_fields = data['mapped_fields']
        
        # Handle both dict and list structures
        if isinstance(mapped_fields, list):
            # Array format: [{source_field: ..., target_field: ..., notes: ...}, ...]
            for field_data in mapped_fields:
                field_name = field_data.get('source_field', 'unknown')
                target_field = field_data.get('target_field', 'N/A')
                notes = field_data.get('notes', '')
                
                # Handle null or "(No Match)" target fields
                if target_field is None or target_field == '(No Match)':
                    target_field = 'unmappable'
                
                result[field_name] = {
                    'target_field': target_field,
                    'notes': notes,
                    'mapping_type': field_data.get('mapping_type', 'Unknown')
                }
        else:
            # Object format: {field_name: {target_field: ..., notes: ...}, ...}
            for field_name, field_data in mapped_fields.items():
                target_field = field_data.get('target_field', 'N/A')
                notes = field_data.get('notes', '')
                
                # Handle null or "(No Match)" target fields
                if target_field is None or target_field == '(No Match)':
                    target_field = 'unmappable'
                
                result[field_name] = {
                    'target_field': target_field,
                    'notes': notes,
                    'mapping_type': field_data.get('mapping_type', 'Unknown')
                }
        
        return result
    
    def get_all_field_names(self, api_name: str) -> set:
        """Get all unique field names from all sources for an API."""
        field_names = set()
        
        # Read ground truth to get base fields
        gt_file = self.ground_truth_dir / f"{api_name}_ground_truth.json"
        if not gt_file.exists():
            gt_file = self.ground_truth_dir / f"{api_name}_enhanced_ground_truth.json"
        
        gt_data = self.read_json_file(gt_file)
        if gt_data and 'mapped_fields' in gt_data:
            field_names.update(gt_data['mapped_fields'].keys())
        
        return field_names
    
    def create_comparison_for_api(self, api_name: str) -> Dict[str, Any]:
        """Create comparison data for a single API."""
        print(f"Processing {api_name}...")
        
        # Determine correct filenames
        if api_name == "adb":
            gt_file = self.ground_truth_dir / "adb_ground_truth.json"
            sp_file = self.single_prompt_dir / "adp_mapping.json"  # Note: adp not adb
            rag_file = self.rag_dir / "adb_to_flip_mapping.json"
            erag_file = self.enhanced_rag_dir / "adb_mapping_template.json"
            ca_file = self.complete_arch_dir / "adb_mapping.json"
        else:
            gt_suffix = "_ground_truth.json" if api_name in ["adb", "bamboo"] else "_enhanced_ground_truth.json"
            gt_file = self.ground_truth_dir / f"{api_name}{gt_suffix}"
            sp_file = self.single_prompt_dir / f"{api_name}_mapping.json"
            rag_file = self.rag_dir / f"{api_name}_to_flip_mapping.json"
            erag_file = self.enhanced_rag_dir / f"{api_name}_mapping_template.json"
            ca_file = self.complete_arch_dir / f"{api_name}_mapping.json"
        
        # Read all files (handle missing files gracefully)
        gt_data = self.read_json_file(gt_file) if gt_file.exists() else None
        sp_data = self.read_json_file(sp_file) if sp_file.exists() else None
        rag_data = self.read_json_file(rag_file) if rag_file.exists() else None
        erag_data = self.read_json_file(erag_file) if erag_file.exists() else None
        ca_data = self.read_json_file(ca_file) if ca_file.exists() else None
        
        # Extract mapped fields from each source
        gt_fields = self.extract_mapped_fields(gt_data, "ground_truth")
        sp_fields = self.extract_mapped_fields(sp_data, "single_prompt")
        rag_fields = self.extract_mapped_fields(rag_data, "rag")
        erag_fields = self.extract_mapped_fields(erag_data, "enhanced_rag")
        ca_fields = self.extract_mapped_fields(ca_data, "complete_arch")
        
        # Get all field names
        field_names = set()
        for fields in [gt_fields, sp_fields, rag_fields, erag_fields, ca_fields]:
            field_names.update(fields.keys())
        
        # Create comparison structure
        comparison = {
            "api_name": api_name,
            "total_fields": len(field_names),
            "files_analyzed": {
                "ground_truth": str(gt_file.name),
                "single_prompt": str(sp_file.name),
                "rag": str(rag_file.name),
                "enhanced_rag": str(erag_file.name),
                "complete_arch": str(ca_file.name)
            },
            "fields_comparison": {}
        }
        
        # Compare each field across all approaches
        for field_name in sorted(field_names):
            comparison["fields_comparison"][field_name] = {
                "ground_truth": gt_fields.get(field_name, {
                    "target_field": "N/A",
                    "notes": "Field not found in ground truth",
                    "mapping_type": "N/A"
                }),
                "single_prompt": sp_fields.get(field_name, {
                    "target_field": "N/A",
                    "notes": "Field not found in single prompt",
                    "mapping_type": "N/A"
                }),
                "rag": rag_fields.get(field_name, {
                    "target_field": "N/A",
                    "notes": "Field not found in RAG",
                    "mapping_type": "N/A"
                }),
                "enhanced_rag": erag_fields.get(field_name, {
                    "target_field": "N/A",
                    "notes": "Field not found in enhanced RAG",
                    "mapping_type": "N/A"
                }),
                "complete_arch": ca_fields.get(field_name, {
                    "target_field": "N/A",
                    "notes": "Field not found in complete architecture",
                    "mapping_type": "N/A"
                })
            }
        
        return comparison
    
    def calculate_accuracy(self, comparison: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate accuracy metrics for each approach vs ground truth."""
        fields = comparison["fields_comparison"]
        
        metrics = {
            "single_prompt": {"correct": 0, "incorrect": 0, "unmappable": 0},
            "rag": {"correct": 0, "incorrect": 0, "unmappable": 0},
            "enhanced_rag": {"correct": 0, "incorrect": 0, "unmappable": 0},
            "complete_arch": {"correct": 0, "incorrect": 0, "unmappable": 0}
        }
        
        for field_name, field_data in fields.items():
            gt_target = field_data["ground_truth"]["target_field"]
            
            # Skip if ground truth is N/A
            if gt_target == "N/A":
                continue
            
            for approach in ["single_prompt", "rag", "enhanced_rag", "complete_arch"]:
                approach_target = field_data[approach]["target_field"]
                
                if approach_target == "N/A":
                    continue
                elif approach_target == "unmappable" or gt_target == "unmappable":
                    metrics[approach]["unmappable"] += 1
                elif approach_target == gt_target:
                    metrics[approach]["correct"] += 1
                else:
                    metrics[approach]["incorrect"] += 1
        
        # Calculate percentages
        for approach, counts in metrics.items():
            total = counts["correct"] + counts["incorrect"] + counts["unmappable"]
            if total > 0:
                metrics[approach]["accuracy"] = round((counts["correct"] / total) * 100, 2)
                metrics[approach]["total_evaluated"] = total
            else:
                metrics[approach]["accuracy"] = 0
                metrics[approach]["total_evaluated"] = 0
        
        return metrics
    
    def process_all_apis(self):
        """Process all APIs and generate comparison files."""
        apis = [
            "adb", "bamboo", "flip", "hibob", "oracle",
            "personio", "rippling", "sage", "sap", "stackone", "workday"
        ]
        
        all_metrics = {}
        
        for api in apis:
            try:
                # Create comparison
                comparison = self.create_comparison_for_api(api)
                
                # Calculate accuracy metrics
                metrics = self.calculate_accuracy(comparison)
                comparison["accuracy_metrics"] = metrics
                all_metrics[api] = metrics
                
                # Save to file
                output_file = self.output_dir / f"{api}_comparison.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(comparison, f, indent=2, ensure_ascii=False)
                
                print(f"✓ Created {output_file.name}")
                
            except Exception as e:
                print(f"✗ Error processing {api}: {e}")
        
        # Create summary report
        self.create_summary_report(all_metrics)
    
    def create_summary_report(self, all_metrics: Dict[str, Dict[str, Any]]):
        """Create a summary report across all APIs."""
        summary = {
            "total_apis_analyzed": len(all_metrics),
            "overall_metrics": {
                "single_prompt": {"total_correct": 0, "total_incorrect": 0, "total_unmappable": 0},
                "rag": {"total_correct": 0, "total_incorrect": 0, "total_unmappable": 0},
                "enhanced_rag": {"total_correct": 0, "total_incorrect": 0, "total_unmappable": 0},
                "complete_arch": {"total_correct": 0, "total_incorrect": 0, "total_unmappable": 0}
            },
            "per_api_summary": {}
        }
        
        # Aggregate metrics
        for api, metrics in all_metrics.items():
            summary["per_api_summary"][api] = {}
            
            for approach in ["single_prompt", "rag", "enhanced_rag", "complete_arch"]:
                approach_metrics = metrics[approach]
                summary["per_api_summary"][api][approach] = {
                    "accuracy": approach_metrics.get("accuracy", 0),
                    "correct": approach_metrics.get("correct", 0),
                    "total": approach_metrics.get("total_evaluated", 0)
                }
                
                # Add to overall
                summary["overall_metrics"][approach]["total_correct"] += approach_metrics.get("correct", 0)
                summary["overall_metrics"][approach]["total_incorrect"] += approach_metrics.get("incorrect", 0)
                summary["overall_metrics"][approach]["total_unmappable"] += approach_metrics.get("unmappable", 0)
        
        # Calculate overall accuracy
        for approach, totals in summary["overall_metrics"].items():
            total = totals["total_correct"] + totals["total_incorrect"] + totals["total_unmappable"]
            if total > 0:
                totals["overall_accuracy"] = round((totals["total_correct"] / total) * 100, 2)
                totals["total_evaluated"] = total
            else:
                totals["overall_accuracy"] = 0
                totals["total_evaluated"] = 0
        
        # Save summary
        summary_file = self.output_dir / "SUMMARY_COMPARISON.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Created {summary_file.name}")
        print("\n=== Overall Accuracy Summary ===")
        for approach, totals in summary["overall_metrics"].items():
            print(f"{approach:20s}: {totals['overall_accuracy']:6.2f}% "
                  f"({totals['total_correct']}/{totals['total_evaluated']} correct)")


def main():
    """Main entry point."""
    base_dir = "/Users/marcbaumholz/Library/CloudStorage/OneDrive-FlipGmbH/github_repo/4 Use Cases/4.1_usecaseone/Complexity_results_mapping"
    
    print("=" * 80)
    print("Field Mapping Comparison Tool")
    print("=" * 80)
    print(f"Base directory: {base_dir}")
    print()
    
    comparator = MappingComparison(base_dir)
    comparator.process_all_apis()
    
    print("\n" + "=" * 80)
    print("Processing complete!")
    print(f"Results saved to: {comparator.output_dir}")
    print("=" * 80)


if __name__ == "__main__":
    main()

