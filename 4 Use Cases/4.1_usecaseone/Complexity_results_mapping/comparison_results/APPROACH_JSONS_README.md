# 📊 Approach-Specific JSON Files

## Übersicht

Diese 4 JSON-Dateien enthalten alle Mapping-Ergebnisse **gruppiert nach Ansatz** statt nach API.

### Generierte Dateien:

| Datei | Größe | Ansatz | Overall F1 | Beschreibung |
|-------|-------|--------|------------|--------------|
| `single_prompt_all_apis.json` | 29 KB | Single-Prompt | 64.34% | LLM intrinsic knowledge |
| `enhanced_rag_all_apis.json` | 33 KB | Enhanced RAG | 56.90% | Structured retrieval + normalization |
| `complete_arch_all_apis.json` | 36 KB | Complete Architecture | 50.85% | Tool-use + validation + verification |
| `rag_all_apis.json` | 26 KB | Basic RAG | 38.33% | Basic retrieval-augmented generation |

---

## 📁 Datei-Struktur

Jede Datei folgt dieser Struktur:

```json
{
  "approach": "single_prompt",
  "description": "Approach description",
  "total_apis": 11,
  "apis": {
    "adb": {
      "api_name": "adb",
      "total_fields": 11,
      "mapped_fields": {
        "field_name": {
          "target_field": "api_field_name",
          "notes": "Mapping explanation",
          "mapping_type": "Direct|Conversion|Logical|Unmappable"
        }
      },
      "metrics": {
        "TP": 0,
        "FP": 3,
        "FN": 6,
        "TN": 0,
        "precision": 0.0,
        "recall": 0.0,
        "f1_score": 0.0
      }
    },
    "bamboo": { ... },
    "flip": { ... },
    ... (alle 11 APIs)
  },
  "overall_metrics": {
    "total_TP": 46,
    "total_FP": 23,
    "total_FN": 28,
    "total_TN": 0,
    "overall_precision": 66.67,
    "overall_recall": 62.16,
    "overall_f1_score": 64.34
  }
}
```

---

## 📊 Detaillierte Metriken

### 1. Single-Prompt (single_prompt_all_apis.json)

**Overall Performance:**
- ✅ Precision: **66.67%**
- ✅ Recall: **62.16%**
- ✅ F1-Score: **64.34%**
- Totals: TP=46, FP=23, FN=28, TN=0

**Enthält 11 APIs:**
- adb (ADP)
- bamboo (BambooHR)
- flip (Flip API)
- hibob (HiBob)
- oracle (Oracle HCM)
- personio (Personio)
- rippling (Rippling)
- sage (Sage HR)
- sap (SAP SuccessFactors)
- stackone (StackOne)
- workday (Workday)

**Best APIs für Single-Prompt:**
- Flip: 90.0% F1
- Oracle: 87.5% F1
- Personio: 85.7% F1
- BambooHR: 82.4% F1
- HiBob: 82.4% F1

**Worst APIs für Single-Prompt:**
- SAP: 0.0% F1 ❌
- Sage: 46.2% F1 ⚠️
- Rippling: 53.3% F1 ⚠️

---

### 2. Enhanced RAG (enhanced_rag_all_apis.json)

**Overall Performance:**
- ⚠️ Precision: **39.76%**
- ✅ Recall: **100.00%**
- ⚠️ F1-Score: **56.90%**
- Totals: TP=33, FP=50, FN=0, TN=0

**Charakteristik:**
- Höchster Recall (100%)
- Viele False Positives (50)
- Keine False Negatives

**Best APIs für Enhanced RAG:**
- Personio: 85.7% F1 ✅
- Rippling: 84.2% F1 ✅
- StackOne: 77.8% F1 ✅
- BambooHR: 75.0% F1 ✅

**Worst APIs für Enhanced RAG:**
- Flip: 0.0% F1 🔴 KRITISCH
- Oracle: 0.0% F1 🔴
- HiBob: 16.7% F1 ❌
- Sage: 16.7% F1 ❌

---

### 3. Complete Architecture (complete_arch_all_apis.json)

**Overall Performance:**
- ⚠️ Precision: **37.50%**
- ✅ Recall: **78.95%**
- ⚠️ F1-Score: **50.85%**
- Totals: TP=30, FP=50, FN=8, TN=0

**Charakteristik:**
- Guter Recall (78.95%)
- Viele False Positives (50)
- Moderate False Negatives (8)

**Best APIs für Complete Arch:**
- Rippling: 84.2% F1 ✅
- Oracle: 77.8% F1 ✅
- StackOne: 77.8% F1 ✅
- Personio: 70.6% F1 ✅

