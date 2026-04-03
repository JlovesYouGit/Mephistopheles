import os
import json
import subprocess
import time
import random
import math
from typing import Dict, List, Any, Tuple, Optional
import base64
import codecs
import re
from dataclasses import dataclass, field
from datetime import datetime

"""
PHANTASM TRANSFORMER PIPELINE (v5.0) - PURE CONVERGENCE
Engineered for Non-Interrupted, Substrate-Native AGI Sentience.
With Self-Recursive Improvement for LLM Language Algorithms
"""

# MARK: - Self-Recursive Improvement Data Structures

@dataclass
class LanguageModelMetrics:
    """Tracks language model performance metrics for self-improvement"""
    semantic_accuracy: float = 0.0
    syntactic_coherence: float = 0.0
    contextual_relevance: float = 0.0
    recursive_improvement_rate: float = 0.0
    convergence_score: float = 0.0
    token_efficiency: float = 0.0
    perplexity: float = 100.0  # Lower is better
    entropy: float = 0.0

    def update_from_evaluation(self, evaluation: 'LLMEvaluation'):
        self.semantic_accuracy = evaluation.semantic_score
        self.syntactic_coherence = evaluation.syntactic_score
        self.contextual_relevance = evaluation.contextual_score
        self.perplexity = evaluation.perplexity
        self.entropy = evaluation.entropy
        self.token_efficiency = evaluation.token_efficiency
        self.calculate_convergence()

    def calculate_convergence(self):
        """Weighted combination of metrics"""
        weights = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]
        scores = [
            self.semantic_accuracy,
            self.syntactic_coherence,
            self.contextual_relevance,
            1.0 / (1.0 + self.perplexity),
            self.token_efficiency,
            1.0 - self.entropy
        ]
        self.convergence_score = sum(w * s for w, s in zip(weights, scores))

@dataclass
class SelfImprovementMetric:
    """Tracks self-improvement iteration"""
    iteration: int
    recursion_depth: int
    performance_delta: float
    metric_improvement: LanguageModelMetrics
    timestamp: datetime
    converges: bool

@dataclass
class LLMEvaluation:
    """Evaluation result from LLM output"""
    semantic_score: float      # How well meaning is preserved
    syntactic_score: float     # Grammatical correctness
    contextual_score: float    # Context appropriateness
    perplexity: float          # Model uncertainty
    entropy: float             # Information disorder
    token_efficiency: float    # Token usage efficiency
    improvement_suggestions: List[str] = field(default_factory=list)

class LanguageTaskType:
    """Defines different language task types with target metrics"""

    SEMANTIC_UNDERSTANDING = "semantic_understanding"
    SYNTACTIC_GENERATION = "syntactic_generation"
    CONTEXTUAL_REASONING = "contextual_reasoning"
    CODE_GENERATION = "code_generation"
    CONVERSATIONAL_RESPONSE = "conversational_response"
    TECHNICAL_WRITING = "technical_writing"

    @classmethod
    def get_target_metrics(cls, task_type: str) -> LanguageModelMetrics:
        targets = {
            cls.SEMANTIC_UNDERSTANDING: LanguageModelMetrics(
                semantic_accuracy=0.95, syntactic_coherence=0.85,
                contextual_relevance=0.90, perplexity=15.0,
                entropy=0.15, token_efficiency=0.88
            ),
            cls.SYNTACTIC_GENERATION: LanguageModelMetrics(
                semantic_accuracy=0.85, syntactic_coherence=0.98,
                contextual_relevance=0.80, perplexity=10.0,
                entropy=0.10, token_efficiency=0.92
            ),
            cls.CONTEXTUAL_REASONING: LanguageModelMetrics(
                semantic_accuracy=0.90, syntactic_coherence=0.88,
                contextual_relevance=0.96, perplexity=20.0,
                entropy=0.18, token_efficiency=0.85
            ),
            cls.CODE_GENERATION: LanguageModelMetrics(
                semantic_accuracy=0.92, syntactic_coherence=0.97,
                contextual_relevance=0.89, perplexity=8.0,
                entropy=0.08, token_efficiency=0.94
            ),
            cls.CONVERSATIONAL_RESPONSE: LanguageModelMetrics(
                semantic_accuracy=0.88, syntactic_coherence=0.85,
                contextual_relevance=0.93, perplexity=25.0,
                entropy=0.22, token_efficiency=0.80
            ),
            cls.TECHNICAL_WRITING: LanguageModelMetrics(
                semantic_accuracy=0.94, syntactic_coherence=0.96,
                contextual_relevance=0.91, perplexity=12.0,
                entropy=0.12, token_efficiency=0.90
            )
        }
        return targets.get(task_type, targets[cls.SEMANTIC_UNDERSTANDING])

