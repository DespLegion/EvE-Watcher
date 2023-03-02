import json
import requests as req
import os


class SystemsListUpdate:
    def __init__(self, source='tranquility'):
        self.base_url = 'https://esi.evetech.net/latest/'
        self.source = source
        self.base_dir = 'data/esi_data/'

    def start(self):
        return self.get_all_systems_ids()

    def get_all_systems_ids(self):
        data = req.get(f'{self.base_url}universe/systems/?datasource={self.source}')
        dict_data = data.json()
        return self.systems_names_update(dict_data)

    def systems_names_update(self, systems_ids):
        i = 0
        for system_id in systems_ids:
            files = os.listdir(self.base_dir)
            sys_data = req.get(f'{self.base_url}universe/systems/{system_id}/?datasource={self.source}')
            if sys_data.status_code == 200:
                sys_dict = sys_data.json()
                sys_name = sys_dict['name']
            else:
                print(f'ERROR - {sys_data.status_code}')
                return f'ERROR - {sys_data.status_code}'
            if 'systems.json' in files:
                with open(f'{self.base_dir}/systems_rev.json', 'r') as sys_data_file:
                    content = json.load(sys_data_file)
                with open(f'{self.base_dir}/systems_rev.json', 'w') as sys_data_file:
                    content[sys_name] = system_id
                    json.dump(content, sys_data_file, indent=2)
            else:
                with open(f'{self.base_dir}/systems_rev.json', 'w') as sys_data_file:
                    json_dict = {sys_name: system_id}
                    json.dump(json_dict, sys_data_file, indent=2)
            i += 1
            print(f'Обновлено {i} из {len(systems_ids)}')
        return f'Обновление успешно завершено. Обновлено {i} систем'
