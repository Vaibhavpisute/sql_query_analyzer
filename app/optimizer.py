from typing import List

class QueryOptimizer:
    def suggest_optimizations(self, parsed, query: str, issues: List[str]):
        tips = []
        q = query.upper()
        
        if "SELECT *" in q:
            tips.append("Replace SELECT * with specific columns")
        
        if "WHERE" not in q and "SELECT" in q:
            tips.append("Add WHERE clause to filter data")
        
        if "JOIN" in q:
            tips.append("Ensure JOIN columns have indexes")
        
        if "LIKE '%" in q or 'LIKE "%' in q:
            tips.append("Avoid leading wildcards in LIKE")
        
        if q.count('SELECT') > 1:
            tips.append("Replace subqueries with JOINs")
        
        tips.append("Run EXPLAIN ANALYZE to see execution plan")
        
        return tips[:5]