MASTER_NODE =  "master"
MASTER_PASSWORD = "Random#123"
DOMAIN_ENDPOINT = "https://search-events-ixh2p2yqvdvwyt6xe6llrwt47e.us-east-1.es.amazonaws.com/"
JSON_FILENAME = "IndexedEvents.json"

!curl -XPOST -u master:Random#123 https://search-events-ixh2p2yqvdvwyt6xe6llrwt47e.us-east-1.es.amazonaws.com/_bulk --data-binary IndexedEvents.json -H 'Content-Type: application/json'