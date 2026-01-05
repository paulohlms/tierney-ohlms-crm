"""
Performance monitoring and optimization utilities.

Provides:
- Request timing middleware
- Database query timing
- Performance logging
- Simple in-memory cache with TTL
"""
import time
import logging
from typing import Dict, Optional, Any
from functools import wraps
from datetime import datetime, timedelta
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)

# Simple in-memory cache with TTL
_cache: Dict[str, tuple[Any, datetime]] = {}
_cache_ttl = timedelta(minutes=5)  # 5 minute cache TTL


def get_cache(key: str) -> Optional[Any]:
    """Get value from cache if not expired."""
    if key in _cache:
        value, expiry = _cache[key]
        if datetime.now() < expiry:
            return value
        else:
            del _cache[key]
    return None


def set_cache(key: str, value: Any, ttl: Optional[timedelta] = None):
    """Set value in cache with TTL."""
    ttl = ttl or _cache_ttl
    expiry = datetime.now() + ttl
    _cache[key] = (value, expiry)


def clear_cache(pattern: Optional[str] = None):
    """Clear cache entries matching pattern, or all if None."""
    if pattern:
        keys_to_delete = [k for k in _cache.keys() if pattern in k]
        for key in keys_to_delete:
            del _cache[key]
    else:
        _cache.clear()


class PerformanceMiddleware(BaseHTTPMiddleware):
    """Middleware to measure and log request performance."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.perf_counter() - start_time
        duration_ms = duration * 1000
        
        # Log slow requests
        if duration_ms > 500:  # Log requests taking more than 500ms
            logger.warning(
                f"[PERF] Slow request: {request.method} {request.url.path} "
                f"took {duration_ms:.2f}ms"
            )
        elif duration_ms > 100:  # Info for requests over 100ms
            logger.info(
                f"[PERF] Request: {request.method} {request.url.path} "
                f"took {duration_ms:.2f}ms"
            )
        
        # Add timing header
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
        
        return response


def time_db_query(func):
    """Decorator to time database queries."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            duration = (time.perf_counter() - start) * 1000
            if duration > 100:  # Log slow queries
                logger.warning(f"[PERF] Slow query {func.__name__}: {duration:.2f}ms")
            return result
        except Exception as e:
            duration = (time.perf_counter() - start) * 1000
            logger.error(f"[PERF] Query {func.__name__} failed after {duration:.2f}ms: {e}")
            raise
    return wrapper


def time_sync_db_query(func):
    """Decorator to time synchronous database queries."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration = (time.perf_counter() - start) * 1000
            if duration > 100:  # Log slow queries
                logger.warning(f"[PERF] Slow sync query {func.__name__}: {duration:.2f}ms")
            return result
        except Exception as e:
            duration = (time.perf_counter() - start) * 1000
            logger.error(f"[PERF] Sync query {func.__name__} failed after {duration:.2f}ms: {e}")
            raise
    return wrapper

