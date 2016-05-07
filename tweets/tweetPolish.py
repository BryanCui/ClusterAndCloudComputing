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
    for doc_id in db:
        doc = db[doc_id]
        if doc["geo"] == None or doc["text"] == None:
            db.delete(doc)
            deleteCount += 1
        else:
            doc["sentiment"] = TextBlob(doc["text"]).sentiment.polarity
            db.save(doc)
            updateCount += 1
    print("%d documents have been deleted" % (deleteCount))
    print("%d documents have been sentiment analysed" % ()

if __name__ == "__main__":
    main()

