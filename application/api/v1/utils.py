def list_iterator(list):
    for i in list:
        if i is None or not i:
            return False
def get_item_by_key(key,dict_):
    if key in dict_:
        return dict_[key]
    return False