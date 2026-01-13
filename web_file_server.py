#!/usr/bin/env python3
"""
Web File Browser and Download Server
Serves files from the current directory with a nice web interface
"""

import os
import http.server
import socketserver
import urllib.parse
from pathlib import Path
import socket

class FileServerHandler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        """Helper to produce a directory listing with better styling."""
        try:
            file_list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        
        file_list.sort(key=lambda a: a.lower())
        
        # Separate directories and files
        dirs = []
        files = []
        for name in file_list:
            fullname = os.path.join(path, name)
            if os.path.isdir(fullname):
                dirs.append(name)
            else:
                files.append(name)
        
        # Build HTML response
        displaypath = urllib.parse.unquote(self.path)
        enc = 'utf-8'
        
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html><head>')
        html_parts.append('<meta charset="utf-8">')
        html_parts.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
        html_parts.append(f'<title>File Browser - {displaypath}</title>')
        html_parts.append('''
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f5f5f5;
                padding: 20px;
                line-height: 1.6;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 {
                font-size: 28px;
                margin-bottom: 10px;
            }
            .path {
                background: #f8f9fa;
                padding: 15px 30px;
                border-bottom: 1px solid #dee2e6;
                font-family: monospace;
                word-break: break-all;
            }
            .file-list {
                padding: 20px 30px;
            }
            .file-item {
                display: block;
                padding: 10px 0;
                text-decoration: none;
                color: #333;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .file-item:hover {
                color: #667eea;
            }
            .file-item.directory {
                color: #0066cc;
            }
            .icon {
                margin-right: 10px;
                font-size: 24px;
            }
            .file-name {
                font-size: 22px;
            }
            .file-size {
                color: #6c757d;
                font-size: 18px;
                margin-left: 12px;
            }
            .empty {
                text-align: center;
                padding: 50px;
                color: #6c757d;
            }
            @media (max-width: 768px) {
                body { padding: 10px; }
                .header { padding: 20px; }
                .header h1 { font-size: 22px; }
                .path { padding: 10px 15px; font-size: 14px; }
                .file-list { padding: 10px 15px; }
                .file-name { font-size: 18px; }
                .file-size { font-size: 14px; }
            }
        </style>
        ''')
        html_parts.append('</head><body>')
        html_parts.append('<div class="container">')
        html_parts.append('<div class="header">')
        html_parts.append('<h1>📁 File Browser</h1>')
        html_parts.append('<p>Click to download files or browse folders</p>')
        html_parts.append('</div>')
        html_parts.append(f'<div class="path">📍 Current Path: {displaypath}</div>')
        html_parts.append('<div class="file-list">')
        
        # Add parent directory link if not root
        if displaypath != '/':
            html_parts.append('<a href=".." class="file-item directory">')
            html_parts.append('<span class="icon">⬆️</span>')
            html_parts.append('<span class="file-name"><strong>Parent Directory</strong></span>')
            html_parts.append('</a>')
        
        # List directories first
        for name in dirs:
            fullname = os.path.join(path, name)
            linkname = urllib.parse.quote(name, errors='surrogatepass')
            html_parts.append(f'<a href="{linkname}/" class="file-item directory">')
            html_parts.append('<span class="icon">📁</span>')
            html_parts.append(f'<span class="file-name">{name}</span>')
            html_parts.append('</a>')
        
        # Then list files
        for name in files:
            fullname = os.path.join(path, name)
            linkname = urllib.parse.quote(name, errors='surrogatepass')
            file_size = os.path.getsize(fullname)
            size_str = self.format_size(file_size)
            
            # Determine file icon based on extension
            icon = self.get_file_icon(name)
            
            html_parts.append(f'<a href="{linkname}" class="file-item" download>')
            html_parts.append(f'<span class="icon">{icon}</span>')
            html_parts.append(f'<span class="file-name">{name}</span>')
            html_parts.append(f'<span class="file-size">{size_str}</span>')
            html_parts.append('</a>')
        
        if not dirs and not files:
            html_parts.append('<div class="empty">📭 This folder is empty</div>')
        
        html_parts.append('</div>')
        html_parts.append('</div>')
        html_parts.append('</body></html>')
        
        encoded = '\n'.join(html_parts).encode(enc, 'surrogateescape')
        
        self.send_response(200)
        self.send_header("Content-type", f"text/html; charset={enc}")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        
        return self.wfile.write(encoded)
    
    def format_size(self, bytes_size):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} PB"
    
    def get_file_icon(self, filename):
        """Return an emoji icon based on file extension."""
        ext = os.path.splitext(filename)[1].lower()
        
        icon_map = {
            # Documents
            '.pdf': '📕',
            '.doc': '📘', '.docx': '📘',
            '.txt': '📄',
            '.rtf': '📝',
            '.odt': '📄',
            
            # Images
            '.jpg': '🖼️', '.jpeg': '🖼️',
            '.png': '🖼️',
            '.gif': '🖼️',
            '.bmp': '🖼️',
            '.svg': '🎨',
            '.ico': '🖼️',
            
            # Audio
            '.mp3': '🎵',
            '.wav': '🎵',
            '.flac': '🎵',
            '.m4a': '🎵',
            '.ogg': '🎵',
            
            # Video
            '.mp4': '🎬',
            '.avi': '🎬',
            '.mkv': '🎬',
            '.mov': '🎬',
            '.wmv': '🎬',
            
            # Archives
            '.zip': '📦',
            '.rar': '📦',
            '.7z': '📦',
            '.tar': '📦',
            '.gz': '📦',
            
            # Code
            '.py': '🐍',
            '.js': '💛',
            '.html': '🌐',
            '.css': '🎨',
            '.java': '☕',
            '.cpp': '⚙️', '.c': '⚙️',
            '.php': '🐘',
            '.rb': '💎',
            '.go': '🔵',
            
            # eBook formats
            '.epub': '📚',
            '.mobi': '📚',
            '.azw': '📚',
            '.azw3': '📚',
        }
        
        return icon_map.get(ext, '📄')

def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def main():
    PORT = 8080
    
    # Change to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    handler = FileServerHandler
    
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        local_ip = get_local_ip()
        
        print("=" * 60)
        print("📁 Web File Browser Server Started!")
        print("=" * 60)
        print(f"\n📍 Serving directory: {os.getcwd()}")
        print(f"\n🌐 Access the server from:")
        print(f"   • Local:    http://localhost:{PORT}")
        print(f"   • Network:  http://{local_ip}:{PORT}")
        print(f"\n📱 On your Kindle, open the browser and go to:")
        print(f"   http://{local_ip}:{PORT}")
        print(f"\n💡 Make sure your Kindle is on the same WiFi network!")
        print(f"\n⛔ Press Ctrl+C to stop the server")
        print("=" * 60)
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped.")

if __name__ == "__main__":
    main()
