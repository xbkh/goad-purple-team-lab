.PHONY: download convert boxes validate up down status provision
download:
	python3 scripts/download-box.py
convert:
	python3 scripts/convert-box.py
boxes: convert
	bash scripts/vagrant.sh box add --provider libvirt --name goad-kvm/dc01 cache/dc01-libvirt.box
	bash scripts/vagrant.sh box add --provider libvirt --name goad-kvm/ws01 cache/ws01-libvirt.box
validate:
	bash scripts/vagrant.sh validate
up:
	bash scripts/vagrant.sh up --provider libvirt
down:
	bash scripts/vagrant.sh halt
status:
	bash scripts/vagrant.sh status
provision:
	bash scripts/provision.sh
