from django.db import models
import shortuuid
import hashlib
from django.contrib.postgres.fields.jsonb import JSONField


class LinuxInfo(models.Model):

	# do not insert every time, only check if there are duplicates

	linux_info_id = models.AutoField(primary_key=True)

	cpu_brand = models.CharField(max_length=100, null=True)
	hz = models.CharField(max_length=100, null=True)
	cpu_cores = models.IntegerField(null=True)
	cpu_times = JSONField(null=True)

	memory = JSONField(null=True)
	swap = JSONField(null=True)
	mounts = JSONField(null=True)
	io = JSONField(null=True)

	sysctl = models.TextField(null=True)


class Compiler(models.Model):

	compiler_id = models.AutoField(primary_key=True)
	compiler = models.CharField(max_length=100, null=False, unique=True)