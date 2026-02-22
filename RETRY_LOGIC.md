# RETRY_LOGIC (Gold)

This repo includes a minimal retry layer for transient failures.

## Files
- scripts/retry.py
- scripts/retry_demo.py

## Proof
Preferred:
- python -m scripts.retry_demo

Also supported:
- python scripts/retry_demo.py

Expected output:
- retry_demo_result= OK
- retry_demo_attempts= 3
