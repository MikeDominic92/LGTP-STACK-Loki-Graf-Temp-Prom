from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yfinance as yf
import pandas as pd
from datetime import datetime
import logging
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
import os

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentation

# Set up logging
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Set up OpenTelemetry
if os.getenv('ENABLE_TELEMETRY', 'false').lower() == 'true':
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)

    # Configure OTLP exporters
    otlp_endpoint = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4317')
    otlp_span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_span_exporter))

    # Metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
    )
    metrics.set_meter_provider(MeterProvider(metric_readers=[metric_reader]))
    meter = metrics.get_meter(__name__)
else:
    tracer = trace.get_tracer(__name__)
    meter = metrics.get_meter(__name__)

# Create metrics
request_counter = meter.create_counter(
    "market_data_requests",
    description="Number of market data requests",
    unit="1",
)

price_gauge = meter.create_gauge(
    "stock_price",
    description="Current stock price",
    unit="USD",
)

# Prometheus metrics
SCRAPE_DURATION = Histogram(
    'market_data_scrape_duration_seconds',
    'Time spent scraping market data',
    ['symbol']
)

REQUEST_COUNT = Counter(
    'market_data_request_total',
    'Total market data requests',
    ['symbol', 'endpoint']
)

app = FastAPI(title="Market Data Service")
FastAPIInstrumentation().instrument_app(app)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/market-data/{symbol}")
async def get_market_data(symbol: str):
    with tracer.start_as_current_span("get_market_data") as span:
        try:
            span.set_attribute("symbol", symbol)
            start_time = time.time()
            
            # Increment request counter
            request_counter.add(1, {"symbol": symbol})
            REQUEST_COUNT.labels(symbol=symbol, endpoint="/market-data").inc()
            
            # Fetch data from Yahoo Finance
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            
            if hist.empty:
                logger.error(f"No data found for symbol {symbol}")
                raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
            
            current_price = hist['Close'].iloc[-1]
            price_gauge.set(current_price, {"symbol": symbol})
            
            # Record duration
            duration = time.time() - start_time
            SCRAPE_DURATION.labels(symbol=symbol).observe(duration)
            
            logger.info(f"Market data retrieved for {symbol}", extra={
                "symbol": symbol,
                "price": current_price,
                "duration": duration
            })
            
            return {
                "symbol": symbol,
                "price": current_price,
                "timestamp": datetime.now().isoformat(),
                "volume": hist['Volume'].iloc[-1]
            }
            
        except Exception as e:
            logger.error(f"Error fetching market data for {symbol}", extra={
                "symbol": symbol,
                "error": str(e)
            })
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/historical-data/{symbol}")
async def get_historical_data(symbol: str, days: int = 30):
    with tracer.start_as_current_span("get_historical_data") as span:
        try:
            span.set_attribute("symbol", symbol)
            span.set_attribute("days", days)
            
            REQUEST_COUNT.labels(symbol=symbol, endpoint="/historical-data").inc()
            
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=f"{days}d")
            
            if hist.empty:
                logger.error(f"No historical data found for symbol {symbol}")
                raise HTTPException(status_code=404, detail=f"No historical data found for symbol {symbol}")
            
            # Convert to list of dictionaries for JSON serialization
            data = []
            for date, row in hist.iterrows():
                data.append({
                    "date": date.isoformat(),
                    "open": row['Open'],
                    "high": row['High'],
                    "low": row['Low'],
                    "close": row['Close'],
                    "volume": row['Volume']
                })
            
            logger.info(f"Historical data retrieved for {symbol}", extra={
                "symbol": symbol,
                "days": days,
                "records": len(data)
            })
            
            return {
                "symbol": symbol,
                "data": data
            }
            
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}", extra={
                "symbol": symbol,
                "days": days,
                "error": str(e)
            })
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
