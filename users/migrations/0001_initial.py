# Generated by Django 4.1.1 on 2022-09-18 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, max_length=50, unique=True)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('signup_choices', models.CharField(choices=[('talent', 'Talent'), ('recruiter', 'Recruiter')], max_length=512)),
                ('cv', models.FileField(upload_to='cv')),
                ('jobType', models.CharField(choices=[('Digital & Design', 'Digital & Design'), ('Information Security / Cyber Security', 'Information Security / Cyber Security'), ('Project & Programme Management', 'Project & Programme Management'), ('Software Development & Engineering', 'Software Development & Engineering'), ('Technology Leadership', 'Technology Leadership'), ('Data & Analytics', 'Data & Analytics')], max_length=512)),
                ('jobContract', models.CharField(choices=[('All', 'All'), ('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time')], max_length=512)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
