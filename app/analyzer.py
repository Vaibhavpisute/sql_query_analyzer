import sqlparse
import hashlib
import time
import asyncio
from typing import List
from app.models import AnalysisResponse
from app.cost_calculator import CostCalculator
from app.optimizer import QueryOptimizer

class QueryAnalyzer:
    def __init__(self, cache):
        self.cache = cache
        self.cost_calc = CostCalculator()
        self.optimizer = QueryOptimizer()
    
    async def analyze(self, query: str, db_type: str):
        start_time = time.time()
        cache_key = self._get_cache_key(query, db_type)
        
        cached_result = self.cache.get(cache_key)
        if cached_result:
            cached_result['cached'] = True
            return AnalysisResponse(**cached_result)
        
        await asyncio.sleep(0.01)
        
        try:
            parsed = sqlparse.parse(query)[0]
        except Exception as e:
            raise ValueError(f"Invalid SQL query: {str(e)}")
        
        issues = self._detect_issues(parsed, query)
        cost = self.cost_calc.estimate_cost(parsed, query)
        tips = self.optimizer.suggest_optimizations(parsed, query, issues)
        
        result = {
            'query': query.strip(),
            'issues': issues,
            'cost_estimate': cost,
            'optimization_tips': tips,
            'execution_time_ms': round((time.time() - start_time) * 1000, 2),
            'cached': False
        }
        
        self.cache.set(cache_key, result)
        return AnalysisResponse(**result)
    
    def _get_cache_key(self, query: str, db_type: str):
        normalized = sqlparse.format(query, strip_comments=True).lower().strip()
        return hashlib.md5((normalized + db_type).encode()).hexdigest()
    
    def _detect_issues(self, parsed, query: str):
        issues = []
        q = query.upper()
        
        if ('DELETE' in q or 'UPDATE' in q) and 'WHERE' not in q:
            issues.append("⚠️ Missing WHERE clause - may affect ALL rows!")
        
        if 'SELECT *' in q:
            issues.append("⚠️ Using SELECT * - fetches unnecessary columns")
        
        if "LIKE '%" in query or 'LIKE "%' in query:
            issues.append("⚠️ Leading wildcard prevents index usage")
        
        join_count = q.count('JOIN')
        if join_count > 2:
            issues.append(f"⚠️ {join_count} JOINs detected - verify indexes exist")
        
        if q.count('SELECT') > 1:
            issues.append("⚠️ Contains subqueries - may be optimized with JOINs")
        
        if 'DISTINCT' in q:
            issues.append("⚠️ DISTINCT operation - adds sorting overhead")
        
        return issues