# Generated by Django 5.1.7 on 2025-04-10 20:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Investment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "initial_amount",
                    models.FloatField(verbose_name="Initial Investment"),
                ),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "profit_percentage",
                    models.FloatField(
                        blank=True, null=True, verbose_name="Profit Percentage"
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Partner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("amount", models.FloatField(verbose_name="Partner Investment")),
                ("profit_share", models.FloatField(verbose_name="Profit Share (%)")),
                (
                    "investment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="partners",
                        to="users.investment",
                    ),
                ),
            ],
        ),
    ]
