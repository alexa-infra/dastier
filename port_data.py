import sqlite3
import json
import datetime

def main():
    db = sqlite3.connect('sqlite.db', sqlite3.PARSE_DECLTYPES|
                         sqlite3.PARSE_COLNAMES)

    with open('schema.sql', 'r') as inputfile:
        db.cursor().executescript(inputfile.read())
    db.commit()

    with open('raw_data.json', 'r') as inputfile:
        data = json.loads(inputfile.read())

    reader_links = [t['fields'] for t in data if t['model'] == 'reader.link']

    def convert_datetime(dt):
        return datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%fZ')

    def convert_last_access(it):
        it['last_access'] = convert_datetime(it['last_access'])
        return it

    reader_links = [convert_last_access(x) for x in reader_links]

    for it in reader_links:
        db.execute('insert into reader_link (url, title, usage_count,'
                   ' last_access) values (?, ?, ?, ?)',
                   [it['url'], it['title'], it['usage_count'],
                    it['last_access']])
    db.commit()

    reader_readlater = [t['fields'] for t in data if t['model'] ==
                        'reader.readlater']
    def convert_created(it):
        it['created'] = convert_datetime(it['created'])
        return it

    reader_readlater = [convert_created(x) for x in reader_readlater]

    for it in reader_readlater:
        db.execute('insert into reader_readlater (url, title, '
                   'created, readed) values (?, ?, ?, ?)',
                   [it['url'], it['title'], it['created'],
                    it['readed']])
    db.commit()

if __name__ == '__main__':
    main()
