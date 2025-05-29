
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routine', '0002_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
