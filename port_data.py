import json
import datetime
from database import db_session, init_db 
from model import Link, ReadLater

def main():
    init_db()    

    with open('raw_data.json', 'r') as inputfile:
        data = json.loads(inputfile.read())

    links = [t['fields'] for t in data if t['model'] == 'reader.link']

    def convert_datetime(dt):
        return datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%fZ')

    def convert_last_access(it):
        it['last_access'] = convert_datetime(it['last_access'])
        return it

    links = [convert_last_access(x) for x in links]

    for it in links:
        link = Link(it['url'], it['title'])
        link.last_access = it['last_access']
        link.usage_count = it['usage_count']
        db_session.add(link)
    db_session.commit()

    readlaters = [t['fields'] for t in data if t['model'] ==
                  'reader.readlater']
    def convert_created(it):
        it['created'] = convert_datetime(it['created'])
        return it

    readlaters = [convert_created(x) for x in readlaters]

    for it in readlaters:
        readlater = ReadLater(it['url'], it['title'])
        readlater.created = it['created']
        readlater.readed = it['readed']
        db_session.add(readlater)
    db_session.commit()

if __name__ == '__main__':
    main()
