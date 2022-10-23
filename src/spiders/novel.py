import sys
import scrapy


class Parser:
    def __init__(
        self: str,
        site: str,
        pages: str,
        content: str,
        garbage: list[str] = [],
        title: str = None,
        next: str = None,
        joiner: str = "\n",
    ):
        self.site = site
        self.pages = pages
        self.title = title
        self.content = content
        self.next = next
        self.garbage = garbage
        self.joiner = joiner


class NovelSpider(scrapy.Spider):
    name = "全本小說網"
    allowed_domains = ["m.wfxs.tw", "www.69shu.com"]
    web_parser = {
        "69shu": Parser(
            site="https://www.69shu.com/{0}/",
            pages="#catalog li a::attr(href)",
            title="h1::text",
            content=".txtnav::text",
            garbage=["(本章完)"],
        ),
        "wfxs": Parser(
            site="https://m.wfxs.tw/xs-{0}/",
            pages="ul.list a::attr(href)",
            title="h1::text",
            content="#content p::text",
            garbage=["本章尚未完結,請點擊下一頁繼續閱讀---->>>"],
        ),
        "czbooks": Parser(
            site="https://czbooks.net/n/{0}",
            pages="#chapter-list li a::attr(href)",
            title=".chapter-detail .name::text",
            content=".chapter-detail .content::text",
        ),
        "czbooks2": Parser(
            site="https://czbooks.net/n/{0}",
            pages="#chapter-list li a::attr(href)",
            content=".chapter-detail .content::text",
        ),
        "zgdyjz": Parser(
            site="https://m.zgdyjz.net/info/{0}/",
            pages="ul li a::attr(href)",
            next=".listpage a:last-child::attr(href)",
            title="h1::text",
            content="#booktxt p::text",
        ),
        "twfanti": Parser(
            site="https://m.twfanti.com/{0}/dir.html/",
            pages=".chapter-list a::attr(href)",
            title=".size18.w100.text-center.lh100.pt30.pb15::text",
            content="#pt-pop p::text",
        ),
        "fantinovels": Parser(
            site="https://m.fantinovels.com/twlist/{0}/dir.html",
            pages=".chapter-list a::attr(href)",
            title=".size18.w100.text-center.lh100.pt30.pb15::text",
            content="#pt-pop p::text",
        ),
    }
    total = 0
    processed = 0

    def __init__(self, novelId, website, limit=None, offset=0, *args, **kwargs):
        super(NovelSpider, self).__init__(*args, **kwargs)
        self.parser = self.web_parser[website]
        self.limit = int(limit) if limit is not None else None
        self.offset = int(offset)
        print(f"Using {website} to parse {novelId} and limit to {limit}")
        self.start_urls = [self.parser.site.format(novelId)]
        print(f"Url: {self.start_urls}")

    def parse_chapter(self, response):
        self.processed += 1
        sys.stdout.write(f"( {self.processed} / {self.total} )\r")

        content = [
            line
            for line in [
                line.strip() for line in response.css(self.parser.content).getall()
            ]
            if line not in self.parser.garbage
        ]
        title = (
            content.pop(0)
            if self.parser.title is None
            else response.css(self.parser.title).get()
        )

        yield {
            "title": title,
            "content": self.parser.joiner.join(content).strip(),
        }

        if self.processed == self.total:
            sys.stdout.write("\nDone!")

    def parse(self, response):
        print("Start parsing!")
        # follow links to author pages
        for href in response.css(self.parser.pages).extract():
            if self.offset > 0:
                self.offset -= 1
                continue

            yield scrapy.Request(
                response.urljoin(href),
                callback=self.parse_chapter,
                dont_filter=True,
            )

            self.total += 1
            if self.limit is not None and self.limit <= self.total:
                print(f"Exec {self.total} and break!")
                break

        if self.parser.next is not None:
            print(self.parser.next)
            href = response.css(self.parser.next).get()
            link = response.urljoin(href)
            if link.startswith("http"):
                print(f"Next {link}")
                yield scrapy.Request(
                    link,
                    callback=self.parse,
                    dont_filter=True,
                )


if __name__ == "__main__":
    print(scrapy.__version__)
