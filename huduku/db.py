import logging
import psycopg2

from django.conf import settings

log = logging.getLogger(__name__)

def get_db_connection():
    """
    returns a connection to the database specified in the settings file
    """
    connection = None
    params = settings.DATABASES.get('default')
    try:
        connection = psycopg2.connect(dbname=params['NAME'], user=params['USER'],
                                      password=params['PASSWORD'], host=params['HOST'])
    except OperationalError, e:
        # connection failed
        log.exception(e)
    return connection

def get_cps_data():
    """
    gets cps product/sku data from CPS DB
    """
    conn = get_db_connection()
    query = """select distinct(product.name), product.id as id, product.description, 
               long_description, age, gender, b.name as brand, b.name as str_brand, 
               m.name as merchant, m.name as str_merchant, category.name as category, 
               category.name as str_category, price, sale_price from product, sku, 
               merchant as b, merchant as m, category where product.brand_id = b.id 
               and sku.merchant_id = m.id and product.category_id = category.id and 
               product.id = sku.product_id and product.active is True and sku.active
               is True;"""
    cur = conn.cursor()
    cur.execute(query)
    for row in cur.fetchall():
        yield row
