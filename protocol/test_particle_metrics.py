import sys
import os
import math
import time

# Add the protocol directory to sys.path
protocol_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(protocol_dir)

from hardware_mesh_nexus import HardwareMeshNexus

def test_particle_metrics():
    print("🧪 Testing Particle Metrics...")
    nexus = HardwareMeshNexus()
    
    # 1. Initial State Check
    for p in nexus.particles_state:
        assert p['val'] == 0.0, f"Initial val should be 0.0, got {p['val']}"
        assert p['rage'] == -1.0, f"Initial rage should be -1.0, got {p['rage']}"
        assert p['y'] == -1.0, f"Initial y should be -1.0, got {p['y']}"
    print("✅ Initial state verified.")

    # 2. Update State and Check Bounding
    metrics = {"energy": 1.0, "thermal": 40.0} # Force some energy
    for _ in range(10):
        nexus.compute_gravitational_descent(metrics)
        for p in nexus.particles_state:
            assert p['y'] <= -1.0, f"Particle y should be <= -1.0, got {p['y']}"
            assert p['rage'] == -1.0, f"Rage should remain -1.0, got {p['rage']}"
    print("✅ Plate bounding (y <= -1.0) and rage verified.")

    # 4. Verify Feedback Loop Influence
    print("🧪 Testing Feedback Loop Influence...")
    # Low energy -> low descent -> small dissipation
    metrics_low = {"energy": 0.5, "thermal": 40}
    nexus.compute_gravitational_descent(metrics_low)
    interval_low = nexus.effect_hardware(metrics_low, 0.0)
    
    # High energy -> high descent -> high dissipation
    metrics_high = {"energy": 5.0, "thermal": 40}
    _, total_descent = nexus.compute_gravitational_descent(metrics_high)
    interval_high = nexus.effect_hardware(metrics_high, total_descent)
    
    print(f"  Interval Low (no descent): {interval_low:.4f}")
    print(f"  Interval High (with descent {total_descent:.4f}): {interval_high:.4f}")
    
    # More dissipation should INCREASE the interval (lowering production)
    assert interval_high >= interval_low, f"Interval should increase with higher dissipation, got {interval_high} vs {interval_low}"
    print("✅ Feedback loop (lowering production) verified.")
    print("✨ All tests passed!")

if __name__ == "__main__":
    test_particle_metrics()
