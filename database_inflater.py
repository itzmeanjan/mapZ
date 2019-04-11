#!/usr/bin/python3


try:
    import psycopg2 as psql
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def push_into_table(db_name, username, password, table_name, data):
    # pushing dataset for a certain layer, is done here
    try:
        conn = psql.connect(database=db_name, user=username, password=password)
        cursor = conn.cursor()  # cursors give us API for executing SQL queries
        count = 0
        for feature_id, feature_name, outline in data:
            cursor.execute("insert into {} values ( %s, %s, st_geogfromtext(%s))".format(table_name),
                           (feature_id, feature_name, outline))
            count += 1
            if(not count % 100):
                # after every 100 push, we just commit the changes made
                conn.commit()
        conn.commit()  # final commit
        cursor.close()
        conn.close()  # connection to DB closed
    except psql.DatabaseError as e:
        print('[!]Error: {}'.format(str(e)))
        cursor.close()
        conn.close()
        return False
    except Exception as e:
        print('[!]Error: {}'.format(str(e)))
        cursor.close()
        conn.close()
        return False
    return True  # in case of success


def create_table(db_name, username, password, table_name):
    # first we need to create a database with postgis plugin enabled
    try:
        conn = psql.connect(database=db_name, user=username, password=password)
        cursor = conn.cursor()
        cursor.execute("drop table if exists {}".format(table_name))
        cursor.execute(
            "create table {} (feature_id varchar primary key, feature_name varchar not null, outline geography)".format(table_name))
        cursor.execute("create index {} on {} using gist( outline )".format(
            '{}_index'.format(table_name), table_name))
        conn.commit()  # committing changes made to DB
        cursor.close()
        conn.close()  # closed connection to DB
    except psql.DatabaseError as e:
        print('[!]Error: {}'.format(str(e)))
        cursor.close()
        conn.close()
        return False
    except Exception as e:
        print('[!]Error: {}'.format(str(e)))
        cursor.close()
        conn.close()
        return False
    return True  # in case of success


def inflate_into_db(db_name, username, password, data_set):
    # database inflation handler
    try:
        for key, value in data_set.items():
            if(create_table(db_name, username, password, 'world_features_level_{}'.format(key))):
                print(
                    '[+]Pushing into table -- `{}`'.format('world_features_level_{}'.format(key)))
                push_into_table(db_name, username, password,
                                'world_features_level_{}'.format(key), value)
            else:
                return False
    except Exception as e:
        print('[!]Error: {}'.format(str(e)))
        return False
    return True


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler.')
    exit(0)
