from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="perfil",
            name="es_comprador",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="perfil",
            name="es_vendedor",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="perfil",
            name="user",
            field=models.OneToOneField(
                on_delete=models.deletion.CASCADE,
                related_name="perfil",
                to="auth.user",
            ),
        ),
        migrations.RemoveField(
            model_name="perfil",
            name="rol",
        ),
    ]
