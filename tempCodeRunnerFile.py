for document in data:
    collection.update_one({'_id': document['_id']}, {'$set': {'obtainMarks': -1}})