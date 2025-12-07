### Some actions connected with daemon
```bash
cd _daemon
```

```bash
nano start_daemon.sh
```

```bash
#!/bin/bash
# /usr/local/bin/my_daemon.sh

source /path/to/your/project/.venv/bin/activate
python /path/to/your/project/your_script.py
```

```bash
/etc/systemd/system/lebinetx-backend.service
```

```bash
nano /etc/systemd/system/lebinetx-backend.service
```

```service
[Unit]
Description=LebiNetX API service
After=network.target

[Service]
Type=simple
User=glebocrew
Group=glebocrew
WorkingDirectory=/home/glebocrew/Projects/lebinetx/backend/api
ExecStart=/home/glebocrew/Projects/lebinetx/backend/api/_daemon/start_daemon.sh
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=my-daemon

[Install]
WantedBy=multi-user.target
```