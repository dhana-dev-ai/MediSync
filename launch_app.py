#!/usr/bin/env python3
"""
MediSync Quick Launcher
Starts the Streamlit app with all necessary setup
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def main():
    # Change to script directory (platform-independent)
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print("=" * 70)
    print("🏥 MediSync - Multi-Agent Healthcare Assistant")
    print("=" * 70)
    print()
    
    # Launch Streamlit
    print("🚀 Launching Streamlit app...")
    print("📍 Access at: http://localhost:8501")
    print()
    print("-" * 70)
    
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "medisync_app.py", 
             "--server.port=8501", "--server.address=localhost"],
            check=False
        )
    except KeyboardInterrupt:
        print("\n\n👋 App closed by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
