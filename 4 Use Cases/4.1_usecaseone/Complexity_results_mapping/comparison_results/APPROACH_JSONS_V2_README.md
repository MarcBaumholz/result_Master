# 📊 Approach-Specific JSON Files V2 - WITH GROUND TRUTH

## ✅ Was ist neu?

**Version 2** enthält jetzt für **jedes Feld** einen direkten Vergleich:
- ✅ **Ground Truth** Target Field + Notes + Mapping Type
- ✅ **Mapped** (Mapping-Ergebnis) Target Field + Notes + Mapping Type
- ✅ **is_correct** Boolean (Match zwischen Ground Truth und Mapping)

---

## 📁 Neue Struktur pro Feld

```json
{
  "field_name": {
    "ground_truth": {
      "target_field": "associateOID",
      "notes": "Employee ID mapped to associateOID in ADP",
      "mapping_type": "Direct"
    },
    "mapped": {
      "target_field": "data.eventContext.associateOID",
      "notes": "Direct mapping - employee identifier in eventContext",
      "mapping_type": "Direct"
    },
    "is_correct": true
  }
}
```

### Vorher (V1) ❌:
```json
{
  "field_name": {
    "target_field": "data.eventContext.associateOID",
    "notes": "...",
    "mapping_type": "Direct"
  }
}
```
**Problem**: Ground Truth fehlte - Kein Vergleich möglich!

### Jetzt (V2) ✅:
```json
{
  "field_name": {
    "ground_truth": { ... },   // Was sollte es sein
    "mapped": { ... },          // Was wurde gemappt
    "is_correct": true/false    // Stimmt es überein?
  }
}
```
**Vorteil**: Direkter Vergleich sichtbar!

---

## 📊 Die 4 JSON-Dateien

| Datei | Größe | F1-Score | Precision | Recall | Beste Eigenschaft |
|-------|-------|----------|-----------|--------|-------------------|
| `single_prompt_all_apis.json` | ~50 KB | **73.91%** | 69.39% | 79.07% | 🥇 Beste Balance |
| `complete_arch_all_apis.json` | ~55 KB | 54.81% | 42.53% | 77.08% | - |
| `enhanced_rag_all_apis.json` | ~52 KB | 52.14% | 39.04% | 78.49% | - |
| `rag_all_apis.json` | ~45 KB | 38.95% | 25.37% | 83.87% | ⚠️ Hohe FP-Rate |

### Neue Metriken (mit korrekter TN-Berechnung):

| Ansatz | TP | FP | FN | TN | Precision | Recall | F1 |
|--------|----|----|----|----|-----------|--------|-----|
| **Single-Prompt** | **102** | 45 | 27 | 25 | **69.39%** | 79.07% | **73.91%** |
| Complete Arch | 74 | 100 | 22 | 14 | 42.53% | 77.08% | 54.81% |
| Enhanced RAG | 73 | 114 | 20 | 6 | 39.04% | 78.49% | 52.14% |
| Basic RAG | 52 | 153 | 10 | 10 | 25.37% | 83.87% | 38.95% |

---

## 🔍 Beispiele

### Beispiel 1: Korrektes Mapping ✅

```bash
# BambooHR - employee_external_id in Single Prompt
cat single_prompt_all_apis.json | jq '.apis.bamboo.fields.employee_external_id'
```

```json
{
  "ground_truth": {
    "target_field": "employeeId",
    "notes": "Employee ID passed as path parameter in BambooHR API",
    "mapping_type": "Direct"
  },
  "mapped": {
    "target_field": "employeeId",
    "notes": "Employee ID passed as path parameter in URL, not in request body",
    "mapping_type": "Conversion"
  },
  "is_correct": true  ✅
}
```

**Analyse**: Mapping korrekt! Beide verwenden `employeeId`.

---

### Beispiel 2: Falsches Mapping ❌

```bash
# ADB - amount in Single Prompt
cat single_prompt_all_apis.json | jq '.apis.adb.fields.amount'
```

