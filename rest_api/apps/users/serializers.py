from django.contrib.auth.models import User
from rest_framework import serializers
from machines.models import Machine
from machines.serializers import MachineSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
	machines = serializers.HyperlinkedRelatedField(many=True, view_name='machine-detail', read_only=True)
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ('id', 'username', 'password', 'email', 'machines')

	'''
	def create(self, email, username, password):
		user = super(UserSerializer, self).create(email=self.normalize_email(email), username=username)
		user.set_password(password)
		user.save()
		return user
	'''

	def get_reports(self, obj):
		"""
		Number of reports
		"""
		machine_dict = []
		target_machines = Machine.objects.filter(owner=obj.id)
		serializer = MachineSerializer(target_machines, many=True)
		# print(serializer.data)
		for item in serializer.data:
			machine_dict.append(item['sn'])

		reports = TestRecord.objects.filter(test_machine__sn__in=machine_dict).count()

		return reports


class TokenSerializer(serializers.Serializer):
	token = serializers.CharField(max_length=255)



