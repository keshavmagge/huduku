import logging

from datetime import datetime

from django.conf import settings
from solr import SolrConnection

from huduku import db

log = logging.getLogger(__name__)

def build_index(**kwargs):
    """
    gets product/sku information from cps DB and indexes them in solr

    existing solr index is wiped before indexing. Revisit if this strategy
    does not work
    """
    # index status log message granularity
    log_index_status_chunks = 25000
    solr = SolrConnection(settings.SOLR)
    clear_index(solr=solr)
    count = 0
    fieldnames = ('name', 'id', 'description', 'long_description', 'age', 
                  'gender', 'brand', 'str_brand', 'merchant', 'str_merchant',
                  'category', 'str_category', 'price', 'sale_price', 'buy_url', 
                  'image',)
    start = datetime.now()
    log.info('Reading product info from the database.....')
    products = db.get_cps_data()
    log.info('Building SOLR index.....')
    for product in products:
        try:
            product_record = dict(zip(fieldnames, product))
            solr.add(**product_record) 
            count += 1
        except Exception, e: 
            log.exception(e)
            continue
        if count % log_index_status_chunks == 0:
            log.info('Indexed %d products in %s' % (count, datetime.now()-start))
    solr.commit()
    log.info('Indexed %d products in %s' % (count, datetime.now()-start))


def clear_index(**kwargs):
    """
    deletes existing index data
    pass additional parameters like brand, merchant etc to filter results
    that ought to be deleted.
    """
    log.info('Clearing existing SOLR index')
    solr = kwargs.get('solr', SolrConnection(settings.SOLR))
    solr.delete_query('*:*')
    solr.commit()    
    log.info('SOLR index cleared!')
