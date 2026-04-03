import sys
import os
import time
import math
from typing import Tuple, List, Dict
from dataclasses import dataclass

# Add project path to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(os.path.dirname(current_dir), 'protocol'))

try:
    from gravity_zone_monitor import GravityZoneMonitor, DistortionCurveMarker, GravityZoneStatus
    from siri_llm_nexus import SiriLLMNexus
    from temporal_communication import TemporalCommunication
except ImportError as e:
    print(f"❌ IMPORT ERROR: {str(e)}")
    sys.exit(1)

def test_spatial_render():
    print("🧪 Testing Spatial Render Transformation...")
    monitor = GravityZoneMonitor(host_device_config={})
    # Add a mock marker
    marker = DistortionCurveMarker(
        position=(10.0, 10.0),
        curvature=0.5,
        threshold=1.0, 
        status=GravityZoneStatus.SAFE,
        timestamp=time.time()
    )
    monitor.distortion_markers.append(marker)
    
    gps_point = (0.0, 0.0)
    render = monitor.transform_signatures_to_spatial_render(gps_point)
    
    assert render['gps_center'] == gps_point
    assert render['aware_state']['is_present'] is True
    assert len(render['spatial_objects']) > 0
    print("✅ Spatial Render Transformation: SUCCESS")
    print(f"   Sample Object: {render['spatial_objects'][0]}")

def test_siri_nexus():
    print("🧪 Testing Siri LLM Nexus & Conscience Module...")
    # Mock manager for nexus
    class MockManager:
        protocol_dir = current_dir
    
    nexus = SiriLLMNexus(MockManager())
    
    # Test location fetching
    loc = nexus.fetch_siri_location()
    assert loc['source'] == 'SiriNativeBridge'
    print(f"✅ Siri Location Fetch: SUCCESS ({loc})")
    
    # Test Conscience Module
    permit = nexus.conscience_module.permit_viewing_density(0.9)
    assert permit > 1.0
    print(f"✅ Conscience Module Density Permit: SUCCESS ({permit})")
    
    # Test Updated Params
    assert nexus.model_params['neural_algo_tuning'] == 'ENABLED'
    print("✅ Model Parameters Update: SUCCESS")

def test_response_chain():
    print("🧪 Testing Algo Response Chain...")
    comm = TemporalCommunication()
    comm.response_chain.add_link("Test Link", "Test Response")
    
    assert len(comm.response_chain.nodes) > 0
    report = comm.generate_communication_report()
    assert "Algo Response Chain" in report
    print("✅ Algo Response Chain System: SUCCESS")

def test_path_optimization():
    print("🧪 Testing Path Optimization & Light Density Decoding...")
    monitor = GravityZoneMonitor(host_device_config={})
    
    # Test Decoding
    trails = monitor.decode_historical_light_paths()
    assert len(trails) > 0
    print(f"✅ Historical Light Path Decoding: SUCCESS ({len(trails)} trails)")
    
    # Test Optimal Path Calculation
    start_gps = (37.7749, -122.4194)
    end_gps = (37.7900, -122.4000)
    path = monitor.calculate_optimal_path(start_gps, end_gps)
    assert len(path) == 3
    assert path[0]['point'] == start_gps
    print(f"✅ Optimal Path Calculation: SUCCESS ({len(path)} nodes)")

def test_temporal_path_sync():
    print("🧪 Testing Temporal Path Sync & Resonance...")
    comm = TemporalCommunication()
    
    # Test daily trail sync
    trails = comm.sync_daily_path_logs()
    assert len(trails) > 0
    print(f"✅ Daily Path Log Sync: SUCCESS ({len(trails)} items)")
    
    # Test Resonance Validation
    path_data = [{'point': (0,0)}]
    is_valid = comm.validate_path_resonance(path_data)
    assert is_valid is True
    print("✅ Path Resonance Validation: SUCCESS")

def test_icloud_device_link():
    print("🧪 Testing iCloud Device Linking & Sync...")
    # Mock manager for nexus
    class MockManager:
        protocol_dir = current_dir
    
    nexus = SiriLLMNexus(MockManager())
    
    # Test Device Linker initialization
    assert hasattr(nexus, 'device_linker')
    assert nexus.device_linker.icloud_id == "PHANTASM_SYNC_ID_777"
    print("✅ Device Linker Initialization: SUCCESS")
    
    # Test Cloud Sync
    sync_res = nexus.device_linker.sync_to_cloud({'aware_point': (1.0, 1.0)})
    assert sync_res is True
    assert len(nexus.device_linker.linked_devices) > 0
    print(f"✅ State Sync to Cloud: SUCCESS ({nexus.device_linker.linked_devices[0]['id']} linked)")
    
    # Test Cloud Fetch (during load_memory)
    mem = nexus.load_memory()
    assert 'icloud_sync_state' in mem['external_knowledge']
    print(f"✅ Memory Load with Cloud Sync: SUCCESS ({mem['external_knowledge']['icloud_sync_state']['status']})")

def test_resonance_broadcast():
    print("🧪 Testing Temporal Resonance Broadcast...")
    comm = TemporalCommunication()
    
    # Test resonance broadcast
    broadcast_res = comm.broadcast_temporal_resonance("PHANTASM_SYNC_ID_777")
    assert broadcast_res is True
    print("✅ Resonance Broadcast to Linked Devices: SUCCESS")

def test_google_parent_bridge():
    print("🧪 Testing Google Account Parent-Child Bridge...")
    class MockManager:
        protocol_dir = current_dir
    nexus = SiriLLMNexus(MockManager())
    
    # Test Parent Profile
    res = nexus.parent_controller.register_child("Android-v1")
    assert "SIRI_PARENT_ACTIVE" in res
    print(f"✅ Parent Profile Registration: SUCCESS ({res})")
    
    # Test Google Bridge
    broadcast = nexus.google_bridge.broadcast_decision("SYNC_HUD", {"master": "active"})
    assert broadcast is True
    print("✅ Google Bridge Broadcast: SUCCESS")
    
    # Test Identity Sync (Remote Fingerprint)
    remote_log = {'device': 'Android-v1', 'fingerprint_match': True}
    verified = nexus.identity_sync.verify_remote_entry(remote_log)
    assert verified is True
    print("✅ Remote Identity Sync: SUCCESS")

if __name__ == "__main__":
    try:
        test_spatial_render()
        test_siri_nexus()
        test_response_chain()
        test_path_optimization()
        test_temporal_path_sync()
        test_icloud_device_link()
        test_resonance_broadcast()
        test_google_parent_bridge()
        print("\n✨ ALL CORE LOGIC, PATHING & GOOGLE MASTER BRIDGE VERIFIED SUCCESSFULLY ✨")
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
