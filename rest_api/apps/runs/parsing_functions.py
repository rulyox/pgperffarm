import pandas
import csv
import json
import hashlib
import io
import re
import copy

from postgres.models import PostgresSettingsSet
from postgres.serializers import PostgresSettingsSerializer
from benchmarks.models import PgBenchBenchmark
from benchmarks.serializers import PgBenchResultSerializer, PgBenchStatementSerializer, PgBenchRunStatementSerializer
from systems.models import KnownSysctlInfo


def ParseSysctl(raw_data):

	data = json.loads(raw_data)
	json_dict = {}
	known_sysctl = KnownSysctlInfo.objects.filter(sysctl_id=1).get()

	for parameter in known_sysctl.sysctl:

		if parameter in data:
			json_dict.update({parameter: data[parameter]})
		
	if json_dict == {}:
		return 'known sysctl info not found'

	else:
		return json_dict


def Hash(json_data):

	hash_value = hashlib.sha256(json.dumps(json_data).encode('utf-8'))
	return hash_value.hexdigest()


def ParseLinuxData(json_data):

	if ('brand' in json_data['system']['cpu']['information']):
		brand = json_data['system']['cpu']['information']['brand']

	else:
		brand = json_data['system']['cpu']['information']['brand_raw']

	if ('hz_actual_raw' in json_data['system']['cpu']['information']):
		hz = json_data['system']['cpu']['information']['hz_actual_raw'][0]

	else:
		hz = json_data['system']['cpu']['information']['hz_actual'][0]

	sysctl = ParseSysctl(json_data['sysctl_log'])

	result = {
		'cpu_brand': brand,
		'hz': hz,
		'cpu_cores': json_data['system']['cpu']['information']['count'],
		'total_memory': json_data['system']['memory']['virtual']['total'],
		'total_swap': json_data['system']['memory']['swap']['total'],
		'mounts_hash': Hash(json_data['system']['memory']['mounts']),
		'mounts': json_data['system']['memory']['mounts'],
		'sysctl': sysctl,
		'sysctl_hash': Hash(sysctl)
	}

	return result


def GetHash(postgres_settings):

	reader = csv.DictReader(io.StringIO(postgres_settings))
	postgres_settings_json = json.dumps(list(reader))

	data_frame = pandas.read_json(postgres_settings_json)

	data_frame.query('source != "default" and source != "client"', inplace = True)

	hash_string = str(data_frame.values.flatten())

	hash_value = hashlib.sha256((hash_string.encode('utf-8')))

	return hash_value.hexdigest(), data_frame


def AddPostgresSettings(hash_value, settings):

	settings_set = PostgresSettingsSet.objects.filter(settings_sha256=hash_value).get()

	settings_set_id = settings_set.postgres_settings_set_id

	# now parsing all settings
	for index, row in settings.iterrows():
		name = row['name']
		unit = row['source']
		value = row['setting']

		settings_object = {
		'db_settings_id': settings_set_id,
		'setting_name': name,
		'setting_unit': unit,
		'setting_value': value
		}

		serializer = PostgresSettingsSerializer(data=settings_object)

		if serializer.is_valid():
				serializer.save()

		else:
			raise RuntimeError('Invalid Postgres settings.')


def ParsePgBenchOptions(item, clients):

	result = {
		'clients': clients,
		'scale': item['scale'],
		'duration': item['duration'],
		'read_only': item['read_only']
	}

	return result


def ParsePgBenchStatementLatencies(statement_latencies, pgbench_result_id): 

	# extract the nonempty statements
	statements = statement_latencies.split("\n")
	statements = list(filter(None, statements))

	line_id = 0

	for statement in statements:
		latency = re.findall('\d+\.\d+', statement)[0]
		text = (statement.split(latency)[1]).strip()
		
		pgbench_statement = {'statement': text}

		statement_serializer = PgBenchStatementSerializer(data=pgbench_statement)

		if statement_serializer.is_valid():
				statement_valid = statement_serializer.save()

				data = {
					'latency': latency,
					'line_id': line_id,
					'pgbench_result_id': pgbench_result_id,
					'result_id': statement_valid.pgbench_statement_id
					}

				run_statement_serializer = PgBenchRunStatementSerializer(data=data)

				if run_statement_serializer.is_valid():
					run_statement_serializer.save()
					line_id += 1

				else:
					raise RuntimeError('Invalid PgBench run statement data.')

		else:
			raise RuntimeError('Invalid PgBench statement data.')



def ParsePgBenchResults(item, run_id):

	json = item['iterations']

	for client in item['clients']:

		for result in json:

			if int(result['clients']) == client:

				data = copy.deepcopy(result)

				pgbench_config = PgBenchBenchmark.objects.filter(clients=data['clients'], scale=item['scale'], duration=item['duration'], read_only=item['read_only']).get()

				# remove statement latencies
				statement_latencies = data['statement_latencies']

				data.pop('statement_latencies')
				data.pop('clients')
				data.pop('threads')

				data['run_id'] = run_id
				data['benchmark_config'] = pgbench_config.pgbench_benchmark_id

				result_serializer = PgBenchResultSerializer(data=data)

				if result_serializer.is_valid():
						result_valid = result_serializer.save()

						ParsePgBenchStatementLatencies(statement_latencies, result_valid.pgbench_result_id)

				else:
					raise RuntimeError('Invalid PgBench data.')


