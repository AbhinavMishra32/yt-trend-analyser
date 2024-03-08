from py1337x import py1337x

# Using 1337x.tw and saving the cache in sqlite database which expires after 500 seconds
torrents = py1337x(proxy='1337x.se', cache='py1337xCache', cacheTime=500)

print(torrents.search('harry potter'))
# {'items': [...], 'currentPage': 1, 'itemCount': 20, 'pageCount': 50}

# Searching harry potter in category movies and sort by seeders in descending order
# torrents.search('harry potter', category='movies', sortBy='seeders', order='desc') 
# {'items': [...], 'currentPage': 1, 'itemCount': 40, 'pageCount': 50}

# Viewing the 5th page of the result
# torrents.search('harry potter', page=5) 
# {'items': [...], 'currentPage': , 'itemCount': 20, 'pageCount': 50}