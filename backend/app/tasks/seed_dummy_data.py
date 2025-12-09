from datetime import datetime, timedelta, timezone

from ..db import SessionLocal
from ..models import Article


def seed_dummy_articles():
    db = SessionLocal()
    try:
        # Check if we already have some articles
        existing_count = db.query(Article).count()
        if existing_count > 0:
            print(f"DB already has {existing_count} articles; skipping seed.")
            return

        now = datetime.now(timezone.utc)

        samples = [
            Article(
                title="Cambodia explores national AI strategy",
                url="https://example.com/cambodia-ai-strategy",
                source="Backend Seed",
                published_at=now - timedelta(hours=1),
                summary="A sample summary about Cambodia's AI strategy to test the news digestor.",
                category="AI policy",
            ),
            Article(
                title="New breakthrough in large language models",
                url="https://example.com/llm-breakthrough",
                source="Backend Seed",
                published_at=now - timedelta(hours=2),
                summary="Researchers report improved efficiency in running 14B models on consumer hardware.",
                category="Research",
            ),
            Article(
                title="Automation workflows boost SME productivity",
                url="https://example.com/automation-sme",
                source="Backend Seed",
                published_at=now - timedelta(hours=3),
                summary="A case study on using Telegram bots and n8n for business automation.",
                category="Automation",
            ),
        ]

        db.add_all(samples)
        db.commit()
        print(f"Inserted {len(samples)} dummy articles.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_dummy_articles()
