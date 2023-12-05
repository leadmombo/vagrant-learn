import subprocess
import os

def run_command(command, capture_output=False):
    try:
        result = subprocess.run(command, check=True, shell=True, text=True, capture_output=capture_output)
        if capture_output:
            return result.stdout
    except subprocess.CalledProcessError:
        print(f"Failed to execute: {command}")
        exit(1)

# Install dnf
run_command("sudo yum install dnf -y")

# Install epel-release and memcached
run_command("sudo dnf install epel-release -y")
run_command("sudo dnf install memcached -y")

# Start and enable memcached service
run_command("sudo systemctl start memcached")
run_command("sudo systemctl enable memcached")

# Check memcached service status
print(run_command("sudo systemctl status memcached", capture_output=True))

# Edit memcached configuration file
memcached_config = "/etc/sysconfig/memcached"
with open(memcached_config, "r") as file:
    config_content = file.read()

config_content = config_content.replace('127.0.0.1', '0.0.0.0')

with open(memcached_config, "w") as file:
    file.write(config_content)

# Restart memcached service
run_command("sudo systemctl restart memcached")

# Update firewall rules
run_command("firewall-cmd --add-port=11211/tcp")
run_command("firewall-cmd --runtime-to-permanent")
run_command("firewall-cmd --add-port=11111/udp")
run_command("firewall-cmd --runtime-to-permanent")

# Run memcached with specific parameters
run_command("sudo memcached -p 11211 -U 11111 -u memcached -d")