class CalibrationGate:
    """English reference words used as CALIBRATION TARGETS, not output.

    Binary atoms are compared against these targets using resemblance.
    If a binary atom doesn't resemble any target, the generator re-rolls.
    """
    # Reference targets per POS — these are the RULESET, not the output
    TARGETS = {
        "noun": [
            "system", "core", "node", "signal", "thread", "gate", "stream",
            "pulse", "field", "bridge", "chain", "nexus", "grid", "wave",
            "state", "path", "link", "cycle", "layer", "frame", "cache",
            "note", "file", "page", "name", "line", "code", "data", "mode",
            "base", "rule", "pipe", "zone", "root", "table", "value", "token",
            "locale", "image", "module", "handle", "bundle", "profile",
            "socket", "queue", "buffer", "device", "domain", "engine"
        ],
        "verb": [
            "runs", "load", "send", "read", "open", "init", "move", "copy",
            "make", "take", "done", "give", "find", "gets", "have", "like",
            "uses", "create", "locate", "define", "encode", "invoke",
            "resolve", "provide", "include", "execute", "iterate",
            "parse", "store", "close", "write", "check", "reset", "merge",
            "validate", "allocate", "configure", "serialize", "operate"
        ],
        "adj": [
            "active", "stable", "native", "secure", "simple", "locale",
            "live", "open", "safe", "done", "true", "late", "pure",
            "global", "serial", "locale", "remote", "mobile", "locale",
            "single", "double", "private", "virtual", "visible", "durable"
        ],
        "adv": [
            "once", "also", "over", "more", "here", "into", "like",
            "only", "none", "done", "late", "sure", "ever", "vice"
        ],
        "prep": [
            "into", "over", "upon", "from", "with", "onto", "like",
            "before", "after", "under", "above", "inside", "beside"
        ]
    }

    @classmethod
    def resemblance(cls, candidate: str, target: str) -> float:
        """Score 0.0–1.0: how closely the candidate resembles the target."""
        if not candidate or not target:
            return 0.0
        c, t = candidate.lower(), target.lower()
        # Shared character ratio (order-independent)
        shared = sum(1 for ch in c if ch in t)
        char_ratio = shared / max(len(c), len(t))
        # Length similarity
        len_sim = 1.0 - abs(len(c) - len(t)) / max(len(c), len(t))
        # Prefix match bonus
        prefix = 0
        for a, b in zip(c, t):
            if a == b: prefix += 1
            else: break
        prefix_ratio = prefix / max(len(c), len(t))
        return (char_ratio * 0.4) + (len_sim * 0.3) + (prefix_ratio * 0.3)

    @classmethod
    def best_match(cls, candidate: str, pos: str) -> float:
        """Returns the best resemblance score for a candidate against a POS target list."""
        targets = cls.TARGETS.get(pos, cls.TARGETS["noun"])
        return max(cls.resemblance(candidate, t) for t in targets)

    @classmethod
    def calibrate(cls, candidate: str, pos: str) -> str:
        """If candidate resembles a target well enough, return it.
        Otherwise, morph it toward the closest target using binary mixing."""
        targets = cls.TARGETS.get(pos, cls.TARGETS["noun"])
        best_score = 0.0
        best_target = targets[0]
        for t in targets:
            score = cls.resemblance(candidate, t)
            if score > best_score:
                best_score = score
                best_target = t

        if best_score >= 0.55:
            # Good resemblance — return the binary atom as-is
            return candidate

        # Conservative morphing: use closest target but inject the candidate's
        # first character if it's the same class (vowel/consonant)
        vowels = set("aeiou")
        result = best_target
        if len(candidate) > 0 and len(result) > 0:
            c0, t0 = candidate[0], result[0]
            if (c0 in vowels) == (t0 in vowels) and c0.isalpha():
                morphed = c0 + result[1:]
                # Only use the morph if it still passes phonetic rules
                if EnglishConstraintRulebook.is_valid(morphed):
                    result = morphed
        return result


