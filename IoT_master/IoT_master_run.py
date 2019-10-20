#!/usr/bin/python3
import urllib3
import yaml


def get_clients_data():
    agent = urllib3.PoolManager()
    with open('clients.yml') as clients:
        targets = yaml.safe_load(clients)

    data = {}
    for target in targets['clients']:
        data[target["ip"]] = {}
        for var in target['vars']:
            try:
                r = agent.request('GET', f'{target["ip"]}:8080/get/{var}').data
            except urllib3.exceptions.MaxRetryError:
                r = None
            data[target["ip"]][var] = r.decode('utf-8')
    return data


if __name__ == '__main__':
    data = get_clients_data()
    print(data)
    # TODO: Add logic to parse data
