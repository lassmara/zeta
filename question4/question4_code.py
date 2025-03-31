import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests_per_second):
        self.max_requests_per_second = max_requests_per_second
        self.user_requests = defaultdict(list)  # Store request timestamps by user

    def _cleanup_old_requests(self, user_id):
        """Remove requests older than 1 second"""
        current_time = time.time()
        self.user_requests[user_id] = [t for t in self.user_requests[user_id] if current_time - t < 1]

    def is_rate_limited(self, user_id):
        """Check if the user is rate-limited"""
        # Clean up requests older than 1 second
        self._cleanup_old_requests(user_id)

        if len(self.user_requests[user_id]) < self.max_requests_per_second:
            # Allow the request and add the timestamp to the list
            self.user_requests[user_id].append(time.time())
            return False  # No rate limit applied
        else:
            return True  # Rate limit applied

# Example usage
rate_limiter = RateLimiter(max_requests_per_second=5)

user_id = "user_123"

# Simulate multiple requests from the same user
for _ in range(10):  # Simulate 10 requests in a short period
    if rate_limiter.is_rate_limited(user_id):
        print("Rate limit exceeded!")
    else:
        print("Request allowed.")
    time.sleep(0.1)  # Simulating small time gaps between requests
