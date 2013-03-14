import re
import urllib
import urlparse
from pyquery import PyQuery 
import domain
import unittest


class HtmlAnalyzer(object):

    @staticmethod
    def detectCharSet(html):

        pq = PyQuery(html)

        metas = pq('head')('meta')

        for meta in metas:
            for key in meta.keys():
                if key == "charset":
                    charset = meta.get('charset')
                    return charset
                if key == "content":
                    try:
                        p = re.match(r".+charset=(.*)\W*",meta.get('content'))
                        return p.group(1)
                    except:
                        continue

    @staticmethod
    def extractLinks(html,baseurl,charset):

        def _extract(url):
            link = url.attrib['href']

            link = link.strip("/ ")
            if link is None:
                raise

            link = urlparse.urljoin(baseurl,link)
            link = urlparse.urldefrag(link)[0]

            try:
                link = urllib.quote(link, ':?=+&#/@')
            except (UnicodeDecodeError,KeyError):
                try:
                    link = urllib.quote(link.encode(charset), ':?=+&#/@')
                except:
                    pass

            return link


        def _isValidLink(url):
            try:
                return all([UrlFilter.checkScheme(url),
                            UrlFilter.checkInvalidChar(url),
                            UrlFilter.checkInvalidExtention(url)
                            ])
            except:
                return False

        pq = PyQuery(html)

        for url in pq('a'):
            try:
                link = _extract(url)
            except:
                continue

            if _isValidLink(link):
                yield link
            continue




class UrlFilter(object):

    invalid_chars = {'\'':None,
                     '\"':None,
                     '\\':None,
                     ' ' :None,
                     '\n':None,
                     '\r':None,
                     '+' :None
                     }

    invalid_extention = {
                    'jpg'  :  None,
                    'gif'  :  None,
                    'bmp'  :  None,
                    'jpeg' :  None,
                    'png'  :  None,

                    'swf'  :  None,
                    'mp3'  :  None,
                    'wma'  :  None,
                    'wmv'  :  None,
                    'wav'  :  None,
                    'mid'  :  None,
                    'ape'  :  None,
                    'mpg'  :  None,
                    'mpeg' :  None,
                    'rm'   :  None,
                    'rmvb' :  None,
                    'avi'  :  None,
                    'mkv'  :  None,

                    'zip'  :  None,
                    'rar'  :  None,
                    'gz'   :  None,
                    'iso'  :  None,
                    'jar'  :  None,

                    'doc'  :  None,
                    'docx' :  None,
                    'ppt'  :  None,
                    'pptx' :  None,
                    'chm'  :  None,
                    'pdf'  :  None,

                    'exe'  :  None,
                    'msi'  :  None,
                }

    @staticmethod
    def checkScheme(url):
        scheme, netloc, path, pm, q, f = urlparse.urlparse(url)
        return scheme in ('http', 'https')

    @classmethod
    def checkInvalidChar(cls,url):
        exist_invalid_char = False
        for c in url:
            if c in cls.invalid_chars:
                exist_invalid_char = True
                break
        return (not exist_invalid_char)

    @classmethod
    def checkInvalidExtention(cls,url):
        dotpos = url.rfind('.') + 1
        typestr = url[dotpos:].lower()
        return (typestr not in cls.invalid_extention)


    @staticmethod
    def isSameDomain(first_url, second_url):
        fhost = urlparse.urlparse(first_url).netloc
        shost = urlparse.urlparse(second_url).netloc
        return (domain.GetFirstLevelDomain(fhost) == 
                domain.GetFirstLevelDomain(shost))

    @staticmethod
    def isSameHost(first_url, second_url):
        return urlparse.urlparse(first_url).netloc == urlparse.urlparse(second_url).netloc

    @staticmethod
    def isSameSuffixWithoutWWW(first_url, second_url):
        fhost = '.' + urlparse.urlparse(first_url).netloc
        shost = '.' + urlparse.urlparse(second_url).netloc

        if shost[:5] == '.www.':
            shost = shost[5:]

        if fhost.find(shost) != -1:
            return True
        else:
            return False
        
    # check whether first_url has the suffix second_url
    @staticmethod
    def isSameSuffix(first_url, second_url):
        fhost = '.' + urlparse.urlparse(first_url).netloc
        shost = '.' + urlparse.urlparse(second_url).netloc

        if fhost.find(shost) != -1:
            return True
        else:
            return False

class TestHtmlAnalyzer(unittest.TestCase):

    url = "http://www.sina.com.cn"
    charset = 'gb2312'

    def setUp(self):
        import requests
        r = requests.get(self.url)
        r.encoding = self.charset
        self.html = r.text

    def testDetectCharSet(self):
        charset = HtmlAnalyzer.detectCharSet(self.html)
        self.assertEqual(charset ,self.charset)

    def testExtractLinks(self):
        links = []
        for link in HtmlAnalyzer.extractLinks(self.html,self.url,self.charset):
            links.append(link)
        self.assertGreater(len(links),1000)


class TestUrlFilter(unittest.TestCase):

    def testCheckScheme(self):
        url1 = "http://www.sina.com.cn"
        url2 = "javascript:void(0)"
        url3 = "mailto:kenshin.acs@gmail.com"
        self.assert_(UrlFilter.checkScheme(url1))
        self.assertFalse(UrlFilter.checkScheme(url2))
        self.assertFalse(UrlFilter.checkScheme(url3))
    
    def testCheckInvalidChar(self):
        url1 = "http://www.sina.com.cn"
        url2 = "http://www.sina.com.cn+"
        self.assert_(UrlFilter.checkInvalidChar(url1))
        self.assertFalse(UrlFilter.checkInvalidChar(url2))

    def testCheckInvalidExtention(self):
        url1 = "http://www.sina.com.cn"
        url2 = "http://www.sina.com.cn/hack.pdf"
        self.assert_(UrlFilter.checkInvalidExtention(url1))
        self.assertFalse(UrlFilter.checkInvalidExtention(url2))

    def testIsSameDomain(self):
        url1 = "http://www.sina.com.cn"
        url2 = "http://www.sina.com"
        url3 = "http://news.sina.com.cn"
        self.assertFalse(UrlFilter.isSameDomain(url1,url2))
        self.assert_(UrlFilter.isSameDomain(url1,url3))

    def testIsSameHost(self):
        url1 = "http://www.sina.com.cn"
        url2 = "http://news.sina.com.cn"
        url3 = "http://www.sina.com.cn/news/"
        self.assertFalse(UrlFilter.isSameHost(url1,url2))
        self.assert_(UrlFilter.isSameHost(url1,url3))

    def testIsSameSuffixWithoutWWW(self):
        url1 = "http://news.sina.com.cn"
        url2 = "http://www.news.sina.com.cn"
        url3 = "http://www.sina.com.cn"
        self.assert_(UrlFilter.isSameSuffixWithoutWWW(url1,url2))
        self.assert_(UrlFilter.isSameSuffixWithoutWWW(url1,url3))

    def testIsSameSuffix(self):
        url1 = "http://news.sina.com.cn"
        url2 = "http://www.news.sina.com.cn"
        url3 = "http://sina.com.cn"
        self.assertFalse(UrlFilter.isSameSuffix(url1,url2))
        self.assert_(UrlFilter.isSameSuffix(url1,url3))


if __name__ == '__main__':
    unittest.main()

        



