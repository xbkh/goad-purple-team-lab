# Synthetic fixtures

These JSON files are artificial examples, not events emitted by the lab.
The `wazuh-logtest` 4.14.0 engine decodes them as JSON, whereas the Windows
rules are attached to the internal `windows_eventchannel` decoder.
The JSON-only tests therefore did not validate rules 100100–100102.

Remaining validation: observe the real events from the Windows agents with
their ID, time, account and source address, then check the
alerts in `/var/ossec/logs/alerts/alerts.json`.
Do not use these fixtures as proof of the detection of an attack.
