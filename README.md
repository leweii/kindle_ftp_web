# Kindle FTP & Web File Server

A simple local file server for transferring books and files to your Kindle (or any device) over WiFi. Includes both FTP and Web interfaces.

## Features

- **Web File Browser** - Beautiful web interface optimized for Kindle's experimental browser
- **FTP Server** - Standard FTP protocol for file manager apps and desktop clients
- **No Dependencies** - Web server uses Python standard library only
- **Cross-Platform** - Works on macOS, Linux, and Windows

## Quick Start

### Web File Browser (Recommended for Kindle)

```bash
python web_file_server.py
```

Then on your Kindle:
1. Open the experimental browser
2. Navigate to `http://<your-computer-ip>:8080`
3. Browse and download files directly

### FTP Server

```bash
pip install pyftpdlib
python ftp_server.py
```

## Connection Details

### Web Server
| Setting | Value |
|---------|-------|
| URL | `http://<your-ip>:8080` |
| Access | Read-only browsing and download |

### FTP Server
| Setting | Value |
|---------|-------|
| Host | `<your-ip>` |
| Port | `2121` |
| Username | `user` |
| Password | `12345` |
| Anonymous | Enabled (read-only) |

## Usage Tips

### Finding Your Computer's IP
The web server will display your local IP address when it starts. You can also find it with:
```bash
# macOS/Linux
ifconfig | grep "inet "

# Windows
ipconfig
```

### Kindle Browser Tips
- Kindle's browser works best with the web server
- Files download directly to your Kindle's documents folder
- Supported formats: `.azw3`, `.mobi`, `.epub`, `.pdf`, `.txt`

### Using FTP Clients
Connect with any FTP client (FileZilla, Cyberduck, etc.):
- Protocol: FTP
- Host: Your computer's IP
- Port: 2121
- Credentials: `user` / `12345`

## File Structure

```
kindle_ftp_web/
├── ftp_server.py      # FTP server script
├── web_file_server.py # Web file browser script
└── books/             # Default directory for your books
```

## Requirements

- Python 3.6+
- `pyftpdlib` (FTP server only): `pip install pyftpdlib`

## License

MIT
