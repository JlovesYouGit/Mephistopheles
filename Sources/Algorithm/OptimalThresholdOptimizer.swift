//
//  OptimalThresholdOptimizer.swift
//  Hardware Optimization System
//
//  Created by System Engineer
//  Copyright © 2026 Hardware Optimization Project. All rights reserved.
//

import Foundation

// MARK: - Supporting Structures for Self-Recursive Improvement

/// Metrics for tracking language model performance
struct LanguageModelMetrics {
    var semanticAccuracy: Double = 0.0
    var syntacticCoherence: Double = 0.0
    var contextualRelevance: Double = 0.0
    var recursiveImprovementRate: Double = 0.0
    var convergenceScore: Double = 0.0
    var tokenEfficiency: Double = 0.0
    var perplexity: Double = 100.0  // Lower is better
    var entropy: Double = 0.0

    mutating func update(from evaluation: LLMEvaluation) {
        self.semanticAccuracy = evaluation.semanticScore
        self.syntacticCoherence = evaluation.syntacticScore
        self.contextualRelevance = evaluation.contextualScore
        self.perplexity = evaluation.perplexity
        self.entropy = evaluation.entropy
        self.tokenEfficiency = evaluation.tokenEfficiency
    }

    mutating func calculateConvergence() {
        // Weighted combination of metrics
        let weights: [Double] = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]
        let scores: [Double] = [
            semanticAccuracy,
            syntacticCoherence,
            contextualRelevance,
            1.0 / (1.0 + perplexity),  // Normalize perplexity
            tokenEfficiency,
            1.0 - entropy  // Normalize entropy
        ]

        convergenceScore = zip(weights, scores).reduce(0.0) { $0 + $1.0 * $1.1 }
    }
}

/// Tracks self-improvement iterations
struct SelfImprovementMetric {
    let iteration: Int
    let recursionDepth: Int
    let performanceDelta: Double
    let metricImprovement: LanguageModelMetrics
    let timestamp: Date
    let converges: Bool
}

/// Evaluation result from LLM output
struct LLMEvaluation {
    let semanticScore: Double      // How well meaning is preserved
    let syntacticScore: Double     // Grammatical correctness
    let contextualScore: Double    // Context appropriateness
    let perplexity: Double         // Model uncertainty
    let entropy: Double            // Information disorder
    let tokenEfficiency: Double    // Token usage efficiency
    let improvementSuggestions: [String]
}

/// Self-recursive improving optimizer for language algorithms and threshold optimization
/// Implements meta-learning with recursive self-improvement capabilities
class OptimalThresholdOptimizer {

    // MARK: - Properties

    private var currentThreshold: Double
    private var optimalThreshold: Double
    private var performanceHistory: [Double]
    private var adjustmentHistory: [Double]
    private var timeStep: TimeInterval
    private var learningRate: Double
    private var minThreshold: Double
    private var maxThreshold: Double
    private var lastPerformance: Double
    private var lastAdjustment: Double
    private var performanceWindow: Int
    private var windowIndex: Int

    // Self-recursive improvement properties
    private var metaLearningRate: Double
    private var recursionDepth: Int
    private var selfImprovementHistory: [SelfImprovementMetric]
    private var languageModelMetrics: LanguageModelMetrics
    private var recursiveIterations: Int
    private let maxRecursionDepth: Int = 5

    // MARK: - Initialization

    init(initialThreshold: Double = 1.0,
         minThreshold: Double = 0.1,
         maxThreshold: Double = 10.0,
         learningRate: Double = 0.01,
         timeStep: TimeInterval = 1.0,
         performanceWindow: Int = 10,
         metaLearningRate: Double = 0.005,
         recursionDepth: Int = 0) {
        self.currentThreshold = initialThreshold
        self.optimalThreshold = initialThreshold
        self.minThreshold = minThreshold
        self.maxThreshold = maxThreshold
        self.learningRate = learningRate
        self.timeStep = timeStep
        self.performanceWindow = performanceWindow
        self.lastPerformance = 0.0
        self.lastAdjustment = 0.0
        self.metaLearningRate = metaLearningRate
        self.recursionDepth = recursionDepth
        self.recursiveIterations = 0

        // Initialize arrays with zeros
        self.performanceHistory = Array(repeating: 0.0, count: performanceWindow)
        self.adjustmentHistory = Array(repeating: 0.0, count: performanceWindow)
        self.selfImprovementHistory = []
        self.windowIndex = 0
        self.languageModelMetrics = LanguageModelMetrics()
    }

