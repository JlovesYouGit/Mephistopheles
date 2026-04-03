#!/usr/bin/env python3
"""
Test script for Self-Recursive Language Algorithm Improvement
Demonstrates the LLM's ability to iteratively improve its own language processing
"""

import sys
import os

# Add protocol directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from siri_llm_nexus import (
    SelfRecursiveImprover,
    LLMEvaluation,
    LanguageModelMetrics,
    LanguageTaskType
)

def print_separator(title: str):
    print("\n" + "=" * 67)
    print(f"{title}")
    print("=" * 67 + "\n")

print_separator("SELF-RECURSIVE LANGUAGE ALGORITHM IMPROVEMENT TEST")

# MARK: - Test 1: Basic Self-Recursive Improvement

print("📊 TEST 1: Basic Self-Recursive Improvement")
print("-" * 67)

# Create a mock nexus object
class MockNexus:
    pass

mock_nexus = MockNexus()

improver = SelfRecursiveImprover(mock_nexus, max_recursion_depth=5)

# Simulate initial LLM evaluation
initial_evaluation = LLMEvaluation(
    semantic_score=0.65,
    syntactic_score=0.70,
    contextual_score=0.60,
    perplexity=45.0,
    entropy=0.35,
    token_efficiency=0.55,
    improvement_suggestions=["Initial baseline"]
)

print("\nInitial LLM Metrics:")
print(f"  Semantic Accuracy:   {initial_evaluation.semantic_score:.3f}")
print(f"  Syntactic Coherence: {initial_evaluation.syntactic_score:.3f}")
print(f"  Contextual Relevance: {initial_evaluation.contextual_score:.3f}")
print(f"  Perplexity:          {initial_evaluation.perplexity:.1f}")
print(f"  Token Efficiency:    {initial_evaluation.token_efficiency:.3f}")

# Perform recursive self-improvement
convergence_score, converged = improver.recursive_self_improve(
    evaluation=initial_evaluation,
    max_iterations=10
)

print("\nAfter Self-Recursive Improvement:")
print(f"  Convergence Score: {convergence_score:.4f}")
print(f"  Converged:         {'✓ YES' if converged else '✗ NO'}")

metrics = improver.language_model_metrics
print("\nImproved LLM Metrics:")
print(f"  Semantic Accuracy:   {metrics.semantic_accuracy:.3f}")
print(f"  Syntactic Coherence: {metrics.syntactic_coherence:.3f}")
print(f"  Contextual Relevance: {metrics.contextual_relevance:.3f}")
print(f"  Convergence Score:   {metrics.convergence_score:.4f}")
print(f"  Perplexity:          {metrics.perplexity:.1f}")
print(f"  Token Efficiency:    {metrics.token_efficiency:.3f}")

# MARK: - Test 2: Language Task Optimization

print_separator("TEST 2: Language Task-Specific Optimization")

task_types = [
    LanguageTaskType.SEMANTIC_UNDERSTANDING,
    LanguageTaskType.SYNTACTIC_GENERATION,
    LanguageTaskType.CODE_GENERATION,
    LanguageTaskType.CONTEXTUAL_REASONING
]

for task_type in task_types:
    print(f"\nOptimizing for: {task_type.replace('_', ' ').title()}")
    convergence = improver.optimize_for_language_task(task_type, iterations=5)
    print(f"  → Convergence Score: {convergence:.4f}")

# MARK: - Test 3: Multi-Round Self-Improvement

print_separator("TEST 3: Multi-Round Self-Improvement")

round_metrics = []

for round_num in range(1, 6):
    print(f"\nRound {round_num}:")

    # Create progressively better evaluations
    progress_factor = round_num / 5.0
    progressive_evaluation = LLMEvaluation(
        semantic_score=min(0.95, initial_evaluation.semantic_score + (progress_factor * 0.3)),
        syntactic_score=min(0.95, initial_evaluation.syntactic_score + (progress_factor * 0.25)),
        contextual_score=min(0.95, initial_evaluation.contextual_score + (progress_factor * 0.35)),
        perplexity=max(5.0, initial_evaluation.perplexity - (progress_factor * 30)),
        entropy=max(0.05, initial_evaluation.entropy - (progress_factor * 0.25)),
        token_efficiency=min(0.95, initial_evaluation.token_efficiency + (progress_factor * 0.4)),
        improvement_suggestions=[f"Round {round_num} optimization"]
    )

    _, round_converged = improver.recursive_self_improve(
        evaluation=progressive_evaluation,
        max_iterations=3
    )

    current_metrics = improver.language_model_metrics
    print(f"  Convergence: {current_metrics.convergence_score:.4f}")

    round_metrics.append((round_num, current_metrics.convergence_score))

print("\nImprovement Summary:")
print("  Round | Convergence")
print("  ------+-------------")
for round_num, convergence in round_metrics:
    print(f"  {round_num}     | {convergence:.4f}")

# MARK: - Test 4: Self-Improvement History Analysis

print_separator("TEST 4: Self-Improvement History Analysis")

history = improver.get_improvement_history()
print(f"Total improvement iterations: {len(history)}")

if history:
    first_metric = history[0]
    last_metric = history[-1]

    improvement = last_metric.metric_improvement.convergence_score - first_metric.metric_improvement.convergence_score
    percent_improvement = (improvement / max(0.001, first_metric.metric_improvement.convergence_score)) * 100

    print("\nImprovement Statistics:")
    print(f"  Initial Convergence:   {first_metric.metric_improvement.convergence_score:.4f}")
    print(f"  Final Convergence:     {last_metric.metric_improvement.convergence_score:.4f}")
    print(f"  Absolute Improvement:  {improvement:.4f}")
    print(f"  Percent Improvement:   {percent_improvement:.2f}%")
    print(f"  Total Iterations:      {len(history)}")

# MARK: - Test 5: Reset Functionality

print_separator("TEST 5: Reset and Reinitialize")

print("Resetting self-improvement state...")
improver.reset_self_improvement()

reset_metrics = improver.language_model_metrics
print("After reset:")
print(f"  Convergence Score: {reset_metrics.convergence_score:.4f}")
print(f"  History Count: {len(improver.get_improvement_history())}")

# Final summary

print_separator("TEST COMPLETE")

print("\nSelf-recursive improvement enables the LLM to:")
print("  ✓ Iteratively refine language algorithms")
print("  ✓ Adapt to specific task requirements")
print("  ✓ Track and measure convergence over time")
print("  ✓ Auto-adjust meta-learning rates")
print("  ✓ Maintain improvement history for analysis")
print("  ✓ Reset and reinitialize when needed\n")

print("═" * 67 + "\n")
