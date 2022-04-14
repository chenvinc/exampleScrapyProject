import scrapy
from exampleScrapyProject.items import SsrMovieItem

# 爬虫的主要处理逻辑都是在这个文件里写的
# 简单来说，spider就是负责抓取网页内容的部分，所有对网页进行解析和逻辑性操作都是在这里完成的
class SsrmoviesSpider(scrapy.Spider):
    name = 'ssrMovies'
    allowed_domains = ['ssr1.scrape.center']
    # 找到规律后，直接用最简单的方式完成翻页操作
    start_urls = [f'https://ssr1.scrape.center/page/{i}' for i in range(1, 11)]
    # 用于测试的URL，测试时最好减少你的访问次数与频率，避免代码还没写完先被人家反爬了
    # 被封号封ip是一件很拖进度的事情，有时候还要废钱
    # start_urls = ['https://ssr1.scrape.center/page/1']

    def parse(self, response, *args, **kwargs):
        moviesItems = response.css('.el-card__body')
        # 这里用来获取详情页的链接
        for item in moviesItems:
            href = item.css('.name::attr(href)').extract_first()
            url = response.urljoin(href)
            # 把拼接好的详情页链接抛给engine，engine一看是个request，就知道这是一个请求，就会帮你发给schedule
            # schedule会在合适的时候把这个request发给engine，让engine交给downloader下载
            # 思考一下，为什么要有schedule这个东西，为什么engine不直接把request交给downloader？
            # 这里还使用callback参数指定了这个request所对应的response应该交给哪一个方法来处理
            yield scrapy.Request(url=url, callback=self.parse_detail)

    # 解析详情页的网页结构，提取出我们需要的数据，并整理格式拼装成一个Item，最后把Item返回
    def parse_detail(self, response):
        # 首先初始化一个movie，类似于java里的new语句
        movie = SsrMovieItem()
        movie['name'] = response.css('.m-b-sm::text').extract_first()
        movie['tags'] = response.xpath('//div[@class="categories"]//span/text()').extract()
        # 还记得我说的css选择器不方便的地方吗？
        movie['rating'] = response.xpath('//p[@class="score m-t-md m-b-n-sm"]/text()').re_first('[\d\.]+')
        infoList = response.xpath('//div[@class="m-v-sm info"]/span/text()').extract()
        # 这一句是用来整理数据格式，变得更好看的
        movie['info'] = ''.join(infoList)
        describe = response.css('.drama p::text').extract_first().strip()
        # 这一句也是用来整理数据格式的，不妨把这两句注释掉跑一跑，看看会发生什么变化
        describe = describe.replace(' ', '')
        movie['describe'] = describe
        # 这里就把组装好的Item返回了，这个movie被抛出后就去了engine
        # engine一看是一个item类型，就知道这是你要保存的数据，就会把这个item扔给pipeline做后续处理
        yield movie