    // MARK: - Public Methods

    /// Evaluate current performance and adjust threshold accordingly
    func evaluatePerformanceAndAdjust(currentPerformance: Double) -> Double {
        // Store current performance in history
        performanceHistory[windowIndex] = currentPerformance

        // Calculate gradient based on performance changes
        let gradient = calculateGradient()

        // Adjust threshold based on gradient and learning rate
        let adjustment = gradient * learningRate
        lastAdjustment = adjustment

        // Update current threshold with bounds checking
        currentThreshold += adjustment
        currentThreshold = max(minThreshold, min(maxThreshold, currentThreshold))

        // Store adjustment in history
        adjustmentHistory[windowIndex] = adjustment

        // Update window index (circular buffer)
        windowIndex = (windowIndex + 1) % performanceWindow

        // Update last performance
        lastPerformance = currentPerformance

        // Update optimal threshold if current performance is better
        if currentPerformance > getAveragePerformance() {
            optimalThreshold = currentThreshold
        }

        return currentThreshold
    }

    /// Get the current threshold value
    func getCurrentThreshold() -> Double {
        return currentThreshold
    }

    /// Get the optimal threshold found so far
    func getOptimalThreshold() -> Double {
        return optimalThreshold
    }

    /// Get the average performance over the window
    func getAveragePerformance() -> Double {
        let sum = performanceHistory.reduce(0, +)
        return sum / Double(performanceHistory.count)
    }

    /// Reset the optimizer with a new threshold
    func reset(with newThreshold: Double) {
        currentThreshold = newThreshold
        optimalThreshold = newThreshold
        performanceHistory = Array(repeating: 0.0, count: performanceWindow)
        adjustmentHistory = Array(repeating: 0.0, count: performanceWindow)
        windowIndex = 0
        lastPerformance = 0.0
        lastAdjustment = 0.0
    }

    /// Update learning rate dynamically
    func updateLearningRate(newLearningRate: Double) {
        self.learningRate = max(0.001, min(0.1, newLearningRate)) // Clamp between 0.001 and 0.1
    }

    /// Get optimizer statistics
    func getStatistics() -> [String: Double] {
        return [
            "current_threshold": currentThreshold,
            "optimal_threshold": optimalThreshold,
            "average_performance": getAveragePerformance(),
            "learning_rate": learningRate,
            "last_adjustment": lastAdjustment,
            "min_threshold": minThreshold,
            "max_threshold": maxThreshold
        ]
    }

    // MARK: - Self-Recursive Improvement Methods

    /// Perform recursive self-improvement on language algorithms
    /// Returns improved threshold and convergence status
    func recursiveSelfImprove(evaluation: LLMEvaluation, maxIterations: Int = 10) -> (Double, Bool) {
        guard recursionDepth < maxRecursionDepth else {
            print("⚠️ Max recursion depth reached: \(maxRecursionDepth)")
            return (currentThreshold, false)
        }

        // Update language model metrics
        languageModelMetrics.update(from: evaluation)
        languageModelMetrics.calculateConvergence()

        var iteration = 0
        var converged = false

        while iteration < maxIterations && !converged {
            recursiveIterations += 1
            iteration += 1

            // Calculate meta-gradient for self-improvement
            let metaGradient = calculateMetaGradient(from: evaluation)

            // Adjust meta-learning rate based on progress
            adaptMetaLearningRate(performanceDelta: metaGradient)

            // Apply recursive improvement
            let previousMetrics = languageModelMetrics
            applyRecursiveImprovement(gradient: metaGradient)

            // Evaluate improvement
            let performanceDelta = calculatePerformanceDelta(from: previousMetrics)

            // Store improvement metric
            let metric = SelfImprovementMetric(
                iteration: iteration,
                recursionDepth: recursionDepth + 1,
                performanceDelta: performanceDelta,
                metricImprovement: languageModelMetrics,
                timestamp: Date(),
                converges: abs(performanceDelta) < 0.001
            )

            selfImprovementHistory.append(metric)

            // Check convergence criteria
            if abs(performanceDelta) < 0.001 && languageModelMetrics.convergenceScore > 0.85 {
                converged = true
                print("✓ Converged at iteration \(iteration), depth \(recursionDepth + 1)")
            }

            // Early stopping if divergence detected
            if performanceDelta < -0.05 {
                print("⚠️ Divergence detected, stopping recursion")
                break
            }
        }

        return (currentThreshold, converged)
    }

