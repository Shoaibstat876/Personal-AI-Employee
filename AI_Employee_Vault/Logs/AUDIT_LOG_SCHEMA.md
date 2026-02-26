# Audit Log Schema (Gold Tier)

Format: JSONL (one JSON object per line)

Required fields:
- ts (ISO timestamp)
- tier
- event
- actor
- status
- details (object)
