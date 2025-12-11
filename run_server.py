"""
Simple script to run Flask server for local testing
"""
import socket
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'netlify', 'functions'))
from api import app

def find_free_port(start_port=5001, max_attempts=10):
    """Find a free port starting from start_port"""
    for i in range(max_attempts):
        port = start_port + i
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                continue
    return None

if __name__ == "__main__":
    port = find_free_port()
    if port is None:
        print("❌ Could not find a free port. Please close other applications.")
        exit(1)
    
    print(f"🚀 Starting Flask server on http://localhost:{port}")
    print(f"🌐 Open http://localhost:{port} in your browser to use the web interface")
    print("📝 API Endpoints:")
    print("   GET  /              - Web interface")
    print("   GET  /api/health    - Health check")
    print("   POST /api/generate-pdf - Generate PDF")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print(f"✅ Server is ready! Open: http://localhost:{port}\n")
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)

