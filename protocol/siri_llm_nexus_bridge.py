import sys
import os
from bioglobe import BioglobeManager

def main():
    if len(sys.argv) < 2:
        print("The resonance requires a query.")
        return

    query = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "FAST"

    manager = BioglobeManager()
    # We don't need to start a full convergence here, just the nexus processing.
    response = manager.nexus.process_siri_input(query, mode=mode)
    
    # Only print the response to stdout for the Swift pipe to catch
    print(response)

if __name__ == "__main__":
    main()
