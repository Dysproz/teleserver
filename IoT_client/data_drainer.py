import yaml


def get_data_for_variable(var):
    with open('/var/lib/teleserver_IoT/data.yml', 'r') as data_file:
        current_data = yaml.safe_load(data_file)
    if var in current_data:
        return current_data[var]
    else:
        return None


def set_data_for_variable(data):
    with open('/var/lib/teleserver_IoT/data.yml', 'r') as data_file:
        current_data = yaml.safe_load(data_file)
    current_data.update(data)
    with open('/var/lib/teleserver_IoT/data.yml', 'w') as data_file:
        yaml.dump(data_file)
