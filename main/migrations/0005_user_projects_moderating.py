#region PREAMBLE
#
#    This is the server-side of the issue-tracker software.
#    Copyright (C) 2021 waleed177 <potatoxel@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, version 3 of the
#    License only.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#endregion

# Generated by Django 3.2.4 on 2021-08-07 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_issuelabel_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='projects_moderating',
            field=models.ManyToManyField(related_name='moderators', to='main.Project'),
        ),
    ]
