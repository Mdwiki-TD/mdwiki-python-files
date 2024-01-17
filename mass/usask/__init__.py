'''

:write python code to do:
1. open url https://openpress.usask.ca/undergradimaging/
2. match all <p class="toc__title">
like:(
    <p class="toc__title"><a href="https://openpress.usask.ca/undergradimaging/chapter/radiation-in-medical-imaging/">Radiation in Medical Imaging: The x-ray Tube</a></p>)
    
3. get href and title
4. add title to dict urls contains: {title: {"url": href, "images": {}}}
5. save urls to json file named urls.json

'''