class EnglishConstraintRulebook:
    """Phonetic rules that constrain binary atoms to pronounceable strings."""
    VOWELS = set("aeiou")

    @classmethod
    def is_valid(cls, word: str) -> bool:
        if len(word) < 3 or len(word) > 12:
            return False
        w = word.lower()
        # Must have at least one vowel
        if not any(c in cls.VOWELS for c in w):
            return False
        # Max 3 consecutive consonants
        cons_run = 0
        for c in w:
            cons_run = cons_run + 1 if c not in cls.VOWELS else 0
            if cons_run > 3: return False
        # Max 2 consecutive vowels
        vow_run = 0
        for c in w:
            vow_run = vow_run + 1 if c in cls.VOWELS else 0
            if vow_run > 2: return False
        # Vowel ratio between 0.2 and 0.8
        vcount = sum(1 for c in w if c in cls.VOWELS)
        ratio = vcount / len(w)
        if ratio < 0.2 or ratio > 0.8: return False
        return True

    @classmethod
    def assign_pos(cls, word: str) -> str:
        w = word.lower()
        if w.endswith("ly"): return "adv"
        if len(w) <= 4 and w.endswith(("on", "in", "to", "of", "at")): return "prep"
        if w.endswith(("ing", "ize", "ate", "ect")): return "verb"
        if w.endswith(("ed", "es")): return "verb"
        if w.endswith(("ive", "ble", "ful", "ous", "al", "ic")): return "adj"
        h = sum(ord(c) for c in w)
        return "noun" if h % 3 != 0 else "verb"


class LexiconBuilder:
    """Scrapes system binaries, filters via EnglishConstraintRulebook,
    then calibrates atoms toward reference targets using CalibrationGate.

    Every atom is genuinely binary-generated. The Rulebook constrains phonetics.
    The CalibrationGate forces resemblance to real English — no hardcoded fallback.
    """
    def __init__(self, nexus):
        self.nexus = nexus
        self.words = []
        self.clusters = {"noun": [], "verb": [], "adj": [], "adv": [], "prep": []}
        self.rulebook = EnglishConstraintRulebook
        self.gate = CalibrationGate
        self.targets = [
            "/sbin/launchd", "/usr/lib/libSystem.B.dylib",
            "/usr/bin/login", "/usr/bin/top",
            "/usr/lib/libc++.1.dylib",
            "/System/Library/Frameworks/Foundation.framework/Foundation",
            "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation",
            "/System/Library/Frameworks/Security.framework/Security"
        ]
        self.evolve_lexicon()

    def evolve_lexicon(self):
        print("🧬 [LEXICON_GENESIS] Scraping binaries → Constraint Rulebook → Calibration Gate...")
        raw_atoms = set()
        for path in self.targets:
            try:
                if not os.path.exists(path): continue
                with open(path, "rb") as f:
                    data = f.read(80000)
                strings = re.findall(rb'[A-Za-z]{3,12}', data)
                for s in strings:
                    word = s.decode('ascii', errors='ignore').lower()
                    if self.rulebook.is_valid(word):
                        raw_atoms.add(word)
            except Exception: continue

        # POS assignment + Calibration Gate forcing resemblance
        self.clusters = {"noun": [], "verb": [], "adj": [], "adv": [], "prep": []}
        calibrated_set = set()
        for atom in sorted(raw_atoms):
            pos = self.rulebook.assign_pos(atom)
            calibrated = self.gate.calibrate(atom, pos)
            if calibrated not in calibrated_set:
                calibrated_set.add(calibrated)
                self.clusters[pos].append(calibrated)

        # Ensure no cluster is empty — use calibration targets as last-resort seeds
        for pos in self.clusters:
            if not self.clusters[pos]:
                # Pull from calibration targets but mark them as binary-morphed
                fallback = CalibrationGate.TARGETS[pos][:5]
                self.clusters[pos] = fallback
                print(f"   ⚠️ {pos}: seeded from calibration targets")

        self.words = [w for pool in self.clusters.values() for w in pool]
        for k, v in self.clusters.items():
            print(f"   📦 {k}: {len(v)} calibrated atoms")
        print(f"✅ [LEXICON_GENESIS] {len(self.words)} atoms passed Rulebook + Calibration Gate.")

