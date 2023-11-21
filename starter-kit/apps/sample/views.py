from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.shortcuts import render
from django.http import HttpResponse
from scrapy.crawler import CrawlerProcess
from .scraper import MySpider


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to sample/urls.py file for more pages.
"""


class SampleView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


# views.py




def category_articles(request):
    """
    Scrape articles based on the selected category and render them in a template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered template.
    """
    # Call a function to scrape articles based on the selected category
    process = CrawlerProcess({
        'DOWNLOAD_DELAY': 5,  # Add a delay of 2 seconds between requests
        'CONCURRENT_REQUESTS': 1,  # Limit concurrent requests to 1
        'COOKIES_ENABLED': True,  # Enable cookies for session management
        'RETRY_TIMES': 3,  # Retry failed requests up to 3 times
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        },
    })

    process.crawl(MySpider)  # Instantiate MySpider class and crawl the data
    process.start()
    
    # Process the scraped data to match the format needed for the template
    results = MySpider.results
    articles = []
    for item in results:
        article = {
            'Title': item['Title'],
            'Authors': ', '.join(item['Authors']),  # Convert authors list to a string
            
        }
        print(article['Title'],article['Authors'])
        articles.append(article)

    # Render the template with the processed data
    return render(request, 'index.html', {'articles': articles})