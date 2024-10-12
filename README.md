
# ReadMe

## Description
py_mounter is a service automation intended to mount the harddrive when system reboots.
Target: RPI.

## Setup
### Create this service file.
This file defines the service and picks up the script needs to be executed.

* location: `/etc/systemd/system/py_mounter.service `

```
[Unit]
Description=My Python Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/prince/Work/python/py_mounter/py_mounter.py
WorkingDirectory=/home/prince
Restart=always
User=prince
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

### Create a timer.
The timer defines how often the service should re-run. It the cron spec.

* location: `/etc/systemd/system/py_mounter.service `

```
[Unit]
Description=Runs py_mounter.service every 1 minutes

[Timer]
OnBootSec=2min
OnUnitActiveSec=1min
Unit=py_mounter.service

[Install]
WantedBy=timers.target

```
OnBootSec is to ensure rediness. It waits 2 minutes after system bootup.

OnUnitActiveSec specifies the interval for re-execution.

### Disable authentication for the user.

* file: `/usr/share/polkit-1/actions/org.freedesktop.UDisks2.policy`

As per [this](https://en.linuxportal.info/tutorials/troubleshooting/how-to-clear-the-not-authorized-to-perform-operation-error-message-when-automatically-attaching-USB-flash-drives-and-other-external-USB-storage-devices) article, `Mount a filesystem` section needs retouch for the `udisksctl` to mount the drive without human interaction. Normaly it requires an initiation from the user. Below steps will bypass it. 


For this section:
```
<action id="org.freedesktop.udisks2.filesystem-mount">
```

Change the defaults to this.
```
   <defaults>
      <allow_any>yes</allow_any>
      <allow_inactive>yes</allow_inactive>
      <allow_active>yes</allow_active>
    </defaults>

```

## Commands will come handy.

* To reload the daemon.

`sudo systemctl daemon-reload`

* To enable the service or a time.

`sudo systemctl enable py_mounter.service` or `sudo systemctl enable py_mounter.timer`

* To start the service.

`sudo systemctl start py_mounter.timer`

* To restart the service.

`sudo systemctl restart py_mounter.service`

* To view the quick status.

`sudo systemctl status py_mounter.service`

* To follow the log.

`sudo journalctl -u py_mounter.service`