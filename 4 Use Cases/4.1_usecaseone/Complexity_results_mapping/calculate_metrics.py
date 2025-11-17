#!/usr/bin/env python3
"""
Calculate TP, FP, FN, TN metrics from comparison files.
Uses relaxed matching: if ground truth field is contained in mapped field, it counts as correct.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple


class MetricsCalculator:
    """Calculate confusion matrix metrics with relaxed field matching."""
    
    def __init__(self, comparison_dir: str):
        self.comparison_dir = Path(comparison_dir)
    
    def is_field_match(self, ground_truth: str, mapped: str) -> bool:
        """
        Check if fields match with relaxed criteria.
        If ground truth field is contained in mapped field, it's a match.
        """
        if ground_truth == "N/A" or mapped == "N/A":
            return False
        
        # Normalize fields
        gt_normalized = ground_truth.lower().strip()
        mapped_normalized = mapped.lower().strip()
        
        # Special cases
        if gt_normalized == "unmappable" or mapped_normalized == "unmappable":
            return gt_normalized == mapped_normalized
        
        if mapped_normalized == "(no match)":
            return False
        
        # Exact match
        if gt_normalized == mapped_normalized:
            return True
        
        # Check if ground truth is contained in mapped field (relaxed)
        # e.g., "leaveTypeCode.codeValue" in "data.transform.workerLeave.leaveAbsence.leaveTypeCode.codeValue"
        if gt_normalized in mapped_normalized:
            return True
        
        # Check if mapped is contained in ground truth
        if mapped_normalized in gt_normalized:
            return True
        
        return False
    
    def calculate_metrics_for_api(self, api_name: str, approach: str) -> Dict[str, int]:
        """Calculate TP, FP, FN, TN for a specific API and approach."""
        comparison_file = self.comparison_dir / f"{api_name}_comparison.json"
        
        if not comparison_file.exists():
            return {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
        
        with open(comparison_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        TP = 0  # Correct mappings
        FP = 0  # Incorrect mappings (hallucinations)
        FN = 0  # Missed mappings
        TN = 0  # Correctly identified unmappable fields
        
        for field_name, comparisons in data['fields_comparison'].items():
            gt = comparisons.get('ground_truth', {})
            approach_data = comparisons.get(approach, {})
            
            gt_target = gt.get('target_field', 'N/A')
            approach_target = approach_data.get('target_field', 'N/A')
            
            # Skip if both are N/A
            if gt_target == "N/A" and approach_target == "N/A":
                continue
            
            # Ground truth says it's unmappable
            if gt_target in ["N/A", "unmappable", "derived", "(No Match)"]:
                if approach_target in ["N/A", "unmappable", "(No Match)"]:
                    TN += 1  # Correctly identified as unmappable
                else:
                    FP += 1  # False positive - mapped something that shouldn't be
            else:
                # Ground truth has a valid mapping
                if approach_target in ["N/A", "unmappable", "(No Match)"]:
                    FN += 1  # False negative - missed a valid mapping
                else:
                    # Check if it's a correct mapping
                    if self.is_field_match(gt_target, approach_target):
                        TP += 1  # Correct mapping
                    else:
                        FP += 1  # Wrong mapping (hallucination)
        
        return {"TP": TP, "FP": FP, "FN": FN, "TN": TN}
    
    def calculate_precision_recall_f1(self, metrics: Dict[str, int]) -> Tuple[float, float, float]:
        """Calculate Precision, Recall, and F1-Score."""
        TP = metrics['TP']
        FP = metrics['FP']
        FN = metrics['FN']
        
        # Precision = TP / (TP + FP)
        precision = (TP / (TP + FP) * 100) if (TP + FP) > 0 else 0.0
        
        # Recall = TP / (TP + FN)
        recall = (TP / (TP + FN) * 100) if (TP + FN) > 0 else 0.0
        
        # F1-Score = 2 * (Precision * Recall) / (Precision + Recall)
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        
        return precision, recall, f1
    
    def generate_results_table(self, approach: str, apis: list) -> str:
        """Generate a formatted results table for an approach."""
        results = []
        total_tp = total_fp = total_fn = total_tn = 0
        
        for api in apis:
            metrics = self.calculate_metrics_for_api(api, approach)
            precision, recall, f1 = self.calculate_precision_recall_f1(metrics)
            
            results.append({
                'api': api.upper() if api != 'flip' else 'Flip',
                'TP': metrics['TP'],
                'FP': metrics['FP'],
                'FN': metrics['FN'],
                'TN': metrics['TN'],
                'precision': precision,
                'recall': recall,
                'f1': f1
            })
            
            total_tp += metrics['TP']
            total_fp += metrics['FP']
            total_fn += metrics['FN']
            total_tn += metrics['TN']
        
        # Calculate overall metrics
        overall_precision = (total_tp / (total_tp + total_fp) * 100) if (total_tp + total_fp) > 0 else 0.0
        overall_recall = (total_tp / (total_tp + total_fn) * 100) if (total_tp + total_fn) > 0 else 0.0
        overall_f1 = (2 * overall_precision * overall_recall / (overall_precision + overall_recall)) if (overall_precision + overall_recall) > 0 else 0.0
        
        # Format table
        table = "API Spec Name\tTP\tFP\tFN\tTN\tPrecision (%)\tRecall (%)\tF1-Score (%)\n"
        for r in results:
            api_name = r['api']
            if api_name == 'ADB':
                api_name = 'ADP'
            elif api_name == 'STACKONE':
                api_name = 'StackOne'
            elif api_name == 'HIBOB':
                api_name = 'HiBob'
            elif api_name == 'BAMBOO':
                api_name = 'BambooHR'
            
            table += f"{api_name}\t{r['TP']}\t{r['FP']}\t{r['FN']}\t{r['TN']}\t{r['precision']:.1f}\t{r['recall']:.1f}\t{r['f1']:.1f}\n"
        
        return table, {
            'total_tp': total_tp,
            'total_fp': total_fp,
            'total_fn': total_fn,
            'total_tn': total_tn,
            'precision': overall_precision,
            'recall': overall_recall,
            'f1': overall_f1
        }
    
    def generate_all_results(self):
        """Generate results for all approaches."""
        apis = ['flip', 'adb', 'bamboo', 'hibob', 'oracle', 'personio', 
                'rippling', 'sage', 'sap', 'stackone', 'workday']
        
        approaches = {
            'single_prompt': 'Single-Prompt',
            'rag': 'Basic RAG',
            'enhanced_rag': 'Enhanced RAG',
            'complete_arch': 'Complete Architecture'
        }
        
        all_results = {}
        
        for approach_key, approach_name in approaches.items():
            table, totals = self.generate_results_table(approach_key, apis)
            all_results[approach_name] = {
                'table': table,
                'totals': totals
            }
            
            print(f"\n{'='*80}")
            print(f"{approach_name} Results")
            print(f"{'='*80}")
            print(table)
            print(f"\nOverall: Precision={totals['precision']:.1f}%, Recall={totals['recall']:.1f}%, F1={totals['f1']:.1f}%")
            print(f"Totals: TP={totals['total_tp']}, FP={totals['total_fp']}, FN={totals['total_fn']}, TN={totals['total_tn']}")
        
        return all_results


def main():
    """Main entry point."""
    comparison_dir = "/Users/marcbaumholz/Library/CloudStorage/OneDrive-FlipGmbH/github_repo/4 Use Cases/4.1_usecaseone/Complexity_results_mapping/comparison_results"
    
    calculator = MetricsCalculator(comparison_dir)
    results = calculator.generate_all_results()
    
    # Generate summary table
    print(f"\n{'='*80}")
    print("Summary Table")
    print(f"{'='*80}")
    print("Methode\tPrecision (%)\tRecall (%)\tF1-Score (%)\tGesamt TP\tGesamt FP\tGesamt FN\tGesamt TN")
    
    for approach_name, data in results.items():
        totals = data['totals']
        print(f"{approach_name}\t{totals['precision']:.1f}\t{totals['recall']:.1f}\t{totals['f1']:.1f}\t"
              f"{totals['total_tp']}\t{totals['total_fp']}\t{totals['total_fn']}\t{totals['total_tn']}")


if __name__ == "__main__":
    main()

