import pymongo
import streamlit as st

user_name = st.secrets["db_username"]
user_pass = st.secrets["db_password"]
def init_connection():
    return pymongo.MongoClient("mongodb+srv://"+user_name+":"+user_pass+"@cluster0.sb2kivl.mongodb.net/?retryWrites=true&w=majority")
set_client = init_connection()

def get_data_from_collection(param_client,param_db,param_collection,param_query='ALL'):
    data = []
    get_db = param_client[param_db]
    get_collection = get_db[param_collection]
    if param_query == "ALL":
        for deta_all in get_collection.find():
          data.append(deta_all)
    else:
        filter_query = get_collection.find(param_query)
        for deta_filter in filter_query:
            data.append(deta_filter)
    return data

def insert_data_into_collection(param_client,param_db,param_collection,param_data_to_insert):
    data = []
    try:
        get_db = param_client[param_db]
        get_collection = get_db[param_collection]
        existing_data = get_collection.find_one(param_data_to_insert)
        if existing_data:
            print("Data already exists:", existing_data)
            # Decide what to do if data already exists, e.g., update or skip insertion
        else:
            x = get_collection.insert_one(param_data_to_insert)
        return "insert data successfully"
    except Exception as e:
        return "error inserting data : "+str(e)

def delete_data_into_collection(param_client,param_db,param_collection,param_data_to_delete):
    data = []
    try:
        get_db = param_client[param_db]
        get_collection = get_db[param_collection]
        x = get_collection.delete_one(param_data_to_delete)
        return "delete data successfully"
    except Exception as e:
        return "error deleting data : "+str(e)

def delete_multiple_data_into_collection(param_client,param_db,param_collection,param_data_to_delete):
    data = []
    try:
        get_db = param_client[param_db]
        get_collection = get_db[param_collection]
        x = get_collection.delete_many(param_data_to_delete)
        return "delete data successfully"
    except Exception as e:
        return "error deleting data : "+str(e)

def create_collection_if_not_exists(param_client,param_db,param_collection):
    try:
        get_db = param_client[param_db]
        get_collection_list = get_db.list_collection_names()
        if param_collection in get_collection_list:
            print("collection exists.")
        else:
            print(param_collection + " does not exist")
            create_collection = get_db.create_collection(param_collection)
            check_collection_list = get_db.list_collection_names()
            print(get_collection_list)
            if param_collection in check_collection_list:
                print(param_collection +" Created")
    except Exception as e:
        return "error creating/checking Collections : "+str(e)
'''         
print(delete_multiple_data_into_collection(set_client,"sample_guides","planets",{"name": "Test4"}))
print(get_data_from_collection(set_client,"sample_guides","planets",{"name": "Test4"}))

print(get_data_from_collection(set_client,"client_services","year_2024"))


print(delete_data_into_collection(set_client,"sample_guides","planets",{"name": "Test4"}))
for coll in mydb.list_collection_names():
    print(coll)
'''
