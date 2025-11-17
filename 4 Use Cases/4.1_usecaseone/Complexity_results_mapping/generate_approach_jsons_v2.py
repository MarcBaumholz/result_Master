#!/usr/bin/env python3
"""
Generate approach-specific JSON files with Ground Truth comparison.
Each field shows: Ground Truth vs. Mapping Result
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class ApproachJsonGeneratorV2:
    """Generates approach-specific JSON files with Ground Truth data."""
    
    def __init__(self, comparison_dir: str, ground_truth_dir: str, output_dir: str):
        self.comparison_dir = Path(comparison_dir)
        self.ground_truth_dir = Path(ground_truth_dir)
        self.output_dir = Path(output_dir)
    
    def read_json_file(self, filepath: Path) -> Dict[str, Any]:
        """Read a JSON file."""
        if not filepath.exists():
            return {}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def read_ground_truth(self, api_name: str) -> Dict[str, Any]:
        """Read ground truth file for an API."""
        # Try both naming conventions
        gt_file = self.ground_truth_dir / f"{api_name}_ground_truth.json"
        if not gt_file.exists():
            gt_file = self.ground_truth_dir / f"{api_name}_enhanced_ground_truth.json"
        
        return self.read_json_file(gt_file)
    
    def read_comparison_file(self, api_name: str) -> Dict[str, Any]:
        """Read comparison file for an API."""
        filepath = self.comparison_dir / f"{api_name}_comparison.json"
        return self.read_json_file(filepath)
    
    def extract_approach_data_with_gt(self, api_name: str, approach: str, 
                                      comparison_data: Dict[str, Any],
                                      ground_truth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data with Ground Truth comparison."""
        if not comparison_data or 'fields_comparison' not in comparison_data:
            return {}
        
        # Build field comparison structure
        fields_with_gt = {}
        
        for field_name, field_data in comparison_data['fields_comparison'].items():
            # Get ground truth for this field
            gt_info = field_data.get('ground_truth', {})
            
            # Get approach mapping
            approach_info = field_data.get(approach, {})
            
            # Create comparison structure
            fields_with_gt[field_name] = {
                "ground_truth": {
                    "target_field": gt_info.get('target_field', 'N/A'),
                    "notes": gt_info.get('notes', ''),
                    "mapping_type": gt_info.get('mapping_type', 'Unknown')
                },
                "mapped": {
                    "target_field": approach_info.get('target_field', 'N/A'),
                    "notes": approach_info.get('notes', ''),
                    "mapping_type": approach_info.get('mapping_type', 'Unknown')
                },
                "is_correct": self.check_if_correct(
                    gt_info.get('target_field', 'N/A'),
                    approach_info.get('target_field', 'N/A')
                )
            }
        
        # Calculate metrics from accuracy_metrics if available
        tp = fp = fn = tn = 0
        
        if 'accuracy_metrics' in comparison_data and approach in comparison_data['accuracy_metrics']:
            metrics = comparison_data['accuracy_metrics'][approach]
            tp = metrics.get('correct', 0)
            fp = metrics.get('incorrect', 0)
            fn_val = metrics.get('unmappable', 0)
            # Note: the 'unmappable' in accuracy_metrics might be FN
            
            # Count correctly
            for field_name, field_comp in fields_with_gt.items():
                gt_target = field_comp['ground_truth']['target_field']
                mapped_target = field_comp['mapped']['target_field']
                
                if gt_target in ['N/A', 'unmappable', 'derived']:
                    if mapped_target in ['N/A', 'unmappable']:
                        tn += 1
                    else:
                        fp += 1
                else:
                    if mapped_target in ['N/A', 'unmappable']:
                        fn += 1
                    elif field_comp['is_correct']:
                        tp += 1
                    else:
                        fp += 1
        
        # Calculate precision, recall, f1
        precision = (tp / (tp + fp) * 100) if (tp + fp) > 0 else 0.0
        recall = (tp / (tp + fn) * 100) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        
        return {
            "api_name": api_name,
            "total_fields": len(fields_with_gt),
            "fields": fields_with_gt,
            "metrics": {
                "TP": tp,
                "FP": fp,
                "FN": fn,
                "TN": tn,
                "precision": round(precision, 2),
                "recall": round(recall, 2),
                "f1_score": round(f1, 2)
            }
        }
    
    def check_if_correct(self, ground_truth: str, mapped: str) -> bool:
        """Check if mapping is correct (relaxed matching)."""
        if ground_truth == "N/A" or mapped == "N/A":
            return False
        
        # Normalize
        gt_norm = ground_truth.lower().strip()
        mapped_norm = mapped.lower().strip()
        
        # Handle unmappable
        if gt_norm in ["unmappable", "derived"] or mapped_norm in ["unmappable", "(no match)"]:
            return gt_norm == mapped_norm
        
        # Exact match
        if gt_norm == mapped_norm:
            return True
        
        # Containment (relaxed)
        if gt_norm in mapped_norm or mapped_norm in gt_norm:
            return True
        
        return False
    
    def generate_approach_json(self, approach: str, apis: List[str]) -> Dict[str, Any]:
        """Generate JSON for an approach with Ground Truth comparison."""
        approach_data = {
            "approach": approach,
            "description": self.get_approach_description(approach),
            "total_apis": len(apis),
            "apis": {}
        }
        
        total_tp = total_fp = total_fn = total_tn = 0
        
        for api in apis:
            print(f"  Processing {api}...")
            
            comparison_data = self.read_comparison_file(api)
            ground_truth_data = self.read_ground_truth(api)
            
            api_data = self.extract_approach_data_with_gt(
                api, approach, comparison_data, ground_truth_data
            )
            
            if api_data:
                approach_data["apis"][api] = api_data
                
                # Aggregate totals
                total_tp += api_data['metrics']['TP']
                total_fp += api_data['metrics']['FP']
                total_fn += api_data['metrics']['FN']
                total_tn += api_data['metrics']['TN']
        
        # Calculate overall metrics
        overall_precision = (total_tp / (total_tp + total_fp) * 100) if (total_tp + total_fp) > 0 else 0.0
        overall_recall = (total_tp / (total_tp + total_fn) * 100) if (total_tp + total_fn) > 0 else 0.0
        overall_f1 = (2 * overall_precision * overall_recall / (overall_precision + overall_recall)) if (overall_precision + overall_recall) > 0 else 0.0
        
        approach_data["overall_metrics"] = {
            "total_TP": total_tp,
            "total_FP": total_fp,
            "total_FN": total_fn,
            "total_TN": total_tn,
            "overall_precision": round(overall_precision, 2),
            "overall_recall": round(overall_recall, 2),
            "overall_f1_score": round(overall_f1, 2)
        }
        
        return approach_data
    
    def get_approach_description(self, approach: str) -> str:
        """Get description for an approach."""
        descriptions = {
            "single_prompt": "Single-Prompt approach using only LLM intrinsic knowledge without external context",
            "rag": "Basic RAG (Retrieval-Augmented Generation) with direct access to API specifications",
            "enhanced_rag": "Enhanced RAG with structured retrieval pipelines and intelligent terminology normalization",
            "complete_arch": "Complete Architecture with integrated tool-use, validation, and verification modules"
        }
        return descriptions.get(approach, "Unknown approach")
    
    def generate_all_approach_jsons(self):
        """Generate JSON files for all approaches."""
        apis = ['adb', 'bamboo', 'flip', 'hibob', 'oracle', 
                'personio', 'rippling', 'sage', 'sap', 'stackone', 'workday']
        
        approaches = {
            'single_prompt': 'single_prompt_all_apis.json',
            'rag': 'rag_all_apis.json',
            'enhanced_rag': 'enhanced_rag_all_apis.json',
            'complete_arch': 'complete_arch_all_apis.json'
        }
        
        for approach, filename in approaches.items():
            print(f"\n{'='*80}")
            print(f"Generating: {filename} (with Ground Truth)")
            print(f"{'='*80}")
            
            approach_data = self.generate_approach_json(approach, apis)
            
            # Save to file
            output_path = self.output_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(approach_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n✓ Created {filename}")
            print(f"  Total APIs: {approach_data['total_apis']}")
            print(f"  Overall Precision: {approach_data['overall_metrics']['overall_precision']:.2f}%")
            print(f"  Overall Recall: {approach_data['overall_metrics']['overall_recall']:.2f}%")
            print(f"  Overall F1-Score: {approach_data['overall_metrics']['overall_f1_score']:.2f}%")
            print(f"  Total TP: {approach_data['overall_metrics']['total_TP']}")
            print(f"  Total FP: {approach_data['overall_metrics']['total_FP']}")
            print(f"  Total FN: {approach_data['overall_metrics']['total_FN']}")
            print(f"  Total TN: {approach_data['overall_metrics']['total_TN']}")


def main():
    """Main entry point."""
    base_dir = "/Users/marcbaumholz/Library/CloudStorage/OneDrive-FlipGmbH/github_repo/4 Use Cases/4.1_usecaseone/Complexity_results_mapping"
    comparison_dir = f"{base_dir}/comparison_results"
    ground_truth_dir = f"{base_dir}/ground_truth"
    output_dir = comparison_dir
    
    print("="*80)
    print("Approach-specific JSON Generator V2")
    print("WITH GROUND TRUTH COMPARISON")
    print("="*80)
    print(f"Comparison directory: {comparison_dir}")
    print(f"Ground Truth directory: {ground_truth_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    generator = ApproachJsonGeneratorV2(comparison_dir, ground_truth_dir, output_dir)
    generator.generate_all_approach_jsons()
    
    print("\n" + "="*80)
    print("✓ All approach JSON files generated with Ground Truth!")
    print("="*80)


if __name__ == "__main__":
    main()

