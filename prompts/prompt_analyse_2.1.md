You are given JSON payload data. Extract the relevant data fields for API mapping.

Use your judgment to determine what fields are relevant based on the data structure and content.

EXCLUDE only obvious system/metadata fields like:
- Pagination (page, pageSize, total)
- System metadata (metadata, links, etc.)

INCLUDE any field that contains business data.

JSON:
{json_data}

Return ONLY valid JSON with relevant data fields:
{
  "fields": ["field1", "field2", "nested.field", ...]
}
Step 2: Field Extraction Validation
# Validate extracted fields against programmatic extraction
# Check for missing important data fields
# Add missing fields from validation
# Report validation status
Step 3: AI-Based Semantic Descriptions
# Generate semantic descriptions for each field
# Add use-case information
# Keep descriptions concise (<=20 words)
Prompt Template
For each field, provide a concise semantic_description (<=20 words) and a short use_case (<=20 words).

Fields: {fields}
Context JSON: {json_data}

Example: 
{
  "employeeId": {
    "semantic_description": "Unique employee identifier",
    "use_case": "Join employees across systems"
  }
}
Step 4: RAG Enhancement
# For each field, gather comprehensive ground-truth snippets
# Query RAG collection with multiple strategies:
queries = [
    f"{field} property schema definition",
    f"{field} parameter definition in request",
    f"{field} field type validation rules",
    f"{field} API endpoint usage examples",
    f"{field} data format and constraints",
    f"HR {field} field mapping"
]

# Deduplicate and rank by score
# Take top 5 results per field
Step 5: Save Results
# Save as JSON and Markdown
# Include:
# - All extracted fields
# - Semantic descriptions
# - Ground truth evidence
# - Validation status
# - Enhancement confidence