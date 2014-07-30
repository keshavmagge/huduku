import re

ESCAPE_CHARS_RE = re.compile(r'(?<!\\)(?P<char>[&|+\-!(){}[\]^"~*?:])')
FUZZY_SEARCH_FIELDS = ('brand', 'description')

def solr_escape(value):
    """
    Escape un-escaped special characters and return escaped value.
    >>> solr_escape(r'foo+') == r'foo\+'
    True
    >>> solr_escape(r'foo\+') == r'foo\+'
    True
    >>> solr_escape(r'foo\\+') == r'foo\\+'
    True
    """
    return ESCAPE_CHARS_RE.sub(r'\\\g<char>', value)


def query_join(values, field, and_clause=False):
    """
    helper to create a chunk of a lucene query, based on
    some value(s) extracted from form data
    """

    # might be single value or a list of values
    if not isinstance(values, list):
        values = [values]

    # escape solr chars
    values = [solr_escape(v) for v in values]

    # quote/fuzzy values
    if field not in FUZZY_SEARCH_FIELDS:
        values = ['"%s"' % v for v in values]
    else:
        values = ['%s~0.8' % v for v in values]

    # add + to the beginnging of each value if we are doing an AND clause
    if and_clause:
        values = ["+%s" % v for v in values]

    return "+%s:(%s)" % (field, ' OR '.join(values))
