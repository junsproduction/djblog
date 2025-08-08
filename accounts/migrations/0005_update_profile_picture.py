from django.db import migrations
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_date_joined'),  # Replace with your last working migration
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=ProcessedImageField(
                blank=True,
                null=True,
                processors=[ResizeToFill(300, 300)],
                format='JPEG',
                options={'quality': 85},
                upload_to='profile_pics'
            ),
        ),
    ]