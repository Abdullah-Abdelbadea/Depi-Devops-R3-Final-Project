FROM prom/prometheus:latest

COPY prometheus.yml /etc/prometheus/prometheus.yml
COPY alerts.rules.yml /etc/prometheus/alerts.rules.yml

EXPOSE 9090

CMD ["--config.file=/etc/prometheus/prometheus.yml"]

