from urllib import request
from io import BytesIO
import gzip
import re

class Spider():
    url = 'https://www.douyu.com/g_LOL'
    root_pattern = '</div><div class="DyListCover-info">([\s\S]*?)</div>'
    num_pattern = '</svg>([\d\D]*?)</span>'
    name_pattern = '<use xlink:href="#icon-user_c95acf8"></use></svg>([\s\S]*?)</h2>$'

    def _fetch_content(self):
        r = request.urlopen(Spider.url)
        htmls = r.read()
        buff = BytesIO(htmls)
        f = gzip.GzipFile(fileobj=buff)
        htmls = f.read().decode('utf-8')
        return htmls
        
    def _analysis(self, htmls):
        root_html = re.findall(Spider.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            num = re.findall(Spider.num_pattern, html)
            anchor = {'name': name, 'num': num}
            anchors.append(anchor)
        return anchors

    def _refine(self, anchors):
        return list(map(lambda anchor: {'name': anchor['name'][0], 'num': anchor['num'][0]}, anchors))

    def _sort(self, anchors):
        return sorted(anchors, key=self._sort_seed, reverse=True)

    def _sort_seed(self, anchor):
        r = re.findall('[1-9]\d*\.?\d*', anchor['num'])
        number = float(r[0])
        if '万' in anchor['num']:
            number *= 10000
        return number

    def _show(self, anchors):
        for rank in range(0, len(anchors)):
            print('排名' + str(rank) + ':  ' + anchors[rank]['name'] + '------' + anchors[rank]['num'])
        
    def go(self):
        htmls = self._fetch_content()
        anchors = self._analysis(htmls)
        anchors = self._refine(anchors)
        anchors = self._sort(anchors)
        self._show(anchors)



spider = Spider()
spider.go()