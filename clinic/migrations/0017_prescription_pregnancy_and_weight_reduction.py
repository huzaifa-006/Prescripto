from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0016_remove_prescription_diet_instructions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='pregnancy',
            field=models.BooleanField(default=False, verbose_name='Pregnancy'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='instruction_weight_reduction',
            field=models.BooleanField(default=False, verbose_name='Weight reduction advised'),
        ),
    ]
