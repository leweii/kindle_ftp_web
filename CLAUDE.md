# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Local file server project with two serving methods:
- **FTP Server** (`ftp_server.py`) - Uses pyftpdlib for FTP protocol access
- **Web File Browser** (`web_file_server.py`) - HTTP server with styled web interface for browser/Kindle access

## Commands

### Setup
```bash
pip install pyftpdlib
```

### Run Servers
```bash
# FTP server on port 2121
python ftp_server.py

# Web file server on port 8080
python web_file_server.py
```

### Connect to FTP
```bash
ftp localhost 2121
# Username: user, Password: 12345
# Anonymous access also available (read-only)
```

## Architecture

Both servers serve the directory where the script is located (`os.path.dirname(os.path.abspath(__file__))`).

- **FTP Server**: Authenticated user gets full permissions (`elradfmwMT`), anonymous gets read-only (`elr`)
- **Web Server**: Read-only browsing with download capability, styled HTML interface with file-type icons
