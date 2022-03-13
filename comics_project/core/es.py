# -*- coding: utf-8 -*-
from uuid import uuid4
from elasticsearch import Elasticsearch, TransportError
from django.conf import settings

es = Elasticsearch(settings.ELASTICSEARCH['url'])
index_name = settings.ELASTICSEARCH['index_name']


class ESException(Exception):
    pass


class ES(object):
    def __init__(self):
        pass


def bulk_create(doc_type, docs):
    bulk_data = []
    for row in docs:
        op_dict = {
            "index": {
                "_index": index_name,
                "_type": doc_type,
                "_id": row['id']
            }
        }

        bulk_data.append(op_dict)
        bulk_data.append(row)

    es.bulk(bulk_data, index=index_name, doc_type=doc_type, refresh=True)


def is_closed():
    state = es.cluster.state(index=index_name, metric='metadata')
    return state['metadata']['indices'][index_name]['state'] == 'close'


def exists():
    return es.indices.exists(index=index_name)


def exists_type():
    return es.indices.exists_type(index=index_name)


def get_mapping():
    return es.indices.get_mapping(index=index_name)


def get_field_mapping():
    return es.indices.get_field_mapping(index=index_name)


def get_settings():
    return es.indices.get_settings(index=index_name)


def delete_indices():
    es.indices.delete(index=index_name)


def create_indice():
    index_settings = {
        'settings': {
            "max_ngram_diff": 6,
            'number_of_shards': settings.ELASTICSEARCH['number_of_shards'],
            'number_of_replicas': settings.ELASTICSEARCH['number_of_replicas'],
            "analysis": {
                "filter": {
                    "ngram_filter": {
                        "type": "ngram",
                        "min_gram": 3,
                        "max_gram": 8
                    }
                },
                "analyzer": {
                    "index_ngram": {
                        "type": "custom",
                        "tokenizer": "keyword",
                        "filter": ["ngram_filter", "lowercase"]
                    },
                    "search_ngram": {
                        "type": "custom",
                        "tokenizer": "keyword",
                        "filter": "lowercase"
                    }
                }
            }
        }
    }

    try:
        es.indices.create(index=index_name, body=index_settings)
    except TransportError as e:
        print(e)
        raise ESException('index already exists')

    return True


def create_doc_type(doc_type, mapping):
    body = {doc_type: mapping}
    resp = es.indices.put_mapping(index=index_name, doc_type=doc_type,
                                  body=body, include_type_name=True)
    return resp


def refresh():
    es.indices.refresh()


def create(doc_type, doc, object_id=None):
    res = es.index(index=index_name, doc_type=doc_type, body=doc, id=object_id)
    return res


def update(doc_type, doc, object_id):
    res = es.update(index=index_name, doc_type=doc_type, body=doc, id=object_id)
    return res


def get(doc_type, object_id):
    res = es.get(index=index_name, doc_type=doc_type, id=object_id)
    return res


def remove(doc_type, object_id):
    return es.delete(index=index_name, id=object_id, doc_type=doc_type)


def count(doc_type, query=None):
    body = None
    if query:
        body = dict()
        body['query'] = query

    response = es.count(index=index_name, doc_type=doc_type, body=body)
    return response.get('count', 0)


def search(doc_type, query=None, order_by=None, offset=0, limit=15, fields=None):
    body = {}
    if query:
        body['query'] = query

    if order_by:
        body['sort'] = order_by

    body['_source'] = {
        'includes': ['*'],
        'excludes': []
    }

    if fields:
        body['_source']['includes'] = fields

    response = es.search(index=index_name,
                         doc_type=doc_type,
                         body=body,
                         from_=offset,
                         size=limit)

    data = [dict(val['_source'].items()) for val in response['hits']['hits']]
    return {'hits': data, 'total': response['hits']['total']}