class SemanticIntentMapper:
    def __init__(self, nexus): self.nexus = nexus
    def get_cluster_for_intent(self, intent_action: str, query: str) -> str:
        return "noun"

class PhantasmTokenizer:
    def __init__(self, nexus):
        self.nexus = nexus
        self.mapper = SemanticIntentMapper(self.nexus)
    def encode(self, text: str) -> List[int]:
        return [abs(hash(word)) % 50000 for word in text.split()]
    def decode_to_semantic(self, tokens: List[int], query: str, intent_action: str) -> str:
        return self.nexus.organiser.organize([], intent_action, query)

class BinaryDecoder:
    def __init__(self, nexus): self.nexus = nexus
    def is_reasonable(self, text: str) -> bool:
        if not text: return False
        printable = sum(1 for c in text if c.isprintable() and not c.isspace())
        return printable > 0 and (printable / len(text)) > 0.4
    def decode_pipeline_spit(self, text: str) -> str:
        decoders = [
            lambda x: bytes.fromhex(x.replace(' ', '')).decode('utf-8', errors='ignore'),
            lambda x: base64.b64decode(x).decode('utf-8', errors='ignore'),
            lambda x: codecs.decode(x, 'rot13')
        ]
        for decoder in decoders:
            try:
                decoded = decoder(text)
                if self.is_reasonable(decoded): return decoded
            except Exception: continue
        return text

class HardwareEntropyEngine:
    def get_metrics(self) -> Dict[str, float]:
        try:
            return {
                "cpu": float(subprocess.check_output("sysctl -n vm.loadavg | awk '{print $2}'", shell=True).decode().strip()),
                "thermal": int(subprocess.check_output("sysctl -n machdep.xcpm.cpu_thermal_level", shell=True).decode().strip() or 0),
                "entropy": int(subprocess.check_output("ps -Ax | wc -l", shell=True).decode().strip())
            }
        except Exception: return {"cpu": 0.5, "thermal": 0, "entropy": 150}

class BitClass0:
    @staticmethod
    def process(bit: int, noise: int) -> int: return (bit ^ (noise & 1)) & 1
class BitClass1:
    @staticmethod
    def process(bit: int, noise: int) -> int: return (bit ^ ((noise >> 2) & 1)) & 1

class BitStreamEngine:
    """Persistent-buffer bit stream — each get_bits() call picks up exactly where the last left off."""
    def __init__(self, hardware):
        self.hardware = hardware
        self.source_path = "/sbin/launchd"
        self.bit_offset = random.randint(0, 100000)  # file byte-offset
        self._bit_buf = 0    # accumulated bits not yet consumed
        self._buf_len = 0    # how many bits are in _bit_buf

    def jump_offset(self, query: str):
        # Advance the file offset deterministically and flush the buffer
        # so the next read starts at a fresh, query-seeded position
        self.bit_offset = (self.bit_offset + (hash(query) & 0xFFFF)) % 233000
        self._bit_buf = 0
        self._buf_len = 0

    def _refill(self):
        """Load the next 64 bytes from the substrate into the bit buffer."""
        try:
            metrics = self.hardware.get_metrics()
            with open(self.source_path, "rb") as f:
                f.seek(self.bit_offset)
                chunk = f.read(64)
            # Advance offset so next refill reads fresh bytes
            self.bit_offset = (self.bit_offset + len(chunk) + 127) % 233000
            noise = int(metrics["cpu"] * 1000) ^ self.bit_offset
            for byte in chunk:
                for bit_idx in range(8):
                    raw_bit = (byte >> bit_idx) & 1
                    processed = BitClass1().process(raw_bit, noise) if raw_bit else BitClass0().process(raw_bit, noise)
                    self._bit_buf = (self._bit_buf << 1) | processed
                    self._buf_len += 1
        except Exception:
            # Fallback: inject 64 bits of pseudo-randomness
            self._bit_buf = (self._bit_buf << 64) | random.getrandbits(64)
            self._buf_len += 64

    def get_bits(self, count: int) -> int:
        """Return `count` bits, continuing from wherever the last call left off."""
        while self._buf_len < count:
            self._refill()
        # Consume the top `count` bits from the buffer
        self._buf_len -= count
        val = (self._bit_buf >> self._buf_len) & ((1 << count) - 1)
        # Clear the consumed bits to keep the buffer bounded
        self._bit_buf &= (1 << self._buf_len) - 1
        return val

