# Maintained reliability fork

This integration is based on
[upstream release `v1.2.2`](https://github.com/romfreiman/tornado-aircon-custom-component/releases/tag/v1.2.2),
commit `f2af31211628c2dbd5c4148d12a515568a60fc7e`.

First maintained release: `1.2.3`.

The fork changes intentionally preserve the `tornado` domain, device
identifiers, entity unique IDs, modes, and services. They only change cloud
transport and refresh behavior:

- use Home Assistant's managed HTTP session instead of an ignored duplicate
  session;
- allow 30 seconds for response data;
- fetch devices once during setup;
- use one coordinator refresh every five minutes;
- keep entities available from the last successful device data when a later
  refresh fails.
