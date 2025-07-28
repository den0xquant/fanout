# fanout

Experimental backend for exploring **fan-out** patterns in distributed systems.  
Based on the **Twitter timeline** example from _Designing Data-Intensive Applications_ by Martin Kleppmann.

## Goals

- Understand the **fan-out on write** and **fan-out on read** strategies.
- Reproduce and experiment with the Twitter-style timeline model.
- Practice working with denormalized data, eventual consistency, and feed generation.

## Stack

- **Python 3.13**
- **FastAPI** — API framework
- **PostgreSQL** — primary datastore
- **Redis** — fanout queue / pub-sub
- **Celery** — background fanout processing
- **Docker** — containerized setup

## Concepts implemented

- User follows / unfollows
- Users can post "tweets"
- Timeline is either:
  - **Fan-out on write**: push tweets to followers’ feeds at post time
  - **Fan-out on read**: fetch tweets from followees at read time
- Asynchronous background workers for fan-out processing

## Project Status

🧪 Work in progress — intended as a learning sandbox.  
Not production-ready. No tests.

## How to run

```bash
git clone https://github.com/den0xquant/fanout
cd fanout
docker-compose up --build
```

API available at http://localhost:8000/docs

## Related Reading

Designing Data-Intensive Applications — Martin Kleppmann
Chapters on data modeling, feed systems, and messaging patterns.

## License

MIT