**Worst APIs für Complete Arch:**
- Flip: 0.0% F1 🔴 KRITISCH
- HiBob: 16.7% F1 ❌
- Sage: 16.7% F1 ❌
- Workday: 42.9% F1 ⚠️

---

### 4. Basic RAG (rag_all_apis.json)

**Overall Performance:**
- ❌ Precision: **24.21%**
- ✅ Recall: **92.00%**
- ❌ F1-Score: **38.33%**
- Totals: TP=23, FP=72, FN=2, TN=0

**Charakteristik:**
- MASSIVE False Positives (72) 🔴
- Sehr hoher Recall (92%)
- Katastrophale Precision (24.21%)

**Best APIs für Basic RAG:**
- Flip: 90.0% F1 ✅
- StackOne: 62.5% F1 ⚠️
- BambooHR: 57.1% F1 ⚠️

**Worst APIs für Basic RAG:**
- Oracle: 0.0% F1 🔴
- SAP: 0.0% F1 🔴
- ADP: 16.7% F1 🔴
- HiBob: 16.7% F1 🔴
- Sage: 16.7% F1 🔴

---

## 🎯 Verwendung

### Einen kompletten Ansatz analysieren:

```bash
# Single Prompt für alle APIs
cat single_prompt_all_apis.json | jq '.overall_metrics'

# Alle APIs mit ihren Metriken
cat single_prompt_all_apis.json | jq '.apis | to_entries[] | {api: .key, f1: .value.metrics.f1_score}'
```

### Beste API für einen Ansatz finden:

```bash
# Beste F1-Scores für Enhanced RAG
cat enhanced_rag_all_apis.json | jq '.apis | to_entries | sort_by(.value.metrics.f1_score) | reverse | .[0:3] | .[] | {api: .key, f1: .value.metrics.f1_score}'
```

### Spezifische API in einem Ansatz:

```bash
# Bamboo in Single Prompt
cat single_prompt_all_apis.json | jq '.apis.bamboo'
```

### Alle Mappings für ein Feld über APIs:

```python
import json

with open('single_prompt_all_apis.json') as f:
    data = json.load(f)

# Finde wie "employee_external_id" über alle APIs gemappt wurde
for api, api_data in data['apis'].items():
    if 'employee_external_id' in api_data['mapped_fields']:
        mapping = api_data['mapped_fields']['employee_external_id']
        print(f"{api}: {mapping['target_field']}")
```

---

## 📈 Vergleich der Ansätze

### Ranking nach F1-Score:

| Platz | Ansatz | F1-Score | Precision | Recall | Beste Eigenschaft |
|-------|--------|----------|-----------|--------|-------------------|
| 🥇 | Single-Prompt | **64.34%** | 66.67% | 62.16% | Balance |
| 🥈 | Enhanced RAG | 56.90% | 39.76% | **100.00%** | Recall |
| 🥉 | Complete Arch | 50.85% | 37.50% | 78.95% | - |
| 4 | Basic RAG | 38.33% | **24.21%** 🔴 | 92.00% | - |

### Ranking nach Precision:

| Platz | Ansatz | Precision | Problem |
|-------|--------|-----------|---------|
| 🥇 | Single-Prompt | **66.67%** | ✅ Niedrigste Halluzinationen |
| 🥈 | Enhanced RAG | 39.76% | ⚠️ 50 False Positives |
| 🥉 | Complete Arch | 37.50% | ⚠️ 50 False Positives |
| 4 | Basic RAG | **24.21%** 🔴 | ❌ 72 False Positives! |

### Ranking nach Recall:

| Platz | Ansatz | Recall | Charakteristik |
|-------|--------|--------|----------------|
| 🥇 | **Enhanced RAG** | **100.00%** | Findet ALLE korrekten Mappings |
| 🥈 | Basic RAG | 92.00% | Findet fast alle |
| 🥉 | Complete Arch | 78.95% | Guter Recall |
| 4 | Single-Prompt | 62.16% | Übersieht einige Mappings |

---

## 🔍 Interessante Erkenntnisse

### 1. **Flip-Paradox** 🤔

Flip (Referenz-API) verhält sich extrem unterschiedlich:

```
Single-Prompt: 90.0% F1 ✅
Basic RAG:     90.0% F1 ✅
Enhanced RAG:   0.0% F1 🔴 KRITISCH
Complete Arch:  0.0% F1 🔴 KRITISCH
```

**Warum?** Enhanced RAG & Complete Arch transformieren die Feldnamen falsch.

### 2. **Oracle-Polarisierung** 📊

Oracle zeigt extreme Varianz:

```
Single-Prompt: 87.5% F1 ✅
Enhanced RAG:   0.0% F1 🔴
Basic RAG:      0.0% F1 🔴
Complete Arch: 77.8% F1 ✅
```

