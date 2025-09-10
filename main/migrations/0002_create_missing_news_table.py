from django.db import migrations


CREATE_NEWS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS main_news (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(20) NOT NULL,
    thumbnail VARCHAR(200) NULL,
    news_views INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_featured BOOLEAN NOT NULL DEFAULT FALSE
);
"""

DROP_NEWS_TABLE_SQL = "DROP TABLE IF EXISTS main_news;"


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(CREATE_NEWS_TABLE_SQL, reverse_sql=DROP_NEWS_TABLE_SQL),
    ]
