import os
from os.path import join, dirname
from dotenv import load_dotenv
import pydgraph
import sqlite3

import schema
import sql

# setup dotenv
def setup_dotenv():
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

# setup dgraph schema
def setup_dgraph(client):
    print('apply schema:')
    print(schema.get_schema())
    op = pydgraph.Operation(schema=schema.get_schema())
    client.alter(op)

def clear_dgraph(client):
    op = pydgraph.Operation(drop_all=True)
    client.alter(op)

if __name__ == '__main__':
    setup_dotenv()

    DGRAPTH_ENDPOINT = os.environ.get("DGRAPTH_ENDPOINT")
    print('connect dgraph: ', DGRAPTH_ENDPOINT)
    client_stub = pydgraph.DgraphClientStub(DGRAPTH_ENDPOINT)
    client = pydgraph.DgraphClient(client_stub)

    clear_dgraph(client)
    setup_dgraph(client)

    SQLITE_DB = os.environ.get("DB_PATH")
    print('read sqlite db: ', SQLITE_DB)
    con = sqlite3.connect(SQLITE_DB)
    cur = con.cursor()


    oid_to_uid = {}
    try:
        # insert objects
        print('insert objects')
        for row in cur.execute(sql.OBJECTS_SQL):
            obj = {
                'id': row[0],
                'external_id': row[1],
                'name': row[3],
                'dgraph.type': 'object'
            }
            txn = client.txn()
            res = txn.mutate(set_obj=obj, commit_now=True)
            for v in res.uids.values():
                oid_to_uid[row[0]] = v

        # update children
        print('update children')
        for row in cur.execute(sql.CHILD_SQL):
            if (not row[0] in oid_to_uid) or (not row[1] in oid_to_uid):
                print("ERROR: Not found uid on update children. :", row[0], ":", row[1])
                continue

            obj_uid = oid_to_uid[row[0]]
            child_uid = oid_to_uid[row[1]]
            nquad = '<{}> <children> <{}> .'.format(obj_uid, child_uid)
            txn = client.txn()
            txn.mutate(set_nquads=nquad, commit_now=True)

        # update parent
        print('update parent')
        for row in cur.execute(sql.PARRENT_SQL):
            if (not row[0] in oid_to_uid) or (not row[1] in oid_to_uid):
                print("ERROR: Not found uid on update parent. :", row[0], ":", row[1])
                continue

            obj_uid = oid_to_uid[row[0]]
            parent_uid = oid_to_uid[row[1]]
            nquad = '<{}> <parent> <{}> .'.format(obj_uid, parent_uid)
            txn = client.txn()
            txn.mutate(set_nquads=nquad, commit_now=True)

        # update instanceof
        print('update instanceof')
        for row in cur.execute(sql.INSTANCEOF_SQL):
            if (not row[0] in oid_to_uid) or (not row[1] in oid_to_uid):
                print("ERROR: Not found uid on update instanceof. :", row[0], ":", row[1])
                continue

            obj_uid = oid_to_uid[row[0]]
            parent_uid = oid_to_uid[row[1]]
            nquad = '<{}> <instanceof> <{}> .'.format(obj_uid, parent_uid)
            txn = client.txn()
            txn.mutate(set_nquads=nquad, commit_now=True)

        # insert attributes
        print('insert attributes')
        for row in cur.execute(sql.ATTRIBUTES_SQL):
            if not row[0] in oid_to_uid:
                print("ERROR: Not found uid on insert attribute. :", row[0])
                continue

            obj = {
                'dgraph.type': 'attribute',
                'name': row[1],
                'category': row[2],
                'data_type': row[3],
                'data_type_context': row[4],
                'display_name': row[5],
                'flags': row[6],
                'display_precision': row[7],
                'value': row[8]
            }
            txn = client.txn()
            res = txn.mutate(set_obj=obj)
            attr_uid = ''
            for v in res.uids.values():
                attr_uid = v

            obj_uid = oid_to_uid[row[0]]
            nquad = '<{}> <attributes> <{}> .'.format(obj_uid, attr_uid)
            txn.mutate(set_nquads=nquad, commit_now=True)
    finally:
        con.close()