```json
{
  "ground_truth": {
    "target_field": "days",
    "notes": "Amount mapped to days field in response schema",
    "mapping_type": "Conversion"
  },
  "mapped": {
    "target_field": "unmappable",
    "notes": "API doesn't track absence amounts in request",
    "mapping_type": "Unmappable"
  },
  "is_correct": false  ❌
}
```

**Analyse**: Single Prompt übersieht das `days` Feld - False Negative!

---

### Beispiel 3: Halluzination (FP) 🔴

```bash
# Rippling - employee_external_id in Enhanced RAG
cat enhanced_rag_all_apis.json | jq '.apis.rippling.fields.employee_external_id'
```

```json
{
  "ground_truth": {
    "target_field": "N/A",
    "notes": "Field not found in ground truth",
    "mapping_type": "N/A"
  },
  "mapped": {
    "target_field": "worker_id",
    "notes": "Direct mapping - Rippling uses worker_id",
    "mapping_type": "Direct"
  },
  "is_correct": false  ❌
}
```

**Analyse**: Enhanced RAG "erfindet" ein Mapping für ein Feld, das nicht existiert - False Positive!

---

## 🎯 Use Cases

### 1. **Finde alle False Negatives für eine API**

```python
import json

with open('single_prompt_all_apis.json') as f:
    data = json.load(f)

api = 'adb'
false_negatives = []

for field, field_data in data['apis'][api]['fields'].items():
    gt = field_data['ground_truth']['target_field']
    mapped = field_data['mapped']['target_field']
    
    # False Negative: Ground Truth hat Wert, aber Mapping sagt "unmappable"
    if gt not in ['N/A', 'unmappable', 'derived']:
        if mapped in ['N/A', 'unmappable']:
            false_negatives.append({
                'field': field,
                'ground_truth': gt,
                'missed': True
            })

print(f"False Negatives for {api}: {len(false_negatives)}")
for fn in false_negatives:
    print(f"  - {fn['field']}: Should be '{fn['ground_truth']}' but was marked unmappable")
```

---

### 2. **Finde alle False Positives für eine API**

```python
import json

with open('enhanced_rag_all_apis.json') as f:
    data = json.load(f)

api = 'oracle'
false_positives = []

for field, field_data in data['apis'][api]['fields'].items():
    gt = field_data['ground_truth']['target_field']
    mapped = field_data['mapped']['target_field']
    is_correct = field_data['is_correct']
    
    # False Positive: Ground Truth sagt N/A/unmappable, aber Mapping hat Wert
    if gt in ['N/A', 'unmappable', 'derived']:
        if mapped not in ['N/A', 'unmappable']:
            false_positives.append({
                'field': field,
                'invented': mapped,
                'notes': field_data['mapped']['notes']
            })
    # Oder: Ground Truth hat Wert, aber Mapping ist falsch
    elif not is_correct and mapped not in ['N/A', 'unmappable']:
        false_positives.append({
            'field': field,
            'should_be': gt,
            'mapped_to': mapped
        })

print(f"False Positives for {api}: {len(false_positives)}")
```

---

### 3. **Vergleiche alle Ansätze für ein spezifisches Feld**

```python
import json

field_name = "employee_external_id"
api_name = "bamboo"

approaches = ['single_prompt', 'rag', 'enhanced_rag', 'complete_arch']

print(f"\n{api_name} - {field_name}:")
print(f"{'='*80}")

for approach in approaches:
    with open(f'{approach}_all_apis.json') as f:
        data = json.load(f)
        
    field_data = data['apis'][api_name]['fields'][field_name]
    
    print(f"\n{approach.upper()}:")
    print(f"  Ground Truth: {field_data['ground_truth']['target_field']}")
    print(f"  Mapped:       {field_data['mapped']['target_field']}")
    print(f"  Correct:      {'✅' if field_data['is_correct'] else '❌'}")
```