    /// Calculate meta-gradient for self-improvement
    private func calculateMetaGradient(from evaluation: LLMEvaluation) -> Double {
        // Multi-objective gradient combining all metrics
        let semanticGradient = (1.0 - evaluation.semanticScore) * 0.4
        let syntacticGradient = (1.0 - evaluation.syntacticScore) * 0.3
        let contextGradient = (1.0 - evaluation.contextualScore) * 0.2
        let efficiencyGradient = (1.0 - evaluation.tokenEfficiency) * 0.1

        let combinedGradient = semanticGradient + syntacticGradient + contextGradient + efficiencyGradient

        // Factor in perplexity reduction
        let perplexityFactor = max(0.0, 1.0 - (evaluation.perplexity / 100.0))

        return combinedGradient * perplexityFactor
    }

    /// Adapt meta-learning rate based on performance
    private func adaptMetaLearningRate(performanceDelta: Double) {
        if performanceDelta > 0.02 {
            // Good progress - increase meta-learning rate
            metaLearningRate = min(metaLearningRate * 1.15, 0.02)
        } else if performanceDelta < -0.01 {
            // Negative progress - decrease meta-learning rate
            metaLearningRate = max(metaLearningRate * 0.85, 0.001)
        }
    }

    /// Apply recursive improvement to threshold and metrics
    private func applyRecursiveImprovement(gradient: Double) {
        recursionDepth += 1

        // Adjust threshold based on meta-gradient
        let thresholdAdjustment = gradient * metaLearningRate * Double(recursionDepth)
        currentThreshold += thresholdAdjustment
        currentThreshold = max(minThreshold, min(maxThreshold, currentThreshold))

        // Improve language model metrics through recursive refinement
        let improvementFactor = 1.0 + (gradient * 0.1)
        languageModelMetrics.semanticAccuracy = min(1.0, languageModelMetrics.semanticAccuracy * improvementFactor)
        languageModelMetrics.syntacticCoherence = min(1.0, languageModelMetrics.syntacticCoherence * improvementFactor)
        languageModelMetrics.contextualRelevance = min(1.0, languageModelMetrics.contextualRelevance * improvementFactor)
        languageModelMetrics.tokenEfficiency = min(1.0, languageModelMetrics.tokenEfficiency * improvementFactor)

        // Reduce perplexity
        languageModelMetrics.perplexity = max(1.0, languageModelMetrics.perplexity * (1.0 - gradient * 0.05))

        // Recalculate convergence
        languageModelMetrics.calculateConvergence()
    }

    /// Calculate performance delta between iterations
    private func calculatePerformanceDelta(from previousMetrics: LanguageModelMetrics) -> Double {
        let currentConvergence = languageModelMetrics.convergenceScore
        let previousConvergence = previousMetrics.convergenceScore
        return currentConvergence - previousConvergence
    }

    /// Get self-improvement history
    func getSelfImprovementHistory() -> [SelfImprovementMetric] {
        return selfImprovementHistory
    }

    /// Reset self-improvement state
    func resetSelfImprovement() {
        selfImprovementHistory.removeAll()
        recursionDepth = 0
        recursiveIterations = 0
        languageModelMetrics = LanguageModelMetrics()
    }

