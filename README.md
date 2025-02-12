# FinTech Trading Platform with Advanced Observability

This project demonstrates a modern FinTech trading platform with comprehensive observability using industry-standard tools:

- **Prometheus**: Metrics collection and storage
- **Loki**: Log aggregation and querying
- **Grafana**: Visualization and dashboards
- **Tempo**: Distributed tracing
- **OpenTelemetry**: Unified observability data collection

## Architecture

The platform consists of three main microservices:

1. **Market Data Service** (Port 8000)
   - Real-time market data fetching
   - Historical data retrieval
   - Price and volume metrics

2. **Trade Execution Service** (Port 8001)
   - Order processing
   - Trade execution
   - Position management

3. **Risk Analysis Service** (Port 8002)
   - Real-time risk assessment
   - Portfolio analysis
   - Exposure monitoring

## Observability Features

### Metrics (Prometheus)
- Market data request latency
- Trade execution times
- Risk calculation durations
- System resource usage
- Custom business metrics

### Logging (Loki)
- Structured JSON logging
- Service-specific log streams
- Error tracking
- Audit logging

### Tracing (Tempo)
- Distributed transaction tracking
- Cross-service request flows
- Performance bottleneck identification
- Error context preservation

### OpenTelemetry Integration
- Unified data collection
- Automatic instrumentation
- Custom metrics and spans
- Context propagation

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fintech-trading-platform.git
cd fintech-trading-platform
```

2. Start the platform:
```bash
docker-compose up -d
```

3. Access the services:
   - Grafana: http://localhost:3000 (admin/admin)
   - Market Data API: http://localhost:8000/docs
   - Prometheus: http://localhost:9090

## Example Requests

### Get Market Data
```bash
curl http://localhost:8000/market-data/AAPL
```

### Get Historical Data
```bash
curl http://localhost:8000/historical-data/MSFT?days=30
```

## Monitoring Dashboards

### Trading Overview
- Real-time trading volume
- Price movements
- Order success rates
- System health

### Risk Metrics
- Portfolio exposure
- Risk levels
- Market volatility
- Position limits

### System Performance
- Service latencies
- Error rates
- Resource utilization
- API health

## Development

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Git

### Local Development
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

2. Install dependencies:
```bash
cd market-data-service
pip install -r requirements.txt
```

3. Run service locally:
```bash
uvicorn main:app --reload
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
