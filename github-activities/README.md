# GitHub Activity Tracker

A simple command-line tool to fetch, display, and cache GitHub activities for a given user. The tracker supports caching using Redis to improve performance by reducing unnecessary API calls.

## Features

- **Fetch**: Fetch recent GitHub activities for a given user.
- **Display**: Display stored GitHub activities in a colorful format.
- **Cache**: Store activities in a Redis cache for faster retrieval.

## Prerequisites

- Python 3.x
- Redis (for caching)
- `requests`, `argparse`, `colorama`, and `redis-py` libraries

### Install Redis

If you don’t have Redis installed, follow the instructions on [Redis installation](https://redis.io/docs/getting-started/) for your system.

### Install Python Dependencies

Install required libraries using `pip`:

```bash
pip install requests redis colorama
```

# Usage

1. Fetch GitHub Activities
   Fetch the activities for the specified GitHub user and save them to a JSON file.

```bash
python github-tracker.py <username> fetch
```

2. Display Stored GitHub Activities
   Show the stored activities for the specified user, if available.

```bash
python github-tracker.py <username> display
```

3. Cache Activities
   Activities are automatically cached in Redis for 300 seconds (5 minutes). Cache will be used if it's not expired.

Example Workflow

# Fetch GitHub activities and save them to a file

```bash
python github-tracker.py johndoe fetch
```

# Display the stored activities for the user

```bash
python github-tracker.py johndoe display
```
