import sqlite3
import pandas as pd
import time

timeframes = ['2020-04-01']

start_t = time.perf_counter()

for timeframe in timeframes:
    connection = sqlite3.connect('{}.db'.format(timeframe))
    c = connection.cursor()
    limit = 5000
    last_unix = 0
    cur_length = limit
    counter = 0
    test_done = False

    while cur_length == limit:

        df = pd.read_sql("SELECT * FROM parent_reply WHERE unix > {} and parent NOT NULL ORDER BY unix ASC LIMIT {}".format(last_unix,limit),connection)
        last_unix = df.tail(1)['unix'].values[0]
        cur_length = len(df)

        if not test_done:
            with open(f'train test/test_{timeframe}.from', 'a', encoding='utf8') as f:
                for content in df['parent'].values:
                    f.write(content+'\n')

            with open(f'train test/test_{timeframe}.to', 'a', encoding='utf8') as f:
                for content in df['comment'].values:
                    f.write(str(content)+'\n')

            test_done = True

        else:
            with open(f'train test/train_{timeframe}.from', 'a', encoding='utf8') as f:
                for content in df['parent'].values:
                    f.write(content+'\n')

            with open(f'train test/train_{timeframe}.to', 'a', encoding='utf8') as f:
                for content in df['comment'].values:
                    f.write(str(content)+'\n')

        counter += 1
        if counter % 20 == 0:
            print(f'{counter * limit:,} rows completed so far')

end_t = time.perf_counter()

print(f"Elapsed time: {end_t - start_t:.2f} seconds")
