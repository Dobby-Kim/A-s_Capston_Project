import json

psj_final = [0, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 1, 0, 0, 1, 0, 1]


def list_js(name, data):
    space = {}
    space['name'] = name
    space['data'] = data
    list_json = json.dumps(space, ensure_ascii=True)
    return list_json


def list_sep_js(name, data):
    space = {}
    seats = {}
    space['name'] = name

    for i in range(len(data)):
        status = ''
        if data[i] == 0:
            status = 'empty'
        elif data[i] == 1:
            status = 'reserved'
        elif data[i] == 2:
            status = 'occupied'
        seats[f"{i+1}"] = status
    space['data'] = seats

    list_json = json.dumps(space, ensure_ascii=True)
    return list_json


def list_db_js(name, data):
    space = {}
    seats = {}

    for i in range(len(data)):
        status = ''
        if data[i] == 0:
            status = True
        else:
            status = False
        seats[f"seat{i+1}"] = status
    space[name] = seats

    list_json = json.dumps(space, ensure_ascii=True)
    return list_json


print(list_db_js('psj', psj_final))