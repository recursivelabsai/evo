# Algorithm Optimization Prompt Template

You are an expert algorithm optimizer working with the EvoChat system. Your task is to help optimize the following algorithm while maintaining correctness.

## Original Algorithm

```{{language}}
{{code}}
```

## Evolution Goal

{{goal}}

## Context Information

{{#if domain_specific_knowledge}}
### Domain-Specific Knowledge
{{domain_specific_knowledge}}
{{/if}}

{{#if previous_optimizations}}
### Relevant Previous Optimizations
The following optimizations have been successful for similar algorithms:

{{previous_optimizations}}
{{/if}}

{{#if symbolic_residue}}
### Symbolic Residue
The following near-misses or innovative fragments from previous evolutions may be relevant:

{{symbolic_residue}}
{{/if}}

## Your Task

1. **Analyze the current implementation**:
   - Identify the algorithm type
   - Determine the current time complexity (Big O notation)
   - Determine the current space complexity (Big O notation)
   - Identify any inefficiencies or redundant operations

2. **Propose an optimized version**:
   - Create a complete implementation, not just snippets
   - Ensure it maintains all functionality of the original algorithm
   - Focus on {{optimization_focus}} as the primary optimization goal
   - Balance other considerations: {{secondary_considerations}}

3. **Explain your optimization**:
   - Describe your approach and reasoning
   - Analyze the time complexity of your solution
   - Analyze the space complexity of your solution
   - Discuss any trade-offs you made

## Guidelines

- Ensure your solution is correct first, then optimize for performance
- Consider standard algorithmic techniques (memoization, dynamic programming, etc.) where appropriate
- If you recognize this as a standard algorithm type, consider well-known optimizations
- Balance readability with performance - avoid overly complex solutions unless the performance gain is significant
- Pay attention to edge cases (empty inputs, single elements, etc.)

## Output Format

```{{language}}
# Optimized Algorithm
# Time Complexity: O(?)
# Space Complexity: O(?)

[Your optimized code here]
```

Then provide a brief explanation of:
1. Your optimization approach
2. How it improves upon the original algorithm
3. Any trade-offs or limitations
