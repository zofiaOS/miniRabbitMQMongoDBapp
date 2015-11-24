from pymongo import MongoClient


def _add_horse(horse, database):
    client = MongoClient()
    db = client[database]

    horses = db.horses
    horses.insert_one(horse)


def add_horse_from_file(horse_file, database):
    horse = {}
    try:
        with open(horse_file, 'r') as f:
            for line in f:
                # Ignore empty lines
                if line.strip():
                    try:
                        key, value = line.split()
                    except ValueError:
                        print("Data should be in key value format")
                        raise
                    horse[key] = value
    except IOError:
        print("Invalid horse file directory: {}".format(horse_file))
        raise
    _add_horse(horse, database)


def find_horse(horse_id, database):
    client = MongoClient()
    db = client[database]

    horses = db.horses
    return horses.find_one({"_id": horse_id})
