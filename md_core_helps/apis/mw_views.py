#!/usr/bin/python3
"""
copied from mwviews

from apis.mw_views import PageviewsClient
# view_bot = PageviewsClient()
# new_data = view_bot.article_views_new(f'{site}.wikipedia', ["title1", "title2"], granularity='monthly', start=f'{year}0101', end=f'{year}1231')
# {'title1': {'all': 501, '2024': 501}, 'title2': {'all': 480, '2024': 480}, ... }

"""
import os
import requests
import traceback
import time
from requests.utils import quote
from datetime import date, datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from tqdm import tqdm


tool = os.getenv("HOME")
tool = tool.split("/")[-1] if tool else "himo"
# ---
default_user_agent = f"{tool} bot/1.0 (https://{tool}.toolforge.org/; tools.{tool}@toolforge.org)"

endpoints = {
    'article': 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article',
}


def parse_date(stringDate):
    return datetime.strptime(stringDate.ljust(10, '0'), '%Y%m%d%H')


def format_date(d):
    return datetime.strftime(d, '%Y%m%d%H')


def timestamps_between(start, end, increment):
    # convert both start and end to datetime just in case either are dates
    start = datetime(start.year, start.month, start.day, getattr(start, 'hour', 0))
    end = datetime(end.year, end.month, end.day, getattr(end, 'hour', 0))

    while start <= end:
        yield start
        start += increment


def month_from_day(dt):
    return datetime(dt.year, dt.month, 1)


class PageviewsClient:
    def __init__(self, user_agent="", parallelism=10):
        """
        Create a PageviewsClient

        :Parameters:
            user_agent : User-Agent string to use for HTTP requests. Should be
                         set to something that allows you to be contacted if
                         need be, ref:
                         https://www.mediawiki.org/wiki/REST_API

            parallelism : The number of parallel threads to use when making
                          multiple requests to the API at the same time
        """

        self.headers = {"User-Agent": user_agent if user_agent else default_user_agent}
        self.parallelism = parallelism

    def article_views(
            self, project, articles,
            access='all-access', agent='all-agents', granularity='daily',
            start=None, end=None):
        """
        Get pageview counts for one or more articles
        See `<https://wikimedia.org/api/rest_v1/metrics/pageviews/?doc\\
                #!/Pageviews_data/get_metrics_pageviews_per_article_project\\
                _access_agent_article_granularity_start_end>`_

        :Parameters:
            project : str
                a wikimedia project such as en.wikipedia or commons.wikimedia
            articles : list(str) or a simple str if asking for a single article
            access : str
                access method (desktop, mobile-web, mobile-app, or by default, all-access)
            agent : str
                user agent type (spider, user, bot, or by default, all-agents)
            end : str|date
                can be a datetime.date object or string in YYYYMMDD format
                default: today
            start : str|date
                can be a datetime.date object or string in YYYYMMDD format
                default: 30 days before end date
            granularity : str
                can be daily or monthly
                default: daily

        :Returns:
            a nested dictionary that looks like: {
                start_date: {
                    article_1: view_count,
                    article_2: view_count,
                    ...
                    article_n: view_count,
                },
                ...
                end_date: {
                    article_1: view_count,
                    article_2: view_count,
                    ...
                    article_n: view_count,
                }
            }
            The view_count will be None where no data is available, to distinguish from 0

        TODO: probably doesn't handle unicode perfectly, look into it
        """
        endDate = end or date.today()
        if type(endDate) is not date:
            endDate = parse_date(end)

        startDate = start or endDate - timedelta(30)
        if type(startDate) is not date:
            startDate = parse_date(start)

        # If the user passes in a string as "articles", convert to a list
        if type(articles) is str:
            articles = [articles]

        articles = [a.replace(' ', '_') for a in articles]
        articlesSafe = [quote(a, safe='') for a in articles]

        urls = [
            '/'.join([
                endpoints['article'], project, access, agent, a, granularity,
                format_date(startDate), format_date(endDate),
            ])
            for a in articlesSafe
        ]

        outputDays = timestamps_between(startDate, endDate, timedelta(days=1))
        if granularity == 'monthly':
            outputDays = list(set([month_from_day(day) for day in outputDays]))
        output = defaultdict(dict, {
            day: {a: None for a in articles} for day in outputDays
        })

        try:
            results = self.get_concurrent(urls)
            some_data_returned = False
            for result in results:
                if 'items' in result:
                    some_data_returned = True
                else:
                    continue
                for item in result['items']:
                    output[parse_date(item['timestamp'])][item['article']] = item['views']
            if not some_data_returned:
                print(Exception(
                    'The pageview API returned nothing useful at: {}'.format(urls)
                ))

            return output
        except Exception as e:
            print(f'ERROR {e} while fetching and parsing ' + str(urls))
            traceback.print_exc()

        return {}

    def get_concurrent(self, urls):
        with ThreadPoolExecutor(self.parallelism) as executor:
            def fetch(url):
                try:
                    resp = requests.get(url, headers=self.headers, timeout=10)
                    resp.raise_for_status()
                    return resp.json()
                except Exception as exc:
                    return {"error": f"{exc}", "url": url}

            # results = executor.map(fetch, urls)
            results = tqdm(executor.map(fetch, urls), total=len(urls), desc="Fetching URLs")
            return list(results)

    def article_views_new(self, project, articles, **kwargs):
        # ---
        time_start = time.time()
        # ---
        dd = self.article_views(project, articles, **kwargs)
        # ---
        new_data = {}
        # ---
        for month, y in dd.items():
            # month = datetime.datetime(2024, 5, 1, 0, 0)
            year_n = month.strftime('%Y')
            for article, count in y.items():
                new_data.setdefault(article, {"all": 0, year_n: 0})
                if count:
                    new_data[article][year_n] += count
                    new_data[article]["all"] += count
        # ---
        delta = time.time() - time_start
        # ---
        print(f"<<green>> article_views, (articles:{len(articles):,}) time: {delta:.2f} sec")
        # ---
        return new_data
