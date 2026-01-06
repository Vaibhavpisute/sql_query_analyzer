class CostCalculator:
    def estimate_cost(self, parsed, query: str):
        cost = 1.0
        q = query.upper()
        
        if 'SELECT' in q and 'WHERE' not in q:
            cost *= 10
        
        if ('DELETE' in q or 'UPDATE' in q) and 'WHERE' not in q:
            cost *= 20
        
        join_count = q.count('JOIN')
        cost *= (1 + join_count * 2)
        
        subquery_count = q.count('SELECT') - 1
        cost *= (1 + subquery_count * 1.5)
        
        if 'DISTINCT' in q:
            cost *= 1.5
        
        if 'ORDER BY' in q:
            cost *= 1.3
        
        if "LIKE '%" in q or 'LIKE "%' in q:
            cost *= 2
        
        return round(cost, 2)