**Output:**
```
bamboo - employee_external_id:
================================================================================

SINGLE_PROMPT:
  Ground Truth: employeeId
  Mapped:       employeeId
  Correct:      ✅

RAG:
  Ground Truth: employeeId
  Mapped:       employee_external_id
  Correct:      ❌

ENHANCED_RAG:
  Ground Truth: employeeId
  Mapped:       employeeId
  Correct:      ✅

COMPLETE_ARCH:
  Ground Truth: employeeId
  Mapped:       employee_external_id
  Correct:      ❌
```

---

### 4. **Accuracy-Report pro API generieren**

```python
import json

def generate_api_report(api_name):
    approaches = ['single_prompt', 'rag', 'enhanced_rag', 'complete_arch']
    
    print(f"\n{'='*80}")
    print(f"API: {api_name.upper()}")
    print(f"{'='*80}\n")
    
    for approach in approaches:
        with open(f'{approach}_all_apis.json') as f:
            data = json.load(f)
        
        api_data = data['apis'][api_name]
        metrics = api_data['metrics']
        
        print(f"{approach.upper()}:")
        print(f"  TP: {metrics['TP']:3d}  |  FP: {metrics['FP']:3d}")
        print(f"  FN: {metrics['FN']:3d}  |  TN: {metrics['TN']:3d}")
        print(f"  Precision: {metrics['precision']:6.2f}%")
        print(f"  Recall:    {metrics['recall']:6.2f}%")
        print(f"  F1-Score:  {metrics['f1_score']:6.2f}%")
        print()

# Für alle APIs
for api in ['adb', 'bamboo', 'flip', 'hibob', 'oracle', 
            'personio', 'rippling', 'sage', 'sap', 'stackone', 'workday']:
    generate_api_report(api)
```

---

### 5. **Beste Ansatz-Empfehlung pro API**

```python
import json

approaches = ['single_prompt', 'rag', 'enhanced_rag', 'complete_arch']
apis = ['adb', 'bamboo', 'flip', 'hibob', 'oracle', 
        'personio', 'rippling', 'sage', 'sap', 'stackone', 'workday']

recommendations = {}

for api in apis:
    best_f1 = 0
    best_approach = None
    
    for approach in approaches:
        with open(f'{approach}_all_apis.json') as f:
            data = json.load(f)
        
        f1 = data['apis'][api]['metrics']['f1_score']
        
        if f1 > best_f1:
            best_f1 = f1
            best_approach = approach
    
    recommendations[api] = (best_approach, best_f1)

print("PRODUCTION RECOMMENDATIONS:")
print(f"{'='*80}\n")

for api, (approach, f1) in sorted(recommendations.items()):
    print(f"{api:12s} → {approach:20s} (F1: {f1:6.2f}%)")
```

---

## 📊 Detaillierte Statistiken

### Single-Prompt (Best Overall: 73.91% F1)

```
Total Fields Evaluated: 199
  ✅ TP: 102 (51.3%) - Correct mappings
  ❌ FP:  45 (22.6%) - Wrong mappings (Hallucinations)
  ⚠️  FN:  27 (13.6%) - Missed mappings
  ✅ TN:  25 (12.6%) - Correctly identified unmappable fields

Precision: 69.39% (2 von 3 Mappings sind korrekt)
Recall:    79.07% (Findet 4 von 5 korrekten Mappings)
F1-Score:  73.91% 🥇
```

### Basic RAG (Worst: 38.95% F1)

```
Total Fields Evaluated: 225
  ✅ TP:  52 (23.1%) - Correct mappings
  ❌ FP: 153 (68.0%) 🔴 - MASSIVE Halluzinationen!
  ⚠️  FN:  10 ( 4.4%) - Missed mappings
  ✅ TN:  10 ( 4.4%) - Correctly identified unmappable

Precision: 25.37% ❌ (3 von 4 Mappings sind FALSCH!)
Recall:    83.87% ✅ (Findet fast alle korrekten Mappings)
F1-Score:  38.95% 
```