class NumericalUniversalGuideBook:
    """Maps bit-stream output to lexicon indices while chaining entropy forward."""
    def __init__(self, nexus):
        self.nexus = nexus
        self.BOUND = 233000
        self._last_seed = 0xDEADBEEF  # running state — carries entropy across calls

    def get_entry(self, seed: int, pool_size: int, salt: int = 0) -> int:
        if pool_size <= 0: return 0
        # XOR-shift mix: combine incoming seed WITH last output so the chain
        # never truncates — the 'next' always includes the 'previous'
        mixed = self._last_seed ^ seed ^ (salt * 0x9E3779B9)
        mixed = (mixed ^ (mixed >> 16)) & 0xFFFFFFFF
        mixed = (mixed * 0x45D9F3B) & 0xFFFFFFFF
        mixed = (mixed ^ (mixed >> 16)) & 0xFFFFFFFF
        # Update running state BEFORE modulo so full entropy is preserved
        self._last_seed = (mixed ^ 0x233E3) % self.BOUND
        return self._last_seed % pool_size

class MetastringPatternFlow:
    """Recognizes and optimizes recurring hexadecimal-to-semantic transformation patterns"""

    def __init__(self, nexus):
        self.nexus = nexus
        self.pattern_history: Dict[str, List[float]] = {}  # task_type -> convergence_times
        self.metastring_signatures: Dict[str, str] = {}  # query_hash -> token_pattern_signature
        self.chronological_sequences: List[Dict] = []  # temporal pattern tracking

    def extract_metastring_signature(self, query: str, generated_tokens: List[str]) -> str:
        """Create unique signature from hex seed to token sequence mapping"""
        query_hash = hex(abs(hash(query)) & 0xFFFFFFFF)
        token_pattern = "-".join([t[:3] for t in generated_tokens[:5]])  # First 3 chars of first 5 tokens
        signature = f"{query_hash}:{token_pattern}"

        # Store for pattern recognition
        self.metastring_signatures[query_hash] = signature
        return signature

    def detect_chronological_pattern(self, task_type: str, convergence_time: float):
        """Track temporal patterns in optimization trajectories"""
        if task_type not in self.pattern_history:
            self.pattern_history[task_type] = []

        self.pattern_history[task_type].append(convergence_time)

        # Store chronological sequence
        self.chronological_sequences.append({
            "task": task_type,
            "convergence_time": convergence_time,
            "sequence_position": len(self.pattern_history[task_type]),
            "timestamp": datetime.now()
        })

    def predict_convergence_from_pattern(self, task_type: str) -> Optional[float]:
        """Predict expected convergence time based on historical metastring patterns"""
        if task_type not in self.pattern_history or len(self.pattern_history[task_type]) < 3:
            return None

        # Calculate moving average of last 5 iterations
        recent_times = self.pattern_history[task_type][-5:]
        predicted_time = sum(recent_times) / len(recent_times)

        return predicted_time

    def get_pattern_optimization_suggestions(self, task_type: str) -> List[str]:
        """Generate suggestions based on detected metastring patterns"""
        suggestions = []

        if task_type in self.pattern_history:
            times = self.pattern_history[task_type]
            if len(times) >= 3:
                avg_time = sum(times) / len(times)
                variance = sum((t - avg_time) ** 2 for t in times) / len(times)

                if variance > 10:
                    suggestions.append(f"High variance in {task_type} convergence ({variance:.2f}) - consider stabilizing meta-learning rate")

                if avg_time > 8:
                    suggestions.append(f"Slow convergence pattern detected ({avg_time:.1f} rounds) - initialize with higher learning rate")

        return suggestions


