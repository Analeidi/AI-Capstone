import sqlite3
import json
from datetime import datetime
import time
import os
from os import path

timeframe = '2020-04-01'
sql_transaction = []
start_row = 0
cleanup = 1000000
num_non_english = 0

connection = sqlite3.connect('{}.db'.format(timeframe))
c = connection.cursor()

# blacklist any subreddits you don't want to include here, these subreddits are popular non-english ones
skip_subreddits = {"Austria", "argentina", "brasil", "brasilivre", "Bundesliga", "chile", "China_irl", "Colombia", "coronabr", "croatia", "de", "Denmark",
                   "espanol", "es", "france", "futbol", "greece", "hungary", "italy", "liberta", "mexico", "Pikabu", "Polska", "portugal", "PortugalVegan", "Quebec", "serbia",
                   "Suomi", "sweden", "uruguay"}


def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS parent_reply 
    (parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT, 
    comment TEXT, subreddit TEXT, unix INT, score INT)""")


def format_data(data):
    data = data.replace('\n', ' ').replace('\r', ' ').replace('"', "'").replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')\
        .replace('‘', "'").replace('’', "'").replace('“', "'").replace('”', "'")
    return data


def transaction_bldr(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 500:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except Exception as e:
                pass
                # print(e)
        connection.commit()
        sql_transaction = []


def sql_insert_replace_comment(commentid, parentid, parent, comment, subreddit, time, score):
    try:
        sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id =?;""".format(
            parentid, commentid, parent, comment, subreddit, int(time), score, parentid)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion', str(e))


def sql_insert_has_parent(commentid, parentid, parent, comment, subreddit, time, score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}","{}",{},{});""".format(
            parentid, commentid, parent, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion', str(e))


def sql_insert_no_parent(commentid, parentid, comment, subreddit, time, score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}",{},{});""".format(
            parentid, commentid, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion', str(e))


def acceptable(data):
    if len(data.split(' ')) > 100 or len(data) <= 1:
        return False
    elif len(data) > 300:
        return False
    elif data == '[deleted]':
        return False
    elif data == '[removed]':
        return False
    else:
        return True


def find_parent(pid):
    try:
        sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        # print(str(e))
        return False


def find_existing_score(pid):
    try:
        sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        # print(str(e))
        return False


def find_foreign_subs():
    c.execute("""CREATE TABLE IF NOT EXISTS parent_reply 
        (parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT, 
        comment TEXT, subreddit TEXT, unix INT, score INT, unicode INT)""")
    rows = 0

    with open("reddit data/RC_{}".format(timeframe), buffering=1000) as f:

        for row in f:
            rows += 1
            row = json.loads(row)
            parent_id = row['parent_id'][3:]
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            comment_id = row['id']

            unicode = 0  #
            if body:
                unicode = max([ord(i) for i in body])

            if unicode >= 191:
                parent_data = find_parent(parent_id)

                if parent_data:
                    try:
                        sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score, unicode) VALUES ("{}","{}","{}","{}","{}",{},{},{});""".format(
                            parent_id, comment_id, parent_data, body, subreddit, int(created_utc), score, unicode)
                        transaction_bldr(sql)
                    except Exception as e:
                        print('s0 insertion', str(e))
                else:
                    try:
                        sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score, unicode) VALUES ("{}","{}","{}","{}",{},{},{});""".format(
                            parent_id, comment_id, body, subreddit, int(created_utc), score, unicode)
                        transaction_bldr(sql)
                    except Exception as e:
                        print('s1 insertion', str(e))

            if rows % 100000 == 0:
                print("Total rows read: {:,}".format(rows))

    print(f"Rows read: {rows}")


def non_english(data):
    global num_non_english
    if subreddit in skip_subreddits:
        return True
    for char in data:
        if 191 <= ord(char) < 233 or 233 < ord(char):
            num_non_english += 1
            if num_non_english % 1000 == 0:
                print(f"Removed potentially non-english comment: {data}")
            return True
    return False


if __name__ == "__main__":
    print(os.getcwd())
    create_table()
    row_counter = 0
    paired_rows = 0
    insertions = 0
    skips = 0

    # The data below is being encoded with latin-1 not utf-8
    with open("reddit data/RC_{}".format(timeframe), buffering=1000) as f:
        start_t = time.perf_counter()

        for row in f:
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id'][3:]
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            comment_id = row['id']

            if acceptable(body) and score >= 3:
                if non_english(body):
                    skips += 1
                    continue

                existing_comment_score = find_existing_score(parent_id)
                parent_data = find_parent(parent_id)

                if existing_comment_score and score > existing_comment_score:
                    sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
                else:
                    if parent_data:
                        sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
                        paired_rows += 1
                        insertions += 1
                    elif len(body) >= 10 and len(body.split()) >= 3:
                        sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score)
                        insertions += 1

            if row_counter % 100000 == 0:
                print("Total rows read: {:,}\t Paired rows: {:,}\t Time: {}".format(row_counter, paired_rows, str(datetime.now())))

        end_t = time.perf_counter()

        print(f"SUMMARY FOR {timeframe}")
        print(f"Elapsed time: {end_t - start_t:.2f} seconds")
        pair_percent = round(paired_rows / row_counter * 100, 2)
        print(f"Total comments read: {row_counter:,}, Comments inserted: {insertions:,}, Comment pairs: {paired_rows:,}, Skips: {skips:,}")
        print(f"Percent inserted: {insertions / row_counter:.2%}, Percent paired: {paired_rows / insertions:.2%}")
        file_path = path.join(os.getcwd(), "reddit data/RC_{}".format(timeframe))
        size = os.stat(file_path).st_size  # size in bytes
        size = size / 1024  # convert to KB
        print(f"Comments per KB: {row_counter / size:.3f}, Comment pairs per KB: {paired_rows / size:.3f}")
