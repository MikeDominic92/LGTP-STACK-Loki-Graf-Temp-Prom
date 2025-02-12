# FinTech Trading Platform with Advanced Observability

A comprehensive FinTech trading platform demonstrating real-world usage of modern observability tools:

## Core Components

### 1. Observability Stack
- **Prometheus**: Metrics collection and storage
- **Loki**: Log aggregation and analysis
- **Grafana**: Visualization and dashboards
- **Tempo**: Distributed tracing
- **OpenTelemetry**: Unified telemetry collection

### 2. Microservices
- **Market Data Service**: Real-time market data and historical analysis
- **Trade Execution Service**: Order processing and execution
- **Risk Analysis Service**: Real-time risk assessment

## Features

### Market Data Service
- Real-time stock price monitoring
- Historical data analysis
- Price and volume metrics
- OpenTelemetry instrumentation
- Custom business metrics

### Observability Features
- Real-time trading metrics
- Service performance monitoring
- Distributed tracing for transactions
- Log correlation across services
- Custom Grafana dashboards

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/MikeDominic92/LGTP-STACK-Loki-Graf-Temp-Prom.git
cd LGTP-STACK-Loki-Graf-Temp-Prom
```

2. Start the platform:
```bash
docker-compose up -d
```

3. Access services:
- Grafana: http://localhost:3000 (admin/admin)
- Market Data API: http://localhost:8000/docs
- Prometheus: http://localhost:9090

## API Endpoints

### Market Data Service (Port 8000)
- GET /market-data/{symbol} - Get real-time market data
- GET /historical-data/{symbol} - Get historical price data
- GET /metrics - Prometheus metrics endpoint

## Monitoring

### Metrics Available
- Trade volume and execution times
- Market data request latency
- Error rates and types
- System resource utilization

### Logging
- Structured JSON logging
- Error tracking and alerting
- Audit trail for all trades

### Tracing
- End-to-end transaction tracking
- Performance bottleneck identification
- Cross-service request flows

## License
MIT License
