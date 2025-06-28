#!/usr/bin/env python3
"""
Frontend server for mentor-mentee app
Serves static files on http://localhost:3000
"""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler


class FrontendHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="frontend", **kwargs)
    
    def end_headers(self):
        # Add CORS headers for API calls to localhost:8080
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header(
            'Access-Control-Allow-Methods', 
            'GET, POST, PUT, DELETE, OPTIONS'
        )
        self.send_header(
            'Access-Control-Allow-Headers', 
            'Content-Type, Authorization'
        )
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


def main():
    port = 3000
    
    # Change to project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if frontend directory exists
    if not os.path.exists("frontend"):
        print("❌ Frontend directory not found!")
        sys.exit(1)
    
    server = HTTPServer(('localhost', port), FrontendHandler)
    print("� Mentor-Mentee Matching App")
    print("=" * 50)
    print(f"🌐 Frontend App: http://localhost:{port}/")
    print(f"🌐 Dashboard: http://localhost:{port}/dashboard.html")
    print("🔗 Backend API: http://localhost:8080/api")
    print("📖 API Docs: http://localhost:8080/docs")
    print("=" * 50)
    print("📁 Serving files from ./frontend directory")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
        server.shutdown()


if __name__ == "__main__":
    main()
