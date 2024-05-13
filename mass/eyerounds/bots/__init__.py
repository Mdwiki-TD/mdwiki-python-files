'''

:write python code to do:
*. open url https://eyerounds.org/cases.htm
*. match all div with class "col-xs-12 col-sm-6 col-md-6 col-lg-4"
like:(
    <div class="col-xs-12 col-sm-6 col-md-6 col-lg-4" id="cat6">
    
*. get href     <div class="col-xs-12 col-sm-6 col-md-6 col-lg-4" id="cat6"><div class="card  m-1"><a href="neuro-op_cases.htm">
*. get title     <div class="col-xs-12 col-sm-6 col-md-6 col-lg-4" id="cat6"><div class="card  m-1"><p class="text-center"><strong>Neuro-Ophthalmology</strong></p>

*. add title to dict urls contains: {title: {"url": href, "cases": {}}}
*. save urls to json file named urls.json

'''