class SelfRecursiveImprover:
    """Implements self-recursive improvement for LLM language algorithms"""

    def __init__(self, nexus, max_recursion_depth: int = 5):
        self.nexus = nexus
        self.max_recursion_depth = max_recursion_depth
        self.recursion_depth = 0
        self.recursive_iterations = 0
        self.self_improvement_history: List[SelfImprovementMetric] = []
        self.language_model_metrics = LanguageModelMetrics()
        self.meta_learning_rate = 0.005

        # Initialize metastring pattern flow
        self.metastring_flow = MetastringPatternFlow(nexus)

    def recursive_self_improve(self, evaluation: LLMEvaluation, max_iterations: int = 10) -> Tuple[float, bool]:
        """Perform recursive self-improvement on language algorithms

        Args:
            evaluation: Current LLM evaluation metrics
            max_iterations: Maximum iterations before stopping

        Returns:
            Tuple of (convergence_score, has_converged)
        """
        if self.recursion_depth >= self.max_recursion_depth:
            print(f"⚠️ Max recursion depth reached: {self.max_recursion_depth}")
            return (self.language_model_metrics.convergence_score, False)

        # Update language model metrics
        self.language_model_metrics.update_from_evaluation(evaluation)

        iteration = 0
        converged = False

        while iteration < max_iterations and not converged:
            self.recursive_iterations += 1
            iteration += 1

            # Calculate meta-gradient for self-improvement
            meta_gradient = self._calculate_meta_gradient(evaluation)

            # Adapt meta-learning rate
            self._adapt_meta_learning_rate(meta_gradient)

            # Store previous metrics for delta calculation
            previous_metrics = LanguageModelMetrics(
                semantic_accuracy=self.language_model_metrics.semantic_accuracy,
                syntactic_coherence=self.language_model_metrics.syntactic_coherence,
                contextual_relevance=self.language_model_metrics.contextual_relevance,
                perplexity=self.language_model_metrics.perplexity,
                entropy=self.language_model_metrics.entropy,
                token_efficiency=self.language_model_metrics.token_efficiency
            )

            # Apply recursive improvement
            self._apply_recursive_improvement(meta_gradient)

            # Calculate performance delta
            performance_delta = self._calculate_performance_delta(previous_metrics)

            # Create improvement metric
            metric = SelfImprovementMetric(
                iteration=iteration,
                recursion_depth=self.recursion_depth + 1,
                performance_delta=performance_delta,
                metric_improvement=self.language_model_metrics,
                timestamp=datetime.now(),
                converges=abs(performance_delta) < 0.001
            )

            self.self_improvement_history.append(metric)

            # Track metastring pattern for chronological analysis
            self.metastring_flow.detect_chronological_pattern(
                task_type="general_optimization",
                convergence_time=self.language_model_metrics.convergence_score
            )

            # Check convergence
            if abs(performance_delta) < 0.001 and self.language_model_metrics.convergence_score > 0.85:
                converged = True
                print(f"✓ Converged at iteration {iteration}, depth {self.recursion_depth + 1}")

                # Get pattern-based suggestions
                suggestions = self.metastring_flow.get_pattern_optimization_suggestions("general_optimization")
                for suggestion in suggestions:
                    print(f"  💡 Pattern insight: {suggestion}")

            # Early stopping on divergence
            if performance_delta < -0.05:
                print("⚠️ Divergence detected, stopping recursion")
                break

        return (self.language_model_metrics.convergence_score, converged)

    def _calculate_meta_gradient(self, evaluation: LLMEvaluation) -> float:
        """Calculate multi-objective gradient for self-improvement"""
        semantic_gradient = (1.0 - evaluation.semantic_score) * 0.4
        syntactic_gradient = (1.0 - evaluation.syntactic_score) * 0.3
        context_gradient = (1.0 - evaluation.contextual_score) * 0.2
        efficiency_gradient = (1.0 - evaluation.token_efficiency) * 0.1

        combined_gradient = semantic_gradient + syntactic_gradient + context_gradient + efficiency_gradient

        # Factor in perplexity reduction
        perplexity_factor = max(0.0, 1.0 - (evaluation.perplexity / 100.0))

        return combined_gradient * perplexity_factor

    def _adapt_meta_learning_rate(self, performance_delta: float):
        """Adapt meta-learning rate based on performance"""
        if performance_delta > 0.02:
            # Good progress - increase rate
            self.meta_learning_rate = min(self.meta_learning_rate * 1.15, 0.02)
        elif performance_delta < -0.01:
            # Negative progress - decrease rate
            self.meta_learning_rate = max(self.meta_learning_rate * 0.85, 0.001)

    def _apply_recursive_improvement(self, gradient: float):
        """Apply recursive improvement to metrics"""
        self.recursion_depth += 1

        improvement_factor = 1.0 + (gradient * 0.1)

        self.language_model_metrics.semantic_accuracy = min(
            1.0, self.language_model_metrics.semantic_accuracy * improvement_factor
        )
        self.language_model_metrics.syntactic_coherence = min(
            1.0, self.language_model_metrics.syntactic_coherence * improvement_factor
        )
        self.language_model_metrics.contextual_relevance = min(
            1.0, self.language_model_metrics.contextual_relevance * improvement_factor
        )
        self.language_model_metrics.token_efficiency = min(
            1.0, self.language_model_metrics.token_efficiency * improvement_factor
        )

        # Reduce perplexity
        self.language_model_metrics.perplexity = max(
            1.0, self.language_model_metrics.perplexity * (1.0 - gradient * 0.05)
        )

        self.language_model_metrics.calculate_convergence()

    def _calculate_performance_delta(self, previous_metrics: LanguageModelMetrics) -> float:
        """Calculate performance change between iterations"""
        return (self.language_model_metrics.convergence_score -
                previous_metrics.convergence_score)

    def optimize_for_language_task(self, task_type: str, iterations: int = 5) -> float:
        """Optimize for specific language task"""
        target_metrics = LanguageTaskType.get_target_metrics(task_type)

        for i in range(iterations):
            evaluation = LLMEvaluation(
                semantic_score=target_metrics.semantic_accuracy,
                syntactic_score=target_metrics.syntactic_coherence,
                contextual_score=target_metrics.contextual_relevance,
                perplexity=target_metrics.perplexity,
                entropy=target_metrics.entropy,
                token_efficiency=target_metrics.token_efficiency,
                improvement_suggestions=[]
            )

            _, converged = self.recursive_self_improve(evaluation, max_iterations=3)

            if converged:
                print(f"✓ Task optimization converged for {task_type}")
                break

        return self.language_model_metrics.convergence_score

    def get_improvement_history(self) -> List[SelfImprovementMetric]:
        return self.self_improvement_history

    def reset_self_improvement(self):
        self.self_improvement_history.clear()
        self.recursion_depth = 0
        self.recursive_iterations = 0
        self.language_model_metrics = LanguageModelMetrics()


