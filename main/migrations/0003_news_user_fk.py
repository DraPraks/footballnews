from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

	dependencies = [
		("main", "0002_create_missing_news_table"),
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
	]

	operations = [
		migrations.AddField(
			model_name='news',
			name='user',
			field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
		),
	]

