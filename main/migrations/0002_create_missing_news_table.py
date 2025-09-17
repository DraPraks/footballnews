from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration previously attempted to create the main_news table with raw SQL
    using PostgreSQL-specific types. It's now a no-op because 0001 already creates
    the News model (and table) in a backend-agnostic way.
    """

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(migrations.RunPython.noop, migrations.RunPython.noop),
    ]