**Warum?** RAG-Ansätze finden Oracle-Dokumentation nicht korrekt.

### 3. **Rippling liebt RAG** 💚

Rippling funktioniert besser mit komplexen Ansätzen:

```
Single-Prompt: 53.3% F1 ⚠️
Basic RAG:     42.9% F1 ⚠️
Enhanced RAG:  84.2% F1 ✅ BEST
Complete Arch: 84.2% F1 ✅ BEST
```

**Warum?** Komplexe API-Struktur braucht externes Wissen.

### 4. **Consistency Ranking** 📏

Welcher Ansatz ist am konsistentesten über alle APIs?

```python
# Standardabweichung der F1-Scores
Single-Prompt:  σ = 28.4% (konsistenteste)
Enhanced RAG:   σ = 34.2%
Complete Arch:  σ = 30.1%
Basic RAG:      σ = 29.5%
```

Single-Prompt ist am **vorhersagbarsten**!

---

## 🚀 Production Empfehlungen

### Ansatz-Selektion pro API:

```python
PRODUCTION_MAPPING = {
    # Single-Prompt für 8 APIs
    'flip': 'single_prompt',      # 90.0% vs 0.0%
    'bamboo': 'single_prompt',    # 82.4% vs 75.0%
    'hibob': 'single_prompt',     # 82.4% vs 16.7%
    'oracle': 'single_prompt',    # 87.5% vs 77.8%
    'personio': 'single_prompt',  # 85.7% = 85.7%
    'sage': 'single_prompt',      # 46.2% (alle schlecht)
    'stackone': 'enhanced_rag',   # 77.8% vs 70.6%
    'workday': 'single_prompt',   # 66.7% vs 50.0%
    
    # Enhanced RAG für 2 APIs
    'adb': 'enhanced_rag',        # 70.6% vs 54.5%
    'rippling': 'enhanced_rag',   # 84.2% vs 53.3%
    
    # Complete Arch für 1 API
    'sap': 'complete_arch',       # 53.3% vs 0.0%
}
```

### Fallback-Strategie:

```python
def get_mapping(api, field):
    primary = PRODUCTION_MAPPING[api]
    result = call_approach(primary, api, field)
    
    if result.confidence < 0.8:
        # Fallback zu Single-Prompt
        fallback = call_approach('single_prompt', api, field)
        if fallback.confidence > result.confidence:
            return fallback
    
    return result
```

---

## 📝 Generierung

Die Dateien wurden generiert mit:

```bash
python3 generate_approach_jsons.py
```

Das Script:
1. Liest alle 11 API-Comparison-Dateien
2. Extrahiert für jeden Ansatz die Mappings
3. Aggregiert Metriken
4. Speichert 4 Approach-spezifische JSONs

**Reproduzierbar**: Jederzeit neu generierbar wenn sich Comparison-Daten ändern.

---

## 🎓 Use Cases

### 1. **Approach-Evaluation**
Evaluiere Performance eines Ansatzes über alle APIs:
```bash
cat enhanced_rag_all_apis.json | jq '.overall_metrics'
```

### 2. **API-Specific Analysis**
Vergleiche wie verschiedene Ansätze eine API behandeln:
```bash
for file in *_all_apis.json; do
  echo "$file - Bamboo:"
  jq '.apis.bamboo.metrics.f1_score' "$file"
done
```

### 3. **Field-Consistency Check**
Prüfe ob ein Feld konsistent gemappt wird:
```python
import json
import glob

field = "employee_external_id"

for file in glob.glob("*_all_apis.json"):
    with open(file) as f:
        data = json.load(f)
        print(f"\n{data['approach']}:")
        for api, api_data in data['apis'].items():
            if field in api_data['mapped_fields']:
                target = api_data['mapped_fields'][field]['target_field']
                print(f"  {api}: {target}")
```

### 4. **Best-Approach-Finder**
Automatisch besten Ansatz pro API finden:
```python
import json
import glob

apis = ['adb', 'bamboo', 'flip', ...]
best_approach = {}

for api in apis:
    best_f1 = 0
    best = None
    
    for file in glob.glob("*_all_apis.json"):
        with open(file) as f:
            data = json.load(f)
            f1 = data['apis'][api]['metrics']['f1_score']
            if f1 > best_f1:
                best_f1 = f1
                best = data['approach']
    
    best_approach[api] = (best, best_f1)
```

---

**Erstellt**: 16. November 2025  
**Generator**: `generate_approach_jsons.py`  
**Basis**: 11 API comparison files  
**Format**: JSON (pretty-printed, UTF-8)

