#!/usr/bin/env python3
"""
Simple HTTP server with clean URL routing for the Cloth Shop frontend.
Handles routes like /dashboard, /inventory, /billing, /reports, /login
"""
import http.server
import socketserver
import os
from urllib.parse import urlparse

PORT = 8080

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    """Handler that maps clean URLs to .html files"""
    
    def do_GET(self):
        # Parse the URL path
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Route mapping
        routes = {
            '/': '/dashboard',
            '/dashboard': '/dashboard.html',
            '/inventory': '/inventory.html',
            '/billing': '/billing.html',
            '/reports': '/reports.html',
            '/login': '/login.html',
        }
        
        # If path is in routes, rewrite it
        if path in routes:
            self.path = routes[path]
        
        # Call parent handler
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run_server():
    """Start the HTTP server"""
    with socketserver.TCPServer(("", PORT), CleanURLHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print(f"Clean URLs enabled:")
        print(f"  - http://localhost:{PORT}/dashboard")
        print(f"  - http://localhost:{PORT}/inventory")
        print(f"  - http://localhost:{PORT}/billing")
        print(f"  - http://localhost:{PORT}/reports")
        print(f"  - http://localhost:{PORT}/login")
        print(f"\nPress Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_server()
