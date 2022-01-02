import scrapy

# from tqdm import tqdm


class Parser:
    def __init__(
        self: str,
        site: str,
        pages: str,
        content: str,
        garbage: list[str] = [],
        title: str = "h1::text",
        joiner: str = "\n",
    ):
        self.site = site
        self.pages = pages
        self.content = content
        self.garbage = garbage
        self.title = title
        self.joiner = joiner


class NovelSpider(scrapy.Spider):
    name = "全本小說網"
    allowed_domains = ["m.wfxs.tw", "www.69shu.com"]
    web_parser = {
        "69shu": Parser(
            site="https://www.69shu.com/{0}/",
            pages="#catalog li a::attr(href)",
            content=".txtnav::text",
            garbage=["(本章完)"],
        ),
        "wfxs": Parser(
            site="https://m.wfxs.tw/xs-{0}/",
            pages="ul.list a::attr(href)",
            content="#content p::text",
            garbage=["本章尚未完結,請點擊下一頁繼續閱讀---->>>"],
        ),
    }
    pbar = None

    def __init__(self, novelId, website, limit=None, *args, **kwargs):
        super(NovelSpider, self).__init__(*args, **kwargs)
        self.parser = self.web_parser[website]
        self.limit = int(limit) if limit is not None else None
        print(f"Using {website} to parse and limit to {limit}")
        self.start_urls = [self.parser.site.format(novelId)]
        print(f"Url: {self.start_urls}")

    def parse_chapter(self, response):
        title = response.css(self.parser.title).get()
        if self.pbar is not None:
            self.pbar.update(1)
        yield {
            "title": title,
            "content": self.parser.joiner.join(
                [
                    line
                    for line in [
                        line.strip()
                        for line in response.css(self.parser.content).getall()
                    ]
                    if line not in self.parser.garbage
                ]
            ),
        }

    def parse(self, response):
        counter = 0
        # follow links to author pages
        for href in response.css(self.parser.pages).extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_chapter)
            counter += 1
            if self.limit is not None and self.limit <= counter:
                print(f"Exec {counter} and break!")
                break
        # self.pbar = tqdm(total=counter)
