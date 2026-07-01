# Generated for skribble game flow API updates.

import datetime

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("back", "0015_skribbleroom_turn_started"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="last_seen",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="skribbleroom",
            name="host",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="hosted_skribble_rooms",
                to="back.userprofile",
            ),
        ),
        migrations.AddField(
            model_name="skribbleroom",
            name="max_rounds",
            field=models.IntegerField(
                default=3,
                validators=[django.core.validators.MinValueValidator(3)],
            ),
        ),
        migrations.AddField(
            model_name="skribbleroom",
            name="game_finished",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="skribbleroom",
            name="timer",
            field=models.DurationField(default=datetime.timedelta(seconds=80)),
        ),
    ]
