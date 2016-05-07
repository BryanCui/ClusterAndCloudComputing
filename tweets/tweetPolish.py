import couchdb
from textblob import TextBlob
import sys, json

def main():
    if len(sys.argv) < 2:
        print("need configuration file")
        sys.exit(-1)
    path = sys.argv[1]

    with open(path) as rawJson:
        conf = json.load(rawJson)

    couch = couchdb.Server(conf["database"]["serverAddr"])
    dbname = conf["database"]["dbName"]

    try:
        db = couch[dbname]
        print("opened", dbname)
    except couchdb.ResourceNotFound:
        print("DB not found")
        sys.exit(-1)

    deleteCount = 0
    updateCount = 0
    for doc_id in couchdb_pager(db):
        doc = db[doc_id]
        if doc["geo"] == None or doc["text"] == None:
            db.delete(doc)
            deleteCount += 1
        else:
            doc["sentiment"] = TextBlob(doc["text"]).sentiment.polarity
            db.save(doc)
            updateCount += 1
        if (deleteCount+updateCount)%10000 == 0:
            print("%d documents have been processed" % (deleteCount+updateCount))
    print("%d documents have been deleted" % (deleteCount))
    print("%d documents have been sentiment analysed" % (updateCount))

def couchdb_pager(db, view_name='_all_docs',
                  startkey=None, startkey_docid=None,
                  endkey=None, endkey_docid=None, bulk=5000):
    options = {'limit': bulk + 1}
    if startkey:
        options['startkey'] = startkey
        if startkey_docid:
            options['startkey_docid'] = startkey_docid
    if endkey:
        options['endkey'] = endkey
        if endkey_docid:
            options['endkey_docid'] = endkey_docid
    done = False
    while not done:
        view = db.view(view_name, **options)
        rows = []
        if len(view) <= bulk:
            done = True
            rows = view.rows
        else:
            rows = view.rows[:-1]
            last = view.rows[-1]
            options['startkey'] = last.key
            options['startkey_docid'] = last.id

        for row in rows:
            yield row.id

if __name__ == "__main__":
    main()

