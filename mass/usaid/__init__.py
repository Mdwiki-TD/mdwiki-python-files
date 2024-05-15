'''

:write python code to do:

# open url: https://www.flickr.com/photos/usaid_images/albums/
# match "albumsList":{(.*?)},"totalItems"
# get albums list from _data : { "data": { "_data":[], }, "exportMetaType": "collection" }
# match next page from <link   rel="next"   href="https://www.flickr.com/photos/usaid_images/albums/page2/"  data-dynamic="true" />
# repeat step 2, 3 and 4 until no more pages



https://www.flickr.com/services/rest/?method=flickr.photosets.getPhotos&api_key=##&photoset_id=72177720316668580&format=json&nojsoncallback=1

https://api.flickr.com/services/rest?extras=can_addmeta%2Ccan_comment%2Ccan_download%2Ccan_print%2Ccan_share%2Ccontact%2Ccontent_type%2Ccount_comments%2Ccount_faves%2Ccount_views%2Cdate_taken%2Cdate_upload%2Cdescription%2Cicon_urls_deep%2Cisfavorite%2Cispro%2Clicense%2Cmedia%2Cneeds_interstitial%2Cowner_name%2Cowner_datecreate%2Cpath_alias%2Cperm_print%2Crealname%2Crotation%2Csafety_level%2Csecret_k%2Csecret_h%2Curl_sq%2Curl_q%2Curl_t%2Curl_s%2Curl_n%2Curl_w%2Curl_m%2Curl_z%2Curl_c%2Curl_l%2Curl_h%2Curl_k%2Curl_3k%2Curl_4k%2Curl_f%2Curl_5k%2Curl_6k%2Curl_o%2Cvisibility%2Cvisibility_source%2Co_dims%2Cpubliceditability%2Csystem_moderation&per_page=500&page=1&get_user_info=1&primary_photo_extras=url_c%2C+url_h%2C+url_k%2C+url_l%2C+url_m%2C+url_n%2C+url_o%2C+url_q%2C+url_s%2C+url_sq%2C+url_t%2C+url_z%2C+needs_interstitial%2C+can_share&jump_to=&photoset_id=72157714381416766&viewerNSID=200672992%40N03&method=flickr.photosets.getPhotos&csrf=1715752980%3Aid3yvgzpgmo%3Ad1e5822e3dca3ea98015e43f81bcddb2&api_key=7ee1c7f52475dd05970ec245e8976645&format=json&hermes=1&hermesClient=1&reqId=7be4de8d-12ee-434b-b6eb-b7473dba5faa&nojsoncallback=1

https://api.flickr.com/services/rest?extras=can_addmeta,can_comment,can_download,can_print,can_share,contact,content_type,count_comments,count_faves,count_views,date_taken,date_upload,description,icon_urls_deep,isfavorite,ispro,license,media,needs_interstitial,owner_name,owner_datecreate,path_alias,perm_print,realname,rotation,safety_level,secret_k,secret_h,url_sq,url_q,url_t,url_s,url_n,url_w,url_m,url_z,url_c,url_l,url_h,url_k,url_3k,url_4k,url_f,url_5k,url_6k,url_o,visibility,visibility_source,o_dims,publiceditability,system_moderation&per_page=500&page=1&get_user_info=1&primary_photo_extras=url_c, url_h, url_k, url_l, url_m, url_n, url_o, url_q, url_s, url_sq, url_t, url_z, needs_interstitial, can_share&jump_to=&photoset_id=72157714381416766&viewerNSID=200672992@N03&method=flickr.photosets.getPhotos&csrf=1715752980:id3yvgzpgmo:d1e5822e3dca3ea98015e43f81bcddb2&api_key=7ee1c7f52475dd05970ec245e8976645&format=json&hermes=1&hermesClient=1&reqId=7be4de8d-12ee-434b-b6eb-b7473dba5faa&nojsoncallback=1
'''