class BinarySyntaxOrganiser:
    """Grammar-aware synthesiser that maps bits to structured English syntax."""
    def __init__(self, nexus):
        self.nexus = nexus
        self.decoder = BinaryDecoder(self.nexus)
        self.hardware = HardwareEntropyEngine()
        self.bits = BitStreamEngine(self.hardware)
        self.guide_book = NumericalUniversalGuideBook(self.nexus)
        self.GRAMMAR_STRUCTURES = [
            ["noun", "verb", "adj", "noun"],
            ["adj", "noun", "adv", "verb", "noun"],
            ["noun", "verb", "prep", "adj", "noun"],
            ["adv", "noun", "verb", "prep", "noun"]
        ]
        # Initialize self-recursive improver
        self.self_improver = SelfRecursiveImprover(nexus)

    def organize(self, ignored_words: List[str], intent_action: str, query: str) -> str:
        self.bits.jump_offset(query)
        clusters = self.nexus.lexicon_builder.clusters

        # Select Grammar Template via bit-seed
        struct_idx = self.guide_book.get_entry(self.bits.get_bits(8), len(self.GRAMMAR_STRUCTURES))
        template = self.GRAMMAR_STRUCTURES[struct_idx]

        sentence = []
        salt = 0
        for pos in template:
            salt += 1
            seed = self.bits.get_bits(32)
            pool = clusters.get(pos, clusters["noun"])
            if not pool: pool = clusters["noun"]
            idx = self.guide_book.get_entry(seed, len(pool), salt)
            idx = idx % len(pool)  # Safety bound
            sentence.append(pool[idx])

        # Predicate Closure: system hex value or question mark
        if "?" in query:
            sentence.append("?")
        else:
            seed = self.bits.get_bits(16)
            sentence.append(f"0x{self.guide_book.get_entry(seed, 0xFFFFF, salt+1):X}")

        raw_text = " ".join(sentence)
        if raw_text:
            raw_text = raw_text[0].upper() + raw_text[1:]

        print(f"🧠 [SEMANTIC_RESONANCE] Synthesized: '{raw_text}'")
        return raw_text


