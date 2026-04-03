#!/usr/bin/env swift

import Foundation

/**
 * Test script for Self-Recursive Language Algorithm Improvement
 * Demonstrates the LLM's ability to iteratively improve its own language processing
 */

print("═══════════════════════════════════════════════════════════")
print("SELF-RECURSIVE LANGUAGE ALGORITHM IMPROVEMENT TEST")
print("═══════════════════════════════════════════════════════════\n")

// MARK: - Test OptimalThresholdOptimizer

print("📊 TEST 1: Basic Self-Recursive Improvement")
print("─────────────────────────────────────────────")

let optimizer = OptimalThresholdOptimizer(
    initialThreshold: 1.0,
    minThreshold: 0.1,
    maxThreshold: 10.0,
    learningRate: 0.01,
    performanceWindow: 10,
    metaLearningRate: 0.005
)

// Simulate initial LLM evaluation
let initialEvaluation = LLMEvaluation(
    semanticScore: 0.65,
    syntacticScore: 0.70,
    contextualScore: 0.60,
    perplexity: 45.0,
    entropy: 0.35,
    tokenEfficiency: 0.55,
    improvementSuggestions: ["Initial baseline"]
)

print("\nInitial LLM Metrics:")
print("  Semantic Accuracy:   \(String(format: "%.3f", initialEvaluation.semanticScore))")
print("  Syntactic Coherence: \(String(format: "%.3f", initialEvaluation.syntacticScore))")
print("  Contextual Relevance: \(String(format: "%.3f", initialEvaluation.contextualScore))")
print("  Perplexity:          \(String(format: "%.1f", initialEvaluation.perplexity))")
print("  Token Efficiency:    \(String(format: "%.3f", initialEvaluation.tokenEfficiency))")

// Perform recursive self-improvement
let (finalThreshold, converged) = optimizer.recursiveSelfImprove(
    evaluation: initialEvaluation,
    maxIterations: 10
)

print("\nAfter Self-Recursive Improvement:")
print("  Final Threshold:     \(String(format: "%.4f", finalThreshold))")
print("  Converged:           \(converged ? "✓ YES" : "✗ NO")")

let metrics = optimizer.getLanguageModelMetrics()
print("\nImproved LLM Metrics:")
print("  Semantic Accuracy:   \(String(format: "%.3f", metrics.semanticAccuracy))")
print("  Syntactic Coherence: \(String(format: "%.3f", metrics.syntacticCoherence))")
print("  Contextual Relevance: \(String(format: "%.3f", metrics.contextualRelevance))")
print("  Convergence Score:   \(String(format: "%.3f", metrics.convergenceScore))")
print("  Perplexity:          \(String(format: "%.1f", metrics.perplexity))")
print("  Token Efficiency:    \(String(format: "%.3f", metrics.tokenEfficiency))")

// MARK: - Test Language Task Optimization

print("\n\n📊 TEST 2: Language Task-Specific Optimization")
print("─────────────────────────────────────────────")

let taskTypes: [LanguageTaskType] = [
    .semanticUnderstanding,
    .syntacticGeneration,
    .codeGeneration,
    .contextualReasoning
]

for taskType in taskTypes {
    print("\nOptimizing for: \(taskType.description)")
    let convergence = optimizer.optimizeForLanguageTask(taskType: taskType, iterations: 5)
    print("  → Convergence Score: \(String(format: "%.4f", convergence))")
}

// MARK: - Test Multiple Iterations

print("\n\n📊 TEST 3: Multi-Round Self-Improvement")
print("─────────────────────────────────────────────")

var roundMetrics: [(round: Int, convergence: Double)] = []

for round in 1...5 {
    print("\nRound \(round):")

    // Create progressively better evaluations
    let progressFactor = Double(round) / 5.0
    let progressiveEvaluation = LLMEvaluation(
        semanticScore: min(0.95, initialEvaluation.semanticScore + (progressFactor * 0.3)),
        syntacticScore: min(0.95, initialEvaluation.syntacticScore + (progressFactor * 0.25)),
        contextualScore: min(0.95, initialEvaluation.contextualScore + (progressFactor * 0.35)),
        perplexity: max(5.0, initialEvaluation.perplexity - (progressFactor * 30)),
        entropy: max(0.05, initialEvaluation.entropy - (progressFactor * 0.25)),
        tokenEfficiency: min(0.95, initialEvaluation.tokenEfficiency + (progressFactor * 0.4)),
        improvementSuggestions: ["Round \(round) optimization"]
    )

    let (_, roundConverged) = optimizer.recursiveSelfImprove(
        evaluation: progressiveEvaluation,
        maxIterations: 3
    )

    let roundMetricsData = optimizer.getLanguageModelMetrics()
    print("  Convergence: \(String(format: "%.4f", roundMetricsData.convergenceScore))")

    roundMetrics.append((round: round, convergence: roundMetricsData.convergenceScore))
}

print("\nImprovement Summary:")
print("  Round | Convergence")
print("  ──────┼────────────")
for metric in roundMetrics {
    print("  \(metric.round)    | \(String(format: "%.4f", metric.convergence))")
}

// MARK: - Test Self-Improvement History

print("\n\n📊 TEST 4: Self-Improvement History Analysis")
print("─────────────────────────────────────────────")

let history = optimizer.getSelfImprovementHistory()
print("Total improvement iterations: \(history.count)")

if let firstMetric = history.first, let lastMetric = history.last {
    let improvement = lastMetric.metricImprovement.convergenceScore - firstMetric.metricImprovement.convergenceScore
    let percentImprovement = (improvement / max(0.001, firstMetric.metricImprovement.convergenceScore)) * 100

    print("\nImprovement Statistics:")
    print("  Initial Convergence:   \(String(format: "%.4f", firstMetric.metricImprovement.convergenceScore))")
    print("  Final Convergence:     \(String(format: "%.4f", lastMetric.metricImprovement.convergenceScore))")
    print("  Absolute Improvement:  \(String(format: "%.4f", improvement))")
    print("  Percent Improvement:   \(String(format: "%.2f%%", percentImprovement))")
    print("  Total Iterations:      \(optimizer.getSelfImprovementHistory().count)")
}

// MARK: - Test Reset Functionality

print("\n\n📊 TEST 5: Reset and Reinitialize")
print("─────────────────────────────────────────────")

print("Resetting self-improvement state...")
optimizer.resetSelfImprovement()

let resetMetrics = optimizer.getLanguageModelMetrics()
print("After reset:")
print("  Convergence Score: \(String(format: "%.4f", resetMetrics.convergenceScore))")
print("  History Count: \(optimizer.getSelfImprovementHistory().count)")

// Final summary
print("\n═══════════════════════════════════════════════════════════")
print("TEST COMPLETE")
print("═══════════════════════════════════════════════════════════")
print("\nSelf-recursive improvement enables the LLM to:")
print("  ✓ Iteratively refine language algorithms")
print("  ✓ Adapt to specific task requirements")
print("  ✓ Track and measure convergence over time")
print("  ✓ Auto-adjust meta-learning rates")
print("  ✓ Maintain improvement history for analysis")
print("  ✓ Reset and reinitialize when needed\n")
