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

# Generated by Django 3.2.6 on 2021-08-12 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20210811_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='publicity',
            field=models.IntegerField(choices=[('private', 0), ('public', 1)], default=0),
        ),
    ]
