# Server optimization

Increase The Maximum Number Of Open Files (nofile limit)

nolimit with Systemd
```
$ mkdir -p /etc/systemd/system/nginx.service.d
$ nano /etc/systemd/system/nginx.service.d/nginx.conf
[Service]
LimitNOFILE=30000
$ systemctl daemon-reload
$ systemctl restart nginx.service
```