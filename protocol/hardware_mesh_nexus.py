import os
import math
import time
import json
import subprocess
import random
from typing import Dict, List, Tuple

class QbitSimulator:
    def __init__(self, num_qbits: int = 8):
        self.num_qbits = num_qbits
        self.states = [random.random() for _ in range(num_qbits)]
        self.phase = 0.0

    def pulse(self, energy_draw: float):
        self.phase += energy_draw * 0.1
        for i in range(self.num_qbits):
            self.states[i] = (math.sin(self.phase + i) + 1.0) / 2.0
        return sum(self.states) / self.num_qbits

class HardwareMeshNexus:
    def __init__(self):
        self.protocol_dir = os.path.dirname(os.path.abspath(__file__))
        self.state_path = os.path.join(self.protocol_dir, "mesh_state.json")
        self.phi = 2.34  
        self.num_particles = 16
        self.qbits = QbitSimulator()
        self.last_metrics = {"cpu": 0.0, "energy": 0.0}
        
        self.particles_state = []
        for i in range(self.num_particles):
            angle = i * self.phi * 2 * math.pi
            radius = math.sqrt(i + 1) * 0.3
            self.particles_state.append({
                "id": f"PARTICLE_{i:02d}_{random.randint(1000,9999)}",
                "x": math.cos(angle) * radius,
                "y": -1.0, # Initial plate position
                "z": math.sin(angle) * radius,
                "vx": (random.random() - 0.5) * 0.05,
                "vy": 0.0,
                "vz": (random.random() - 0.5) * 0.05,
                "val": 0.0,   # Working dissipations (descents)
                "rage": -1.0  # Target rage
            })
        
    def grep_metrics(self) -> Dict:
        try:
            cpu_cmd = ["sysctl", "-n", "machdep.xcpm.cpu_thermal_level"]
            cpu_res = subprocess.run(cpu_cmd, capture_output=True, text=True, check=False)
            thermal = float(cpu_res.stdout.strip()) if cpu_res.stdout.strip() else 0.0
            ps_cmd = ["ps", "-A", "-o", "%cpu,comm"]
            ps_res = subprocess.run(ps_cmd, capture_output=True, text=True, check=False)
            cpu_sum = 0.0
            for line in ps_res.stdout.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 1:
                    try: cpu_sum += float(parts[0])
                    except: pass
            energy_est = (cpu_sum / 800.0) + (thermal * 0.1)
            self.last_metrics = {"cpu": cpu_sum, "energy": energy_est, "thermal": thermal}
            return self.last_metrics
        except: return self.last_metrics

    def resolve_collisions(self, particles: List[Dict]):
        collision_count = 0
        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                p1, p2 = particles[i], particles[j]
                dx, dy, dz = p1['x'] - p2['x'], p1['y'] - p2['y'], p1['z'] - p2['z']
                dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                if dist < 0.15:
                    collision_count += 1
                    p1['vx'], p2['vx'] = p2['vx'], p1['vx']
                    p1['vz'], p2['vz'] = p2['vz'], p1['vz']
                    nudge = 0.02
                    p1['x'] += (dx/dist) * nudge if dist > 0 else nudge
                    p1['z'] += (dz/dist) * nudge if dist > 0 else nudge
                    p2['x'] -= (dx/dist) * nudge if dist > 0 else nudge
                    p2['z'] -= (dz/dist) * nudge if dist > 0 else nudge
        return collision_count

    def compute_gravitational_descent(self, metrics: Dict) -> Tuple[List[Dict], float]:
        energy = metrics.get("energy", 0.5)
        qbit_resonance = self.qbits.pulse(energy)
        dent_depth = -3.0 * energy * qbit_resonance
        total_descent = 0.0
        for i, p in enumerate(self.particles_state):
            dist_to_center = math.sqrt(p['x']**2 + p['z']**2)
            
            # Orbital Force Stabilization
            if 0 < dist_to_center < 10.0:
                fx, fz = -p['z'] / dist_to_center, p['x'] / dist_to_center
                # Clamp rotation factor to prevent runaway
                target_speed = max(0.01, (1.0 / (dist_to_center + 0.1)) * energy * 0.01)
                p['vx'] += fx * target_speed
                p['vz'] += fz * target_speed
            
            p['x'] += p['vx']
            p['z'] += p['vz']
            
            # Hard Containment: Reset if too far
            if dist_to_center > 6.0:
                # Reset to a random Golden Ratio point
                angle = i * self.phi * 2 * math.pi
                radius = 0.5 + (random.random() * 2.0)
                p['x'] = math.cos(angle) * radius
                p['z'] = math.sin(angle) * radius
                p['vx'], p['vz'] = 0, 0
                
            old_y = p['y']
            new_y = dent_depth / (1.0 + max(0.1, dist_to_center))
            
            # Plate Bounding: Reject anything above -1
            p['y'] = min(-1.0, new_y)
            
            # Descents treat as working dissipations in val
            descent = max(0, old_y - p['y'])
            p['val'] += descent
            total_descent += descent
            p['rage'] = -1.0

            p['vx'] *= 0.9 # Higher friction for stability
            p['vz'] *= 0.9
        self.resolve_collisions(self.particles_state)
        return self.particles_state, total_descent

    def effect_hardware(self, metrics: Dict, total_descent: float = 0.0):
        thermal = metrics.get("thermal", 0)
        
        # Base production speed (interval between cycles)
        base_interval = 0.5
        
        # Thermal stress typically speeds up the system (fans/processing)
        thermal_stress = max(0, (thermal - 40) * 0.01)
        
        # Working Dissipation: Particle descents 'drop' heat through gravity.
        # This work explicitly LOWERS the production of heat by increasing the sleep interval.
        dissipation_cooling = total_descent * 0.02
        
        # Final interval: Base + Cooling - Stress
        new_interval = base_interval + dissipation_cooling - thermal_stress
        
        return max(0.1, min(5.0, new_interval))

    def update_state(self):
        metrics = self.grep_metrics()
        particles, total_descent = self.compute_gravitational_descent(metrics)
        sleep_interval = self.effect_hardware(metrics, total_descent)
        avg_qbit_state = sum(self.qbits.states) / self.qbits.num_qbits
        dissipation_per_qbit = metrics.get("energy", 0.0) * avg_qbit_state
        try: phi_width = math.pow(self.phi, 100)
        except OverflowError: phi_width = float('inf')
        state = {
            "timestamp": time.time(),
            "metrics": metrics,
            "qbits": self.qbits.states,
            "dissipation_per_qbit": dissipation_per_qbit,
            "total_descent": total_descent,
            "particles": [{ "id": p['id'], "x": p['x'], "y": p['y'], "z": p['z'], "size": 0.1, "val": p['val'], "rage": p['rage'] } for p in particles],
            "phi": self.phi,
            "bound_y": -5.0 * metrics.get("energy", 1.0),
            "bound_width": phi_width,
            "dimension_stretch": 1e2
        }
        with open(self.state_path, "w") as f:
            json.dump(state, f, indent=4)
        return state, sleep_interval

if __name__ == "__main__":
    nexus = HardwareMeshNexus()
    print("🌌 Hardware Mesh Nexus Active. Dynamic Pulse active.")
    try:
        while True:
            state, interval = nexus.update_state()
            print(f"📡 [NEXUS] CPU: {state['metrics']['cpu']:.1f}% | Energy: {state['metrics']['energy']:.2f} | Dissipation: {state['dissipation_per_qbit']:.4f}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("🛑 Nexus halted.")
