#!/usr/bin/python3
import requests
import yaml


def get_clients_data():
    with open('clients.yml') as clients:
        targets = yaml.safe_load(clients)

    data = {}
    for target in targets['clients']:
        data[target["ip"]] = {}
        for var in target['vars']:
            url = f'https://{target["ip"]}:8080/get/{var}'
            try:
                r = requests.post(url=url, data={'token': target['token']})
            except requests.exceptions.InvalidSchema:
                r = None
            data[target["ip"]][var] = r.decode('utf-8')
    return data


if __name__ == '__main__':
    data = get_clients_data()
    print(data)
    # TODO: Add logic to parse data
