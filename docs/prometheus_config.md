```
- job_name: pcp-dynamic-discovery
  metrics_path: /metrics
  consul_sd_configs:
  - server: 'consul.monitoring.svc:8500'
    allow_stale: true
    scheme: http
  relabel_configs:
  - source_labels: [__meta_consul_service_id]
    action: drop
    regex: "consul"
  - source_labels: [__meta_consul_service_metadata_skip]
    action: drop
    regex: "true"
  - source_labels:
    - __meta_consul_service_metadata_prometheus_io_path
    action: replace
    target_label: __metrics_path__
    regex: (.+)
  - source_labels: [__meta_consul_service]
    target_label: instance
  - action: labelmap
    regex: __meta_consul_service_metadata_(.+)
```