#!/usr/bin/env python3
"""
Simple FTP Server
Serves the current directory via FTP protocol
"""

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

def main():
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()
    
    # Define a new user having full r/w permissions
    # Username: user, Password: 12345
    authorizer.add_user("user", "12345", current_dir, perm="elradfmwMT")
    
    # Define anonymous access (optional - uncomment if needed)
    authorizer.add_anonymous(current_dir, perm="elr")
    
    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer
    
    # Define a customized banner (optional)
    handler.banner = "FTP Server Ready"
    
    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('0.0.0.0', 2121)
    server = FTPServer(address, handler)
    
    # Set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5
    
    # Start FTP server
    print(f"Starting FTP server on port 2121...")
    print(f"Serving directory: {current_dir}")
    print(f"Login credentials:")
    print(f"  Username: user")
    print(f"  Password: 12345")
    print(f"  Anonymous access: enabled (read-only)")
    print(f"\nConnect using: ftp://localhost:2121")
    print(f"Press Ctrl+C to stop the server")
    
    server.serve_forever()

if __name__ == '__main__':
    main()
