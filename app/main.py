from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import List
from app.models import QueryRequest, AnalysisResponse
from app.analyzer import QueryAnalyzer
from app.cache.memory_cache import MemoryCache

app = FastAPI(title="SQL Query Cost Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = MemoryCache(max_size=1000, ttl_seconds=3600)
analyzer = QueryAnalyzer(cache)

@app.get("/")
async def root():
    return {"message": "SQL Query Cost Analyzer API", "status": "running"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_query(request: QueryRequest):
    try:
        result = await analyzer.analyze(request.query, request.database_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/analyze/batch", response_model=List[AnalysisResponse])
async def analyze_batch(requests: List[QueryRequest]):
    if len(requests) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 queries per batch")
    
    tasks = [analyzer.analyze(req.query, req.database_type) for req in requests]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    valid_results = []
    for result in results:
        if not isinstance(result, Exception):
            valid_results.append(result)
    
    return valid_results

@app.get("/health")
async def health_check():
    return {"status": "healthy", "cache_size": len(cache.cache)}