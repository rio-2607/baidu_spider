#-*-coding:utf-8-*_
import bs4
from bs4 import BeautifulSoup as bs
import urllib2 as url
import urllib

class BaiduSpider(object):
    def __init__(self,word,max_page):
        self._word = word
        self._max_page = max_page
        p = {"wd":word}
        self._start_url = "http://www.baidu.com/s?" + urllib.urlencode(p)
        # print self._start_url

    def _get_links(self):
        links = []
        # 从第一页开始获取其他几页的链接的结果不包括第一页的链接
        links.append(self._start_url)

        soup = bs(self._get_html(self._start_url),"lxml")

        links_tag = soup.select("#page")
        if 0 != len(links_tag):
            links_tag = links_tag[0]
        #
        for child in links_tag.children:
            attr = child.attrs
            if attr:
                links.append("http://www.baidu.com" + attr["href"])

        end = self._max_page if self._max_page < len(links) else len(links)

        return links[:end]

    def _get_html(self,link):
        res = url.urlopen(link)
        return res.read().decode("utf-8")

    def _get_content(self,content):
        # 先要把bs4.element.NavigableString类型转化为string类型
        return reduce(lambda x,y:x+y,map(lambda x:x.replace("<em>","").replace("</em>",""),
                                     map(lambda x:x.string,content)))

    def _spider(self):

        total_links = self._get_links()
        print total_links
        for i,l in enumerate(total_links):
            print "Page {0}".format(i+1)
            soup = bs(self._get_html(l),"lxml")
            # 找到左边内容到的跟节点
            base_div = soup.select("#content_left")[0] # base_div_list是一个列表

  
            childs = base_div.children
            for child in childs:
                # isinstance(child,bs4.element.Tag) 用来过滤掉\n
                # 'c-container' in child['class'] 用来过滤掉广告
                # child.div 过滤掉其他的干扰
                if isinstance(child,bs4.element.Tag) and child.div and child.get('class',None) and 'c-container' in child['class']:
                    # 获取到title所在的tag
                    # title所在的class标签为class=t
                    title = child.select(".t")[0]

                    print "链接:",title.a["href"]
                    print "标题",self._get_content(title.a.contents)

                    # 查找abstract所在的tag
                    # abstract坐在的class标签是class=c-abstract
                    abstract = child.select(".c-abstract")
                    # 如果没有找到c-abstract标签，则试着找下.c-span18标签
                    if 0 == len(abstract):
                        abstract = child.select(".c-span18")

                    #
                    if 0 != len(abstract):
                        abstract_str = ""
                        for c in abstract[0].children:
                            if isinstance(c,bs4.element.NavigableString):
                                abstract_str += c.string
                            if isinstance(c,bs4.element.Tag):
                                for c1 in c.children:
                                    if isinstance(c1,bs4.element.NavigableString):
                                        abstract_str += c1.string
                        print "概要:",abstract_str

    def start(self):
        self._spider()



if '__main__' == __name__:
    baidu_spider = BaiduSpider("电子科技大学",2)
    baidu_spider.start()