### Key Insight:
**Basic RAG findet zwar viele korrekte Mappings (hoher Recall), aber erfindet massiv falsche Mappings (153 FP!)** - Daher katastrophale Precision.

---

## 🎓 Erkenntnisse aus V2

### 1. **True Negatives sind wichtig!**

V1 hatte **keine TN-Metrik**. V2 zeigt jetzt:
- Single-Prompt: 25 TN - Erkennt unmappbare Felder am besten
- Basic RAG: 10 TN - Versucht fast alles zu mappen
- Enhanced RAG: 6 TN - Noch aggressiver
- Complete Arch: 14 TN - Moderate Erkennung

**Bedeutung**: Ein gutes System muss auch erkennen, was **nicht mappbar** ist!

### 2. **Ground Truth Varianz**

Manche APIs haben mehr N/A-Felder in Ground Truth:
- Flip: Wenige N/A (Referenz-API ist komplett)
- ADB: Mehr N/A (Ground Truth unvollständig)
- Rippling: Mix aus beiden

**Bedeutung**: Ground Truth Qualität variiert - Metriken vorsichtig interpretieren!

### 3. **Mapping Type Mismatch**

Oft ist `mapping_type` unterschiedlich:
```
Ground Truth: "Direct"
Mapped:       "Conversion"
```

Das kann trotzdem **korrekt** sein, wenn das Target Field stimmt!

---

## 🚀 Production Deployment

### Empfohlene Konfiguration:

```python
PRODUCTION_CONFIG = {
    # Single-Prompt für 8 APIs (Best F1)
    'flip': 'single_prompt',      # 73.91% avg
    'bamboo': 'single_prompt',
    'hibob': 'single_prompt',
    'oracle': 'single_prompt',
    'personio': 'single_prompt',
    'sage': 'single_prompt',
    'stackone': 'single_prompt',
    'workday': 'single_prompt',
    
    # Enhanced RAG für 2 APIs
    'adb': 'enhanced_rag',        # Besser bei komplexen APIs
    'rippling': 'enhanced_rag',
    
    # Complete Arch für 1 API
    'sap': 'complete_arch',       # Einziger funktionierender Ansatz
}
```

### Quality Gates:

```python
def should_use_mapping(ground_truth, mapped, is_correct):
    """Entscheide ob Mapping verwendet werden soll."""
    
    # Wenn Ground Truth N/A ist und wir ein Mapping haben
    if ground_truth in ['N/A', 'unmappable']:
        if mapped not in ['N/A', 'unmappable']:
            # Potentieller False Positive - Manuelle Review!
            return "MANUAL_REVIEW"
    
    # Wenn explizit als korrekt markiert
    if is_correct:
        return "ACCEPT"
    
    # Wenn Ground Truth existiert aber Mapping fehlt
    if ground_truth not in ['N/A', 'unmappable']:
        if mapped in ['N/A', 'unmappable']:
            # False Negative - Versuche anderen Ansatz
            return "TRY_FALLBACK"
    
    # Wenn beide existieren aber nicht matchen
    if not is_correct:
        # False Positive - Reject oder Manual Review
        return "REJECT_OR_REVIEW"
    
    return "UNKNOWN"
```

---

## 📝 Generierung

Erstellt mit:
```bash
python3 generate_approach_jsons_v2.py
```

**Features:**
- ✅ Liest Ground Truth aus `/ground_truth/`
- ✅ Liest Comparison Data aus `/comparison_results/`
- ✅ Kombiniert beide in neue Struktur
- ✅ Berechnet `is_correct` mit relaxed matching
- ✅ Zählt TP, FP, FN, TN korrekt
- ✅ Berechnet Precision, Recall, F1

**Reproduzierbar**: Jederzeit neu generierbar!

---

**Version**: 2.0  
**Erstellt**: 16. November 2025  
**Format**: JSON (pretty-printed, UTF-8)  
**Größe**: ~50-55 KB pro Datei  
**Status**: ✅ Production-ready mit Ground Truth Comparison

