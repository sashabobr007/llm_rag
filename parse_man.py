import subprocess
import re
from tqdm import tqdm

commands_names = [
    "ls",
    "cd",
    "pwd",
    "mkdir",
    "rm",
    "cp",
    "mv",
    "touch",
    "cat",
    "less",
    "head",
    "tail",
    "grep",
    "find",
    "chmod",
    "chown",
    "chgrp",
    "tar",
    "zip",
    "unzip",
    "adduser",
    "usermod",
    "deluser",
    "passwd",
    "su",
    "sudo",
    "finger",
    "who",
    "id",
    "groups",
    "useradd",
    "userdel",
    "usermod",
    "passwd",
    "last",
    "w",
    "logout",
    'apt-get install', 'apt-get remove', 'apt-get update', 'apt-get upgrade', 'apt-cache search',
            'dpkg -i', 'dpkg -r', 'dpkg -l', 'snap install', 'snap remove', 'snap list',
            'systemctl start', 'systemctl stop', 'systemctl restart', 'systemctl enable', 'systemctl disable',
            'service <service> start', 'service <service> stop', 'service <service> restart', 'service <service> status',
'shutdown', 'reboot', 'halt', 'poweroff', 'systemctl', 'service', 'ifconfig', 'ip',
            'netstat', 'ping', 'traceroute', 'ssh', 'scp', 'rsync', 'crontab', 'at',
            'shutdown', 'nohup', 'history','top', 'ps', 'kill', 'pkill', 'htop', 'free', 'vmstat', 'killall', 'renice', 'nice',
            'pgrep', 'strace', 'lsof', 'sar', 'uptime', 'time','smem', 'sync', 'swapoff', 'swapon', 'sysctl', 'ulimit', 'pmap', 'slabtop', 'ulimit', 'numactl', 'sysrq', 'mdb'
]

def remove_spaces(text):
    return re.sub(r'\s{2,}', ' ', text)

def split_last(text):
    pattern = r"--.*?      "
    matches = re.findall(pattern, text)
    last_match = matches[-1] if matches else None
    t = text.split(last_match)[0]
    #print(t)
    return t


# # Для каждой команды создаем файл txt с man-страницей
for command in tqdm(commands_names):
    try:
        filename = f"man/{command}.txt"
        with open(filename, "w") as file:
            man_command = subprocess.run(f"man {command}", shell=True, check=True, capture_output=True).stdout.decode()
            file.write(man_command)
            tn = man_command.split('DDEESSCCRRIIPPTTIIOONN')[1]
            filename_preprocessed = f"man/{command}_preprocessed.txt"
            with open(filename_preprocessed, "w") as file:
                file.write(remove_spaces(split_last(tn)))
    except:
        print(command)

# with open('man/pwd_preprocessed.txt', 'r') as file:
#     t = file.read()
#     print(t)
#