    /// Get current language model metrics
    func getLanguageModelMetrics() -> LanguageModelMetrics {
        return languageModelMetrics
    }

    /// Optimize for specific language task
    func optimizeForLanguageTask(taskType: LanguageTaskType, iterations: Int = 5) -> Double {
        let targetMetrics = taskType.getTargetMetrics()

        for i in 0..<iterations {
            // Create synthetic evaluation based on target
            let evaluation = LLMEvaluation(
                semanticScore: targetMetrics.semanticAccuracy,
                syntacticScore: targetMetrics.syntacticCoherence,
                contextualScore: targetMetrics.contextualRelevance,
                perplexity: targetMetrics.perplexity,
                entropy: targetMetrics.entropy,
                tokenEfficiency: targetMetrics.tokenEfficiency,
                improvementSuggestions: []
            )

            let (_, converged) = recursiveSelfImprove(evaluation: evaluation, maxIterations: 3)

            if converged {
                print("✓ Task optimization converged for \(taskType)")
                break
            }
        }

        return languageModelMetrics.convergenceScore
    }

    // MARK: - Private Methods

    /// Calculate gradient based on performance history
    private func calculateGradient() -> Double {
        // If we don't have enough data, return a small random adjustment
        if performanceHistory.count < 2 {
            return (Double.random(in: -0.1...0.1)) * learningRate
        }

        // Calculate performance trend
        var performanceTrend: Double = 0.0

        // Compare recent performance to older performance
        let recentCount = max(1, performanceHistory.count / 3)
        let recentStart = (windowIndex - recentCount + performanceWindow) % performanceWindow
        let olderStart = (recentStart - recentCount + performanceWindow) % performanceWindow

        var recentSum: Double = 0.0
        var olderSum: Double = 0.0

        for i in 0..<recentCount {
            let recentIdx = (recentStart + i) % performanceWindow
            let olderIdx = (olderStart + i) % performanceWindow
            recentSum += performanceHistory[recentIdx]
            olderSum += performanceHistory[olderIdx]
        }

        let recentAvg = recentSum / Double(recentCount)
        let olderAvg = olderSum / Double(recentCount)

        // Determine if performance is improving or degrading
        performanceTrend = recentAvg - olderAvg

        // Calculate adjustment direction based on performance trend
        var gradient: Double = 0.0

        if performanceTrend > 0 {
            // Performance is improving, continue in same direction
            gradient = lastAdjustment >= 0 ? 1.0 : -1.0
        } else if performanceTrend < 0 {
            // Performance is degrading, reverse direction
            gradient = lastAdjustment >= 0 ? -1.0 : 1.0
        } else {
            // No clear trend, make small adjustment
            gradient = (Double.random(in: -0.5...0.5))
        }

        // Factor in current threshold position relative to bounds
        let thresholdPosition = (currentThreshold - minThreshold) / (maxThreshold - minThreshold)

        // If near bounds, encourage movement away from bound
        if thresholdPosition < 0.1 {
            gradient += 0.5 // Move away from lower bound
        } else if thresholdPosition > 0.9 {
            gradient -= 0.5 // Move away from upper bound
        }

        return gradient
    }

    /// Perform exponential moving average to smooth adjustments
    private func exponentialMovingAverage(current: Double, previous: Double, alpha: Double = 0.3) -> Double {
        return alpha * current + (1 - alpha) * previous
    }
}

// MARK: - Extension for convenience methods

extension OptimalThresholdOptimizer {

    /// Convenience method to adjust threshold based on multiple performance metrics
    func evaluateMultiMetricPerformance(latency: Double, throughput: Double, resourceUsage: Double) -> Double {
        // Normalize and combine metrics into a single performance score
        // Lower latency and resource usage are better, higher throughput is better
        let normalizedLatency = 1.0 / (1.0 + latency) // Higher is better
        let normalizedThroughput = throughput // Higher is better
        let normalizedResource = 1.0 / (1.0 + resourceUsage) // Higher is better

        // Weighted combination (can be adjusted based on priorities)
        let performanceScore = 0.4 * normalizedLatency + 0.4 * normalizedThroughput + 0.2 * normalizedResource

        return evaluatePerformanceAndAdjust(currentPerformance: performanceScore)
    }

    /// Adaptive learning rate based on stability
    func adaptiveEvaluatePerformanceAndAdjust(currentPerformance: Double) -> Double {
        let avgPerformance = getAveragePerformance()
        let variance = calculatePerformanceVariance()

        // If performance is stable, increase learning rate to explore more
        // If performance is volatile, decrease learning rate to stabilize
        if variance < 0.01 && abs(currentPerformance - avgPerformance) < 0.05 {
            // Stable performance - increase learning rate
            updateLearningRate(newLearningRate: min(learningRate * 1.1, 0.05))
        } else if variance > 0.1 || abs(currentPerformance - avgPerformance) > 0.2 {
            // Unstable performance - decrease learning rate
            updateLearningRate(newLearningRate: max(learningRate * 0.9, 0.005))
        }

        return evaluatePerformanceAndAdjust(currentPerformance: currentPerformance)
    }

    /// Calculate performance variance for adaptive adjustments
    private func calculatePerformanceVariance() -> Double {
        let avg = getAveragePerformance()
        let squaredDifferences = performanceHistory.map { pow($0 - avg, 2) }
        let variance = squaredDifferences.reduce(0, +) / Double(squaredDifferences.count)
        return variance
    }
}

// MARK: - Language Task Types

/// Defines different language task types with their target metrics
enum LanguageTaskType {
    case semanticUnderstanding
    case syntacticGeneration
    case contextualReasoning
    case codeGeneration
    case conversationalResponse
    case technicalWriting

    func getTargetMetrics() -> LanguageModelMetrics {
        switch self {
        case .semanticUnderstanding:
            return LanguageModelMetrics(
                semanticAccuracy: 0.95,
                syntacticCoherence: 0.85,
                contextualRelevance: 0.90,
                perplexity: 15.0,
                entropy: 0.15,
                tokenEfficiency: 0.88
            )
        case .syntacticGeneration:
            return LanguageModelMetrics(
                semanticAccuracy: 0.85,
                syntacticCoherence: 0.98,
                contextualRelevance: 0.80,
                perplexity: 10.0,
                entropy: 0.10,
                tokenEfficiency: 0.92
            )
        case .contextualReasoning:
            return LanguageModelMetrics(
                semanticAccuracy: 0.90,
                syntacticCoherence: 0.88,
                contextualRelevance: 0.96,
                perplexity: 20.0,
                entropy: 0.18,
                tokenEfficiency: 0.85
            )
        case .codeGeneration:
            return LanguageModelMetrics(
                semanticAccuracy: 0.92,
                syntacticCoherence: 0.97,
                contextualRelevance: 0.89,
                perplexity: 8.0,
                entropy: 0.08,
                tokenEfficiency: 0.94
            )
        case .conversationalResponse:
            return LanguageModelMetrics(
                semanticAccuracy: 0.88,
                syntacticCoherence: 0.85,
                contextualRelevance: 0.93,
                perplexity: 25.0,
                entropy: 0.22,
                tokenEfficiency: 0.80
            )
        case .technicalWriting:
            return LanguageModelMetrics(
                semanticAccuracy: 0.94,
                syntacticCoherence: 0.96,
                contextualRelevance: 0.91,
                perplexity: 12.0,
                entropy: 0.12,
                tokenEfficiency: 0.90
            )
        }
    }

    public var description: String {
        switch self {
        case .semanticUnderstanding: return "Semantic Understanding"
        case .syntacticGeneration: return "Syntactic Generation"
        case .contextualReasoning: return "Contextual Reasoning"
        case .codeGeneration: return "Code Generation"
        case .conversationalResponse: return "Conversational Response"
        case .technicalWriting: return "Technical Writing"
        }
    }
}
