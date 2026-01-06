# 🔍 SQL Query Cost Analyzer

A FastAPI-based SQL query analysis tool that detects issues, estimates costs, and provides optimization suggestions. Built with async processing and in-memory caching for high performance.

## ✨ Features

- **Query Analysis**: Detects common SQL issues (missing WHERE, SELECT *, leading wildcards)
- **Cost Estimation**: Estimates query execution cost based on complexity
- **Optimization Tips**: Provides actionable suggestions to improve queries
- **Async Processing**: Handles multiple queries concurrently
- **Smart Caching**: LRU cache with TTL for fast repeated queries
- **Batch API**: Analyze multiple queries in parallel
- **Zero Dependencies**: No Docker or Redis required - simple Python setup

## 🏗️ Architecture

```
sql-query-analyzer/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app & endpoints
│   ├── models.py            # Pydantic models
│   ├── analyzer.py          # Query analysis logic
│   ├── cost_calculator.py   # Cost estimation
│   └── optimizer.py         # Optimization suggestions
├── cache/
│   └── memory_cache.py      # Thread-safe LRU cache
├── config/
│   └── settings.py          # App configuration
├── tests/
│   └── test_analyzer.py     # Unit tests
└── requirements.txt
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sql-query-analyzer.git
cd sql-query-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn app.main:app --reload --port 8000
```

Visit http://localhost:8000/docs for interactive API documentation.

## 📡 API Endpoints

### Analyze Single Query
```bash
POST /analyze
Content-Type: application/json

{
  "query": "SELECT * FROM users WHERE id = 1",
  "database_type": "postgresql"
}
```

**Response:**
```json
{
  "query": "SELECT * FROM users WHERE id = 1",
  "issues": ["Using SELECT * - fetches unnecessary columns"],
  "cost_estimate": 1.0,
  "optimization_tips": ["Replace SELECT * with specific columns"],
  "execution_time_ms": 0.52,
  "cached": false
}
```

### Analyze Batch Queries
```bash
POST /analyze/batch
Content-Type: application/json

[
  {"query": "SELECT * FROM users"},
  {"query": "DELETE FROM logs"}
]
```

### Health Check
```bash
GET /health
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app
```

## 💡 What It Detects

| Issue | Detection |
|-------|-----------|
| Missing WHERE clause | DELETE/UPDATE without WHERE |
| SELECT * usage | Fetching unnecessary columns |
| Leading wildcards | LIKE '%term' prevents index usage |
| Multiple JOINs | Suggests index verification |
| Subqueries | Identifies optimization opportunities |

## 🎯 Use Cases

- **Development**: Catch problematic queries before production
- **Code Review**: Automated SQL quality checks
- **Learning**: Understand query optimization
- **Performance**: Identify expensive queries early

## 🔧 Configuration

Edit `config/settings.py`:

```python
CACHE_MAX_SIZE = 1000      # Max cached queries
CACHE_TTL_SECONDS = 3600   # Cache expiration (1 hour)
```

## 📊 Performance

- **Caching**: ~0.1ms for cached queries
- **Analysis**: ~10-50ms for complex queries
- **Batch**: Processes queries in parallel using asyncio

## 🛠️ Tech Stack

- **FastAPI**: Modern async web framework
- **SQLParse**: SQL parsing and formatting
- **Pydantic**: Data validation
- **Pytest**: Testing framework
- **Uvicorn**: ASGI server

## 📈 Future Enhancements

- [ ] Redis integration for distributed caching
- [ ] Real database query plan analysis
- [ ] Custom rule configuration
- [ ] Query performance benchmarking
- [ ] Support for more database types


⭐ Star this repo if you find it helpful!
