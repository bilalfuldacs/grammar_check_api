# Grammar Check API

A FastAPI-based grammar checking service using local LLM (Gemma 3 1B) via Ollama.

## Features

- ✅ **Grammar Error Detection**: Identifies and corrects grammar errors
- ✅ **Triplet Output**: Returns `wrong`, `corrected`, and `error_type`
- ✅ **Local LLM**: Uses Gemma 3 1B for privacy and cost-effectiveness
- ✅ **RESTful API**: Clean HTTP endpoints with proper status codes
- ✅ **Error Handling**: Comprehensive exception handling
- ✅ **Async Architecture**: Non-blocking, scalable design

## Quick Start

### Prerequisites

1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
2. **Pull Model**: `ollama pull gemma3:1b`
3. **Python 3.8+**: Required for async/await support

### Installation

```bash
# Clone and setup
git clone <repository>
cd grammar-check-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama
ollama serve

# In another terminal, start the API
python -m uvicorn app.main:app --reload
```

### Usage

```bash
# Health check
curl http://localhost:8000/health

# Grammar check
curl -X POST "http://localhost:8000/check" \
  -H "Content-Type: application/json" \
  -d '{"text": "I goes to the store yesterday."}'
```

## API Endpoints

### `GET /health`
Check if the service is running and Ollama is connected.

**Response:**
```json
{
  "status": "healthy",
  "ollama_connected": true
}
```

### `POST /check`
Check grammar in the provided text.

**Request:**
```json
{
  "text": "I goes to the store yesterday."
}
```

**Response:**
```json
{
  "issues": [
    {
      "wrong": "I goes",
      "corrected": "I went",
      "error_type": "verb tense"
    }
  ]
}
```

## System Evaluation

### Evaluation Framework

The system includes a comprehensive evaluation framework to assess:

1. **🎯 Accuracy**: Grammar error detection capability
2. **⚡ Performance**: Response times and throughput
3. **🛡️ Reliability**: Error handling and edge cases
4. **🌐 API**: Endpoint functionality and documentation

### Running Evaluation

```bash
# Start your API first
python -m uvicorn app.main:app --reload

# In another terminal, run evaluation
python run_evaluation.py
```

### Evaluation Metrics

#### Accuracy Metrics
- **Precision**: How many detected errors are actually correct
- **Recall**: How many actual errors are detected
- **F1-Score**: Harmonic mean of precision and recall

#### Performance Metrics
- **Average Response Time**: Typical processing time
- **Success Rate**: Percentage of successful requests
- **Throughput**: Requests per second capability

#### Reliability Metrics
- **Error Handling**: Proper HTTP status codes
- **Edge Cases**: Empty text, long text, special characters
- **API Endpoints**: All endpoints functional

### Sample Evaluation Output

```
📋 GRAMMAR CHECK API EVALUATION REPORT
============================================================
Date: 2024-01-15 14:30:25
Model: gemma3:1b
Framework: FastAPI
============================================================

🎯 ACCURACY EVALUATION
==================================================
📝 Test Case 1: I goes to the store yesterday. She have a apple.
  ✅ Correct detections: 3
  ❌ False positives: 0
  ❌ False negatives: 0
  📋 Detected errors:
    - 'I goes' → 'I went' (verb tense)
    - 'She have' → 'She has' (subject-verb agreement)
    - 'a apple' → 'an apple' (article usage)

📊 ACCURACY METRICS:
  Precision: 1.000
  Recall: 1.000
  F1-Score: 1.000
  Total Correct: 8/8

⚡ PERFORMANCE EVALUATION
==================================================
📝 Performance Test 1: 35 characters
  Run 1: 12.45s, 3 issues
  Run 2: 11.89s, 3 issues
  Run 3: 12.23s, 3 issues

📊 PERFORMANCE METRICS:
  Average Response Time: 12.19s
  Median Response Time: 12.23s
  Min Response Time: 11.89s
  Max Response Time: 12.45s
  Success Rate: 9/9 (100.0%)

🛡️ RELIABILITY EVALUATION
==================================================
  ✅ Empty text: PASS
  ✅ Text too long: PASS
  ✅ Normal text: PASS
  ✅ Text with errors: PASS

📊 RELIABILITY SCORE: 4/4 (100.0%)

🌐 API ENDPOINT EVALUATION
==================================================
  ✅ Root endpoint: Working
  ✅ Health check: Working
  ✅ API documentation: Working

📊 API ENDPOINTS: 3/3 working
```

## Why FastAPI?

### ✅ **Advantages for This Project:**

1. **Async Performance**: Built for high-performance async operations
2. **Automatic Documentation**: Auto-generates OpenAPI/Swagger docs
3. **Type Safety**: Pydantic models with automatic validation
4. **Modern Python**: Uses latest Python features (async/await, type hints)
5. **Lightweight**: Minimal boilerplate, fast startup
6. **Production Ready**: Used by Netflix, Microsoft, Uber

### ❌ **Why Not Django?**

- **Overkill**: Django is a full-stack framework with ORM, admin, etc.
- **Performance**: Slower than FastAPI for API-only projects
- **Complexity**: More setup and configuration required
- **Async Support**: Limited async capabilities compared to FastAPI

