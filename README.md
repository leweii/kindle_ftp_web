# FTP Server

A simple local FTP server that serves the current directory.

## Setup

1. Install the required Python package:
```bash
pip install pyftpdlib
```

2. Run the FTP server:
```bash
python ftp_server.py
```

## Connection Details

- **Server Address**: `ftp://localhost:2121`
- **Username**: `user`
- **Password**: `12345`
- **Anonymous Access**: Enabled (read-only)

## Connect via Command Line

```bash
ftp localhost 2121
# Then login with username: user, password: 12345
# Or login as anonymous
```

## Connect via FileZilla or Other FTP Clients

- Host: `localhost`
- Port: `2121`
- Protocol: `FTP`
- Username: `user`
- Password: `12345`

## Permissions

- Authenticated user (`user`): Full read/write permissions
- Anonymous: Read-only access

## Stop the Server

Press `Ctrl+C` in the terminal where the server is running.
