import shortuuid
import json
from rest_framework import serializers

from benchmarks.models import PgBenchBenchmark, PgBenchResult, PgBenchStatement, PgBenchRunStatement, PgBenchLog


class PgBenchBenchmarkSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchBenchmark
		fields = '__all__'


class PgBenchResultSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchResult
		fields = '__all__'


class PgBenchStatementSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchStatement
		fields = '__all__'


class PgBenchRunStatementSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchRunStatement
		fields = '__all__'


class PgBenchLogSerializer(serializers.ModelSerializer):

	class Meta:
		model = PgBenchLog
		fields = '__all__'


class PgBenchAllResultsSerializer(serializers.ModelSerializer):

	benchmark_config = PgBenchBenchmarkSerializer(read_only=True)

	class Meta:
	 	model = PgBenchResult
	 	fields = ['tps', 'latency', 'benchmark_config']
