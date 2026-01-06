import pytest
from app.analyzer import QueryAnalyzer
from app.cache.memory_cache import MemoryCache

@pytest.fixture
def analyzer():
    cache = MemoryCache(max_size=100, ttl_seconds=60)
    return QueryAnalyzer(cache)

@pytest.mark.asyncio
async def test_detect_missing_where(analyzer):
    query = "DELETE FROM users"
    result = await analyzer.analyze(query, "postgresql")
    assert any("WHERE" in issue for issue in result.issues)

@pytest.mark.asyncio
async def test_cache_works(analyzer):
    query = "SELECT id FROM users"
    result1 = await analyzer.analyze(query, "postgresql")
    assert result1.cached is False
    result2 = await analyzer.analyze(query, "postgresql")
    assert result2.cached is True