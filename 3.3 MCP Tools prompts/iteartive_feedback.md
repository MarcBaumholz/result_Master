---

## Übersicht

Das Tool verwendet das **ReAct Pattern (Think-Act-Observe)** für iteratives Field Mapping mit Feedback-Loop:

1. **THINK Phase** - Analysiert Situation und plant nächste Aktion
2. **ACT Phase** - Führt Mapping-Aktion aus
3. **OBSERVE Phase** - Validiert Ergebnis und erhält Feedback

---

## ReAct Pattern Workflow

```
For each iteration (max 3 iterations):
  1. THINK → Analyze & Plan
     ↓
  2. ACT → Execute Mapping
     ↓
  3. OBSERVE → Validate & Get Feedback
     ↓
  If success AND confidence > 0.7:
    → Break (early success)
  Else:
    → Continue to next iteration
```

---

## 1. THINK Phase Prompt

**Method:** `_think()`  
**Location:** `iterative_mapping_with_feedback_combined.py:110-165`  
**Purpose:** Analysiert die aktuelle Situation und plant die nächste Aktion

### Complete Prompt Template

```
You are an expert API field mapping agent using the ReAct pattern.

TASK: Map the source field '{source_field}' to the best matching field in the target API.

CURRENT ITERATION: {iteration + 1}/{max_iterations}

RAG ANALYSIS RESULTS:
{rag_results_json}

{history_context}

THINK: Analyze the current situation and plan your next action.
Consider:
1. What have we learned from previous attempts?
2. What is the best field match based on RAG results?
3. How should we test this mapping?

Provide your reasoning in 2-3 sentences.
```

### Variable Placeholders

#### `{source_field}`
- **Type:** String
- **Description:** Name des zu mappenden Source-Feldes
- **Example:** `"employee_id"`, `"start_date"`, `"status"`

#### `{iteration + 1}`
- **Type:** Integer
- **Description:** Aktuelle Iterationsnummer (1-basiert)
- **Example:** `1`, `2`, `3`

#### `{max_iterations}`
- **Type:** Integer
- **Description:** Maximale Anzahl Iterationen (default: 3, konfigurierbar via `MAX_ITERATIONS` env var)
- **Example:** `3`

#### `{rag_results_json}`
- **Type:** JSON String
- **Description:** JSON-formatierte RAG-Ergebnisse für das Source-Feld
- **Format:** Array von RAG-Ergebnissen

#### `{history_context}`
- **Type:** String (optional)
- **Description:** Kontext aus vorherigen Iterationen (nur wenn History vorhanden)
- **Format:** Formatiert als Markdown-Liste

### RAG Results JSON Format

```json
[
  {
    "text": "The employee_id field is a required string parameter...",
    "semantic_score": 0.92,
    "chunk_type": "parameter_definition",
    "metadata": {
      "endpoint": "POST /api/employees",
      "parameter": "body.employee_id"
    }
  },
  {
    "text": "employee_id property schema definition...",
    "semantic_score": 0.87,
    "chunk_type": "schema_property",
    "metadata": {
      "schema_path": "#/components/schemas/Employee/properties/employee_id"
    }
  },
  {
    "text": "Field validation rules for employee_id...",
    "semantic_score": 0.81,
    "chunk_type": "validation_rules",
    "metadata": {}
  }
]
```

### History Context Format

```
Previous attempts:

- Thought: [Previous thought from iteration 1]
- Action: [Previous action from iteration 1]
- Result: [Previous observation from iteration 1]

- Thought: [Previous thought from iteration 2]
- Action: [Previous action from iteration 2]
- Result: [Previous observation from iteration 2]
```

### Expected Response Format

Die LLM sollte eine kurze Analyse (2-3 Sätze) zurückgeben, die:
- Was aus vorherigen Versuchen gelernt wurde
- Den besten Field-Match basierend auf RAG-Ergebnissen identifiziert
- Eine Test-Strategie vorschlägt

**Example Response:**
```
Based on the RAG results, I can see that 'employee_id' maps strongly to the 'id' field in the target API (score 0.92). However, previous attempts showed that 'id' might be too generic. I should try 'employee_id' directly first, as it has semantic alignment and appears in multiple RAG results. I'll validate this by checking if the field exists in the POST /api/employees endpoint schema.
```

---

## 2. ACT Phase Prompt

**Method:** `_act()`  
**Location:** `iterative_mapping_with_feedback_combined.py:167-222`  
**Purpose:** Führt die geplante Mapping-Aktion aus

### Complete Prompt Template

```
Based on your analysis: {thought}

Execute the mapping action for field '{source_field}'.

Return a JSON object with:
{
    "target_field": "best_matching_field_name",
    "confidence": 0.95,
    "reasoning": "why this field matches",
    "test_strategy": "how to validate this mapping"
}

Focus on the most promising field match from the RAG results.
```

### Variable Placeholders

#### `{thought}`
- **Type:** String
- **Description:** Die Analyse aus der THINK-Phase
- **Example:** `"Based on the RAG results, I can see that 'employee_id' maps strongly..."`

#### `{source_field}`
- **Type:** String
- **Description:** Name des zu mappenden Source-Feldes
- **Example:** `"employee_id"`

### Expected JSON Response Format

```json
{
    "target_field": "employee_id",
    "confidence": 0.92,
    "reasoning": "Strong semantic match found in RAG results with score 0.92. The field appears in POST /api/employees endpoint with matching data type (string). Previous attempts showed that generic 'id' was too broad, so using the specific field name is better.",
    "test_strategy": "Validate by checking if 'employee_id' exists in the request body schema of POST /api/employees endpoint. Verify data type compatibility (string to string). Check if field is required."
}
```

### Response Fields Explanation

- **`target_field`**: Name des besten passenden Feldes im Target-API
- **`confidence`**: Confidence-Score zwischen 0.0 und 1.0
- **`reasoning`**: Begründung für diese Mapping-Entscheidung
- **`test_strategy`**: Strategie zur Validierung des Mappings

### JSON Parsing

Das Tool verwendet robustes JSON-Parsing:
1. Findet erste `{` und letzte `}`
2. Extrahiert JSON-String
3. Parst JSON
4. Erstellt `ActionResult` Objekt

**Fallback bei Parsing-Fehler:**
- `target_field`: Setzt auf `source_field`
- `confidence`: 0.0
- `method`: "json_parse_error" oder "no_json"
- `reasoning`: Fehlerbeschreibung

---

## 3. OBSERVE Phase

**Method:** `_observe()`  
**Location:** `iterative_mapping_with_feedback_combined.py:224-253`  
**Purpose:** Validiert das Mapping-Ergebnis gegen API-Spec

### Process (No LLM Prompt)

Die OBSERVE-Phase verwendet **keinen LLM-Prompt**, sondern:
1. **API Spec Validation**: Verwendet `verifier.verify_field_mapping()`
2. **Comprehensive Validation**: Prüft ob Feld in API-Spec existiert
3. **Returns**: Validation-Ergebnis mit Score

### Validation Result Format

```python
{
    'success': True,  # Boolean: Feld gefunden?
    'validation_score': 0.95,  # Float: 0.0-1.0
    'endpoint_used': '/api/employees',  # String: Endpoint oder Schema-Pfad
    # Optional:
    'error': None  # String: Fehlerbeschreibung falls vorhanden
}
```

---