Think:
            You are an expert API field mapping agent using the ReAct pattern.
            
            TASK: Map the source field '{source_field}' to the best matching field in the target API.
            
            CURRENT ITERATION: {iteration + 1}/{self.max_iterations}
            
            RAG ANALYSIS RESULTS:
            {json.dumps(rag_results, indent=2)}
            
            {history_context}
            
            THINK: Analyze the current situation and plan your next action.
            Consider:
            1. What have we learned from previous attempts?
            2. What is the best field match based on RAG results?
            3. How should we test this mapping?
            
            Provide your reasoning in 2-3 sentences.

Act:
    Based on your analysis: {thought}
            
    Execute the mapping action for field '{source_field}'.
    
    Return a JSON object with:
    - target_field: The best matching field name
    - confidence: Confidence score (0.0-1.0)
    - method: How you determined this mapping
    
    Keep response concise and valid JSON.

