API Read Me
-----------

end point
    /api/search/?format=json

optional query params to filter results
    - brand
    - description
    - gender
    - category
    - merchant

###fuzzy search support on params
    - brand

      /api/search/?brand=Adidass&merchant=Nordstrom&format=json
      /api/search/?brand=Adidas&merchant=Nordstrom&format=json

return same results

      /api/search/?brand=Calvin+Klein&merchant=Nordstrom&format=json

returns results for brands that have either Calvin or Klein in their name

    - category

      /api/search/?category=top&merchant=Nordstrom&format=json
      /api/search/?category=tops&merchant=Nordstrom&format=json

return same results

faceting available on brand, merchant, category, price, gender

###Pagination

API response has meta section that tells the current page and has next 
and previous links

    meta{
        limit:20
        next:"/api/search/?merchant=nordstrom&offset=20&limit=20&format=json"
        offset:0
        previous:null
        total_count:20
        total_search_hits:255324
    }

pass 'offset' and 'limit' params to paginate through the results

    /api/search/?merchant=nordstrom&format=json&offset=50&limit=50