### ❌ **Why Not Flask?**

- **No Async**: Flask doesn't have native async support
- **Manual Setup**: Requires more manual configuration
- **Documentation**: No automatic API documentation
- **Type Safety**: No built-in type validation

## Why Local LLM?

### ✅ **Advantages:**

1. **Privacy**: No data sent to external services
2. **Cost**: No API costs or usage limits
3. **Control**: Full control over model and deployment
4. **Offline**: Works without internet connection
5. **Customization**: Can fine-tune for specific use cases

### ❌ **Why Not OpenAI?**

- **Privacy Concerns**: Data sent to external servers
- **Cost**: Per-token pricing can be expensive
- **Dependency**: Relies on external service availability
- **Rate Limits**: API usage restrictions
- **Data Control**: Limited control over data processing

## Why Gemma 3 1B?

### **🎯 My Model Selection Process**

When I started this project, I needed to choose an LLM for grammar checking. I looked at the available models in Ollama and tested a few to see which one worked best for my needs.

### **✅ Why I Chose Gemma 3 1B**

After trying different models, I found that **Gemma 3 1B** was the best fit for this grammar checking task.

#### **What I Tested:**
```bash
# I tried these models
ollama pull gemma3:1b
ollama pull llama3.2:3b  
ollama pull zephyr:7b
```

#### **What I Found:**

**Gemma 3 1B:**
- ✅ **Fast enough**: ~12 seconds per request
- ✅ **Works on my laptop**: Only needs 2GB RAM
- ✅ **Good accuracy**: Detects grammar errors well
- ✅ **Reliable JSON**: Consistent output format

**Llama 3.2 3B:**
- ❌ **Too slow**: ~25 seconds per request
- ❌ **Heavy**: Needs 4GB RAM
- ✅ **Better accuracy**: But not worth the extra resources

**Zephyr 7B:**
- ❌ **Very slow**: ~45 seconds per request
- ❌ **Crashed my laptop**: Needs 8GB RAM
- ✅ **Best accuracy**: But way too heavy for this task

### **🎯 My Decision**

I chose **Gemma 3 1B** because:

1. **Fast enough**: 12 seconds is acceptable for grammar checking
2. **Works everywhere**: Only needs 2GB RAM
3. **Good accuracy**: Detects grammar errors reliably
4. **Simple**: Easy to set up and use

### **📊 Simple Comparison**

| Model | Speed | Memory | Accuracy | Works on Laptop |
|-------|-------|--------|----------|-----------------|
| **Gemma 3 1B** | ⚡ Fast | 2GB | Good | ✅ Yes |
| Llama 3.2 3B | 🐌 Slow | 4GB | Better | ❌ Struggles |
| Zephyr 7B | 🐌 Very Slow | 8GB | Best | ❌ Crashes |

### **🎯 For Production (Future)**

If I had better hardware or more time, I might try:
```bash
ollama pull llama3.2:3b  # Better accuracy
ollama pull zephyr:3b     # Good balance
```

But for now, **Gemma 3 1B** is perfect for this grammar checking task.

## Project Structure

```
grammar-check-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── exceptions.py        # Custom exceptions
│   ├── ollama_client.py     # LLM communication
│   └── grammar.py           # Business logic
├── tests/
│   ├── __init__.py
│   └── test.py              # Basic functionality tests
├── evaluation_framework.py  # Comprehensive evaluation
├── run_evaluation.py        # Evaluation runner
├── run_tests.py            # Test runner
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## Design Choices

### **Architecture**
- **Modular Design**: Separated concerns (API, LLM, business logic)
- **Async First**: Non-blocking I/O for better performance
- **Type Safety**: Pydantic models for validation
- **Error Handling**: Custom exception hierarchy

### **LLM Integration**
- **Ollama**: Local LLM serving platform
- **Gemma 3 1B**: Lightweight, fast model
- **JSON Output**: Structured responses for easy parsing
- **Error Filtering**: Removes invalid responses

### **API Design**
- **RESTful**: Standard HTTP methods and status codes
- **JSON**: Simple, universal data format
- **CORS**: Cross-origin request support
- **Documentation**: Auto-generated API docs

## Challenges Faced

1. **LLM Response Formatting**: Ensuring consistent JSON output
2. **Error Handling**: Comprehensive exception management
3. **Performance**: Optimizing for local LLM constraints
4. **Testing**: Creating reliable evaluation framework

## Performance Considerations

- **Response Time**: 10-15 seconds typical (local LLM limitation)
- **Throughput**: ~4 requests/minute (model-dependent)
- **Memory Usage**: ~50-100MB (lightweight)
- **Scalability**: Can handle concurrent requests via async

## Future Improvements

1. **Caching**: Redis for response caching
2. **Background Processing**: Celery for async processing
3. **Model Optimization**: GPU acceleration
4. **Rate Limiting**: Request throttling
5. **Monitoring**: Prometheus metrics
6. **Load Balancing**: Multiple model instances

## Testing

### Basic Tests
```bash
python run_tests.py
```

### Comprehensive Evaluation
```bash
python run_evaluation.py
```

## License

MIT License - see LICENSE file for details. 