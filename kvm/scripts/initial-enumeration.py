#!/usr/bin/env python3
"""Guided MINILAB LDAP read and one SMB credential verification; no password export."""
import json,re,os
from pathlib import Path
from datetime import datetime,timezone
from ldap3 import Server,Connection,NTLM
from impacket.smbconnection import SMBConnection
root=Path(__file__).resolve().parents[2]
config=json.loads((root/'GOAD/ad/MINILAB/data/config.json').read_text())['lab']['domains']['mini.lab']
proof={'started_at':datetime.now(timezone.utc).isoformat(),'scope':['192.168.56.30','192.168.56.31'],'method':'guided: initial dave credentials from upstream lab configuration','ldap_bind_user':'dave'}
conn=Connection(Server('192.168.56.30',connect_timeout=10),user='MINILAB\\dave',password=config['users']['dave']['password'],authentication=NTLM,auto_bind=True,raise_exceptions=True,receive_timeout=20)
conn.search('DC=mini,DC=lab','(&(objectCategory=person)(objectClass=user))',attributes=['sAMAccountName','description','memberOf'])
proof['ldap_read_succeeded']=True
proof['scenario_accounts']=[]
bob_password=None
for entry in conn.entries:
 data=entry.entry_attributes_as_dict
 name=(data.get('sAMAccountName') or [''])[0]
 if name not in ('alice','bob','carol','dave'): continue
 descriptions=data.get('description',[])
 exposed=next((re.search(r'\(Password\s*:\s*([^)]+)\)',str(d),re.I) for d in descriptions if re.search(r'\(Password\s*:\s*([^)]+)\)',str(d),re.I)),None)
 groups=[v.split(',')[0].removeprefix('CN=') for v in data.get('memberOf',[])]
 proof['scenario_accounts'].append({'name':name,'groups':groups,'plaintext_password_in_description':bool(exposed)})
 if name=='bob' and exposed: bob_password=exposed.group(1).strip()
conn.unbind()
proof['bob_smb_login_from_read_description']=False
if bob_password:
 smb=SMBConnection('dc','192.168.56.30',timeout=15)
 smb.login('bob',bob_password,'MINILAB')
 proof['bob_smb_login_from_read_description']=True
 smb.logoff();smb.close()
proof['finished_at']=datetime.now(timezone.utc).isoformat()
p=root/'kvm/logs/initial-enumeration.json'
p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(proof,indent=2,ensure_ascii=False)+'\n');p.chmod(0o600)
print(json.dumps(proof,indent=2,ensure_ascii=False))
