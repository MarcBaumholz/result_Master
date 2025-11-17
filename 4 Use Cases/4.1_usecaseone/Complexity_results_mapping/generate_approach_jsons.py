#!/usr/bin/env python3
"""
Generate approach-specific JSON files from API comparison files.
Creates one JSON per approach containing all 11 APIs.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class ApproachJsonGenerator:
    """Generates approach-specific JSON files from comparison data."""
    
    def __init__(self, comparison_dir: str, output_dir: str):
        self.comparison_dir = Path(comparison_dir)
        self.output_dir = Path(output_dir)
    
    def read_comparison_file(self, api_name: str) -> Dict[str, Any]:
        """Read a comparison file for an API."""
        filepath = self.comparison_dir / f"{api_name}_comparison.json"
        
        if not filepath.exists():
            print(f"Warning: {filepath.name} not found")
            return {}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_approach_data(self, api_name: str, approach: str, comparison_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data for a specific approach from comparison data."""
        if not comparison_data or 'fields_comparison' not in comparison_data:
            return {}
        
        # Build mapped_fields structure
        mapped_fields = {}
        
        for field_name, field_data in comparison_data['fields_comparison'].items():
            if approach in field_data:
                mapped_fields[field_name] = field_data[approach]
        
        # Calculate metrics
        tp = fp = fn = tn = 0
        
        if 'accuracy_metrics' in comparison_data and approach in comparison_data['accuracy_metrics']:
            metrics = comparison_data['accuracy_metrics'][approach]
            tp = metrics.get('correct', 0)
            fp = metrics.get('incorrect', 0)
            fn = metrics.get('unmappable', 0)
            # TN would need to be calculated differently
        
        # Calculate precision, recall, f1
        precision = (tp / (tp + fp) * 100) if (tp + fp) > 0 else 0.0
        recall = (tp / (tp + fn) * 100) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        
        return {
            "api_name": api_name,
            "total_fields": len(mapped_fields),
            "mapped_fields": mapped_fields,
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
    
    def generate_approach_json(self, approach: str, apis: List[str]) -> Dict[str, Any]:
        """Generate a JSON file for a specific approach containing all APIs."""
        approach_data = {
            "approach": approach,
            "description": self.get_approach_description(approach),
            "total_apis": len(apis),
            "apis": {}
        }
        
        total_tp = total_fp = total_fn = total_tn = 0
        
        for api in apis:
            comparison_data = self.read_comparison_file(api)
            api_data = self.extract_approach_data(api, approach, comparison_data)
            
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
            print(f"Generating: {filename}")
            print(f"{'='*80}")
            
            approach_data = self.generate_approach_json(approach, apis)
            
            # Save to file
            output_path = self.output_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(approach_data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Created {filename}")
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
    output_dir = comparison_dir  # Save in same directory
    
    print("="*80)
    print("Approach-specific JSON Generator")
    print("="*80)
    print(f"Input directory: {comparison_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    generator = ApproachJsonGenerator(comparison_dir, output_dir)
    generator.generate_all_approach_jsons()
    
    print("\n" + "="*80)
    print("✓ All approach JSON files generated successfully!")
    print("="*80)


if __name__ == "__main__":
    main()

