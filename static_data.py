class GasInfoClass(object):

    def __init__(self):
        self._boiler_room_and_no = [
            '地点A/1号锅炉',
            '地点A/2号锅炉',
            '地点A/3号锅炉',
            '地点B/1号锅炉',
            '地点C/1号锅炉'
        ]

    def _get_boiler_room_and_no(self):
        return self._boiler_room_and_no

    def get_gas_field_list(self):
        field_list = list()
        for record in self._boiler_room_and_no:
            location = str(record).split('/')[0]
            boiler_room = str(record).split('/')[1]
            record_set = (record, location + ' - ' + boiler_room, )
            field_list.append(record_set)
        return field_list

    def get_gas_url_list(self):
        return self._boiler_room_and_no


