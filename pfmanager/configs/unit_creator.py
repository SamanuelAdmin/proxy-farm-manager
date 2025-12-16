"""
Use it to create systemd unit for 3proxy
"""

def PROXY_UNIT(path_to_proxy: str, path_to_file):
    return f"""[Unit]
Description=3proxy Socks5 Server (for proxy farm manager)
After=network.target

[Service]
Type=simple
ExecStart={path_to_proxy} {path_to_file}
Restart=always

[Install]
WantedBy=multi-user.target
"""
