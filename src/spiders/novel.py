import scrapy


class NovelSpider(scrapy.Spider):
    name = "全本小說網"
    allowed_domains = ["m.wfxs.tw"]

    def __init__(self, novelId, *args, **kwargs):
        super(NovelSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://m.wfxs.tw/xs-{novelId}/"]
        self.custom_settings = {
            "FEEDS": {
                "data/{novelId}.jl": {
                    "format": "jsonlines",
                    "encoding": "utf8",
                },
            }
        }

    def parse_chapter(self, response):
        title = response.css("h1::text").get()
        self.logger.info("讀取 %s", title)
        yield {
            "title": title,
            "content": "\n".join(
                [
                    line
                    for line in [
                        line.strip()
                        for line in response.css("#content p::text").getall()
                    ]
                    if line != "本章尚未完結,請點擊下一頁繼續閱讀---->>>"
                ]
            ),
        }

    def parse(self, response):
        counter = 0
        # follow links to author pages
        for href in response.css("ul.list a::attr(href)").extract():
            counter += 1
            yield scrapy.Request(response.urljoin(href), callback=self.parse_chapter)
