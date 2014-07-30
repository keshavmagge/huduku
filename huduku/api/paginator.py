from tastypie.paginator import Paginator


class SolrPaginator(Paginator):
    def __init__(self, request_data, objects, resource_uri=None, limit=None, 
                 offset=0, max_limit=1000, collection_name='objects', object_count=0):
        self.request_data = request_data
        self.objects = objects
        self.limit = limit
        self.max_limit = max_limit
        self.offset = offset
        self.resource_uri = resource_uri
        self.collection_name = collection_name
        self.object_count = object_count

    def get_slice(self, limit, offset):
        """
        no need to slice as SOLR has already returned the desired slice
        """
        return self.objects

    def get_previous(self, limit, offset):
        """
        If a previous page is available, will generate a URL to request that
        page.
        """
        if offset-limit > 0:
            return self._generate_uri(limit, offset-limit)
        return None

    def get_next(self, limit, offset, count):
        """
        If a next page is available, will generate a URL to request that
        page. 
        """
        if offset + limit < self.object_count:
            return self._generate_uri(limit, offset+limit)
        return None

    def page(self):
        """
        adds total search hits to _meta
        """
        data = super(SolrPaginator, self).page()
        data['meta']['total_search_hits'] = self.object_count
        return data
