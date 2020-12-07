import sqlite3
import pandas as pd

#This can later be edited so that it can contain more months
timeframes = ['2009-01']

def pullData():
    with open('test.from','a', encoding='utf8') as f:
        for content in df['parent'].values:
            f.write(content+'\n')

    with open('test.to','a', encoding='utf8') as f:
        for content in df['comment'].values:
            f.write(str(content)+'\n')



for timeframe in timeframes:
    connection = sqlite3.connect('{}.db'.format(timeframe))
    c = connection.cursor()
    limit = 50000
    last_unix = 0 
    cur_length = 0 
    counter = 0 
    test_done = False

    while cur_length == limit:
        df = pd.read_sql("SELECT * FROM parent_reply WHERE unix > {} and parent NOT NULL and score > 0 ORDER BY unix ASC LIMIT {}".format(last_unix,limit),connection)
        last_unix = df.tail(1)['unix'].values[0]
        cur_length = len(df)

        if not test_done:
            pullData()
            test_done = True
        else:
            pullData()
        
        counter += 1
        if counter % 20 == 0:
            print(counter*limit,'rows completed so far')

        
