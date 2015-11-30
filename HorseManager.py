import bson
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


def add_many_horses(horse_file_list, database):
    for h in horse_file_list:
        add_horse_from_file(h, database)


def find_horse(horse_id, database):
    client = MongoClient()
    db = client[database]

    horses = db.horses
    return horses.find_one({"_id": horse_id})


def modify_horse_doc(horse_id, database, key, new_value):
    client = MongoClient()
    db = client[database]

    db.horses.update_one(
        {"_id": horse_id},
        {
            "$set": {
                key: new_value
            },
            "$currentDate": {"lastModified": True}
        }
    )


def groupByCondition(database):
    # Show a list of pairs of list of horses and their condition

    mapper = bson.Code("""
        function () {
            emit(this.Condition,
            {"horses":
                [
                    this.Name
                ]
            });
        }
    """)

    reducer = bson.Code("""
        function(key, values) {
            var reduced = {"horses":[]};

            for (var i in values) {
                var inter = values[i];
                for (var j in inter.horses) {
                    reduced.horses.push(inter.horses[j]);
                }
            }
            return reduced;
        }
    """)

    client = MongoClient()
    db = client[database]
    results = db.horses.map_reduce(mapper, reducer, "sick_horses")

    return results.find()
