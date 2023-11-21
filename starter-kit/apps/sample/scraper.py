import scrapy
from scrapy.crawler import CrawlerProcess
import tkinter as tk
from tkinter import ttk
from prettytable import PrettyTable


class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ["https://easychair.org/publications/EPiC/Computing"]

    def start_requests(self):
        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        articles = response.xpath('//td')
        if not articles:
            self.logger.info(f"No articles found for category: Computer Science")
            self.logger.info(f"Here is the link I used: {response.url}")
            return

        results = []  # List to store the results

        for article in articles:
            title = article.xpath('.//div[@class="title"]/a/text()').extract()
            authors = article.xpath('.//div[@class="authors"]/a/text()').extract()
            result = {
                "Title": title,
                "Authors": authors,
            }
            results.append(result)  # Add the result to the list

        # Log the number of items retrieved
        self.logger.info(f"Retrieved {len(articles)} items")

        # Log any errors that occur
        if response.status != 200:
            self.logger.error(f"Error retrieving data. Status code: {response.status}")

        # Display the results in a table
        table = PrettyTable()
        table.field_names = ["Title", "Authors"]

        for result in results:
            table.add_row([result["Title"], result["Authors"]])

        # Create a GUI window
        window = tk.Tk()
        window.title("Results")

        # Create a treeview widget to display the table
        tree = ttk.Treeview(window)
        tree["columns"] = ("Title", "Authors")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Title", anchor=tk.W, width=200)
        tree.column("Authors", anchor=tk.W, width=200)
        tree.heading("Title", text="Title")
        tree.heading("Authors", text="Authors")

        # Insert the data into the treeview
        for result in results:
            tree.insert("", tk.END, values=(result["Title"], result["Authors"]))

        # Pack the treeview widget
        tree.pack(expand=True, fill=tk.BOTH)

        # Start the GUI event loop
        window.mainloop()

