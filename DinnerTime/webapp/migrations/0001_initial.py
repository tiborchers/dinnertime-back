# Generated by Django 2.1.4 on 2019-08-31 01:04

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('photo', models.CharField(blank=True, max_length=200, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['username'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('logo', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CategoryPerDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('photo', models.CharField(blank=True, max_length=200, null=True)),
                ('generalIngredient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='webapp.Ingredient')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IngredientRequired',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('measure', models.CharField(choices=[('Gramos', 'g'), ('Kilogramos', 'kg'), ('Tazas', 'taza'), ('Cucharas', 'cuchara'), ('Cucharitas', 'cucharita'), ('Litros', 'lts'), ('Partes', 'partes'), ('Unidades', 'cantidad'), ('Al gusto', 'al_gusto'), ('Otro', 'other')], max_length=50)),
                ('optional', models.BooleanField(default=False)),
                ('customMeasure', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Ingredients required',
                'ordering': ['ingredient', 'recipe'],
            },
        ),
        migrations.CreateModel(
            name='IngredientRequiredAlternative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('measure', models.CharField(choices=[('Gramos', 'g'), ('Kilogramos', 'kg'), ('Tazas', 'taza'), ('Cucharas', 'cuchara'), ('Cucharitas', 'cucharita'), ('Litros', 'lts'), ('Partes', 'partes'), ('Unidades', 'cantidad'), ('Al gusto', 'al_gusto'), ('Otro', 'other')], max_length=50)),
                ('optional', models.BooleanField(default=False)),
                ('customMeasure', models.CharField(blank=True, max_length=200, null=True)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Ingredient')),
                ('originalIngredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.IngredientRequired')),
            ],
            options={
                'ordering': ['originalIngredient', 'ingredient'],
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('days', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('video_url', models.CharField(blank=True, max_length=100, null=True)),
                ('photo', models.CharField(blank=True, max_length=200, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(to='webapp.Category')),
                ('ingredients', models.ManyToManyField(through='webapp.IngredientRequired', to='webapp.Ingredient')),
            ],
            options={
                'ordering': ['name', 'author'],
            },
        ),
        migrations.CreateModel(
            name='RecipeForDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RefrigeratorContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('measure', models.CharField(choices=[('Gramos', 'g'), ('Kilogramos', 'kg'), ('Tazas', 'taza'), ('Cucharas', 'cuchara'), ('Cucharitas', 'cucharita'), ('Litros', 'lts'), ('Partes', 'partes'), ('Unidades', 'cantidad'), ('Al gusto', 'al_gusto'), ('Otro', 'other')], max_length=50)),
                ('customMeasure', models.CharField(blank=True, max_length=200, null=True)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('optional', models.BooleanField(default=False)),
                ('photo', models.CharField(blank=True, max_length=200, null=True)),
                ('order', models.IntegerField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Recipe')),
            ],
            options={
                'ordering': ['recipe', 'order'],
            },
        ),
        migrations.CreateModel(
            name='Refrigerator',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('photo', models.CharField(blank=True, max_length=200, null=True)),
                ('menu', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='webapp.Menu')),
            ],
        ),
        migrations.AddField(
            model_name='recipeforday',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Menu'),
        ),
        migrations.AddField(
            model_name='recipeforday',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Recipe'),
        ),
        migrations.AddField(
            model_name='menu',
            name='categories',
            field=models.ManyToManyField(through='webapp.CategoryPerDay', to='webapp.Category'),
        ),
        migrations.AddField(
            model_name='menu',
            name='recipes',
            field=models.ManyToManyField(through='webapp.RecipeForDay', to='webapp.Recipe'),
        ),
        migrations.AddField(
            model_name='ingredientrequired',
            name='alternatives',
            field=models.ManyToManyField(related_name='alternative_ingredients', through='webapp.IngredientRequiredAlternative', to='webapp.Ingredient'),
        ),
        migrations.AddField(
            model_name='ingredientrequired',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='webapp.Ingredient'),
        ),
        migrations.AddField(
            model_name='ingredientrequired',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Recipe'),
        ),
        migrations.AddField(
            model_name='categoryperday',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Menu'),
        ),
        migrations.AlterUniqueTogether(
            name='step',
            unique_together={('recipe', 'order')},
        ),
        migrations.AddField(
            model_name='refrigeratorcontent',
            name='refrigerator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Refrigerator'),
        ),
        migrations.AddField(
            model_name='refrigerator',
            name='content',
            field=models.ManyToManyField(through='webapp.RefrigeratorContent', to='webapp.Ingredient'),
        ),
        migrations.AddField(
            model_name='refrigerator',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='refrigerator',
            name='recipes',
            field=models.ManyToManyField(to='webapp.Recipe'),
        ),
        migrations.AlterUniqueTogether(
            name='ingredientrequiredalternative',
            unique_together={('originalIngredient', 'ingredient')},
        ),
        migrations.AlterUniqueTogether(
            name='ingredientrequired',
            unique_together={('ingredient', 'recipe')},
        ),
    ]