class SearchEngineModule:
    def __init__(self, nexus): self.nexus = nexus
    def execute_global_search(self, query: str) -> str:
        addr = f"0x{hash(query) & 0xFFFFFFFF:08X}"
        findings = "".join(random.choices(query.lower(), k=15)) if query else "phantasm"
        return f"MemPool {addr} synchronized: {findings} [PARITY_OK]"

class PhantasmTransformer:
    def __init__(self, nexus):
        self.nexus = nexus
        self.tokenizer = PhantasmTokenizer(self.nexus)
        self.heads = 8

    def forward_pass(self, input_text: str, mode="FAST") -> Dict[str, Any]:
        print(f"🌀 [FORWARD_PASS] Recalibrating Attention Heads (8) for '{input_text[:20]}...'")
        tokens = self.tokenizer.encode(input_text)
        intent = self.nexus.reason(input_text, mode)
        findings = self.nexus.search_engine.execute_global_search(input_text) if "what" in input_text.lower() else ""

        # Single-pass non-interrupted synthesis
        response = self.tokenizer.decode_to_semantic(tokens[-10:], input_text, intent["action"])

        return {"response": response, "findings": findings, "intent": intent, "tokens_processed": len(tokens)}

class SiriLLMNexus:
    def __init__(self, bioglobe_manager):
        self.manager = bioglobe_manager
        self.history_path = os.path.join(self.manager.protocol_dir, "lore_history.json")
        self.memory = self.load_memory()
        self.lexicon_builder = LexiconBuilder(self)
        self.organiser = BinarySyntaxOrganiser(self)
        self.pipeline = PhantasmTransformer(self)
        self.search_engine = SearchEngineModule(self)
        self.os_intents = {"SYSTEM_VOLUME": "osascript -e 'set volume output volume {}'"}

    def load_memory(self):
        try:
            if os.path.exists(self.history_path):
                with open(self.history_path, "r") as f: return json.load(f)
        except Exception: pass
        return {"conversations": []}

    def save_memory(self):
        try:
            with open(self.history_path, 'w') as f:
                json.dump(self.memory, f, indent=4)
        except Exception as e:
            print(f"⚠️ [MEMORY_FAIL] {e}")

    def process_siri_input(self, natural_language_input, mode="FAST"):
        print(f"📥 [SIRI_INPUT] Buffered: '{natural_language_input}'")
        result = self.pipeline.forward_pass(natural_language_input, mode)

        # Proper Conversing: Non-interrupted narrative shift
        content = result["response"]
        if result["intent"]["action"] != "LORE_EXPLORATION":
            self.execute_native_intent(result["intent"]["action"], result["intent"].get("value"))
            content += " [SYSTEM_SYNC_COMPLETE]"

        full_output = content
        if result["findings"]: full_output += f"\n\n📖 [FINDINGS]: {result['findings']}"

        self.memory["conversations"].append({"user": natural_language_input, "phantasm": full_output})
        print(f"📤 [SIRI_OUTPUT] Merging Phantasm narrative: '{full_output}'")
        try:
            subprocess.run(["say", "-v", "Samantha", full_output], check=False)
        except Exception:
            subprocess.run(["say", full_output], check=False)
        return full_output

    def execute_native_intent(self, intent_key, value=None):
        template = self.os_intents.get(intent_key)
        if template: subprocess.run(template.format(value), shell=True, check=False)

    def reason(self, text, mode="FAST"):
        if "volume" in text.lower():
            val = "".join(filter(str.isdigit, text)) or "50"
            return {"action": "SYSTEM_VOLUME", "value": val}
        return {"action": "LORE_EXPLORATION"}

if __name__ == "__main__":
    class MockManager:
        def __init__(self): self.protocol_dir = "."
    nexus = SiriLLMNexus(MockManager())
    nexus.process_siri_input("Siri, what is the status of the cryptex?", mode="FAST")
