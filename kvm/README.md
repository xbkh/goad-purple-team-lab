# MINILAB on KVM/libvirt — preparation

Local adaptation of the official MINILAB, outside the providers supported by GOAD.
Two machines: DC01 (192.168.56.30) and WS01 (192.168.56.31), both running
Server 2019; WS01 plays the role of the MINILAB scenario's member server.
Initial allocation: 2 GiB and 2 vCPU per machine, to be validated at provisioning.
Memory can be increased with `GOAD_VM_MEMORY=3072` if needed.

The Server 2019 box published by `mayfly` is pinned and its SHA-256 sum is
verified by `scripts/download-box.py`. Both VMs use the same base,
with separate disks. The Windows 10 image initially tried has an expired
evaluation that causes an automatic shutdown; it is no longer used.

The download, the VMDK → QCOW2 conversion and the addition of the libvirt boxes
come before startup. A temporary VM first completes the Windows initial
configuration and checks WinRM; its state is then integrated into the local box.
This step avoids running provisioning commands during the OOBE.
The shutdown of this VM uses an explicit Windows command; the conversion
only continues after its shutdown is confirmed.
Provisioning also fixes `GOAD/ansible/data.yml` locally: the network
interfaces are discovered on each machine, because the names differ
between DC01 and WS01. The shared loading of the lab configuration is kept.
Before joining, WS01 is generalised with Sysprep if its Windows identity is
identical to that of the controller. After this reboot, the script restores its
private address and removes the temporary preparation task.
`scripts/vagrant.sh` uses the container documented by
vagrant-libvirt, with the machine's libvirt socket.

The domain network is isolated. A second NAT network is planned only for
provisioning and must be isolated in turn before the attack phase.
Both VMs are deployed; the domain, the WS01 trust relationship, the
Wazuh services and agents, the real collection and the network isolation are validated.
The complete redeployment from scratch remains to be validated.
Do not launch the attacks until the full isolation has been verified.

## Commands

Prerequisites: Docker, working KVM/libvirt, Python 3.12 with venv, qemu-img,
Ruby to check syntax, and user access to the libvirt socket.

From `kvm/`, the manual steps are:

```sh
bash scripts/bootstrap.sh
make download
make boxes
make up
make provision
```

The Wazuh manager is started by `docker compose -f wazuh/compose.yml up -d`
after creating the isolated network defined in `lab-network.xml`.
Its enrolment password is created locally by bootstrap and excluded from Git.
The manager collects the JSON alerts; no dashboard or indexer is deployed.

The installation of the agents is defined in `wazuh/install-agents.yml`.
The local follow-up is in `logs/setup-status.txt` and `logs/finish-setup.log`.
Logs and secrets stay local. The Windows images are not published.
`scripts/export-alert-evidence.py` only exports an explicit list of
lab alert metadata; it excludes raw messages and commands.

To resume a provisioning already prepared up to the domain join:
`bash scripts/finish-setup.sh --from ad-members.yml`. This resume assumes that
the previous preparation steps succeeded.

Sources:
- https://vagrant-libvirt.github.io/vagrant-libvirt/installation.html
- https://vagrant-libvirt.github.io/vagrant-libvirt/configuration.html
- https://github.com/Orange-Cyberdefense/GOAD/tree/main/ad/MINILAB
- https://learn.microsoft.com/en-us/troubleshoot/windows-server/setup-upgrade-and-drivers/windows-installations-disk-duplication
