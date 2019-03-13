import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import os


# 文件名里不能有l中的特殊符号需要删除
def amendName(s):
    '''adjust string s to meet the
    demand of Windows file naming.
'''
    name = ''
    l = ['<', '>', '/', '\\', '|', ':', '\"', '*', '?']
    for i in s:
        if i not in l:
            name += i
    return name


# 下载某个帖子内的图片
def downloadPictures(url, headers, path):
    '''download all the pictures in a single subpage.'''
    res = requests.get(url, params=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    titlelist = soup.select('.core_title_txt')  # 取带有标题名的元素
    if len(titlelist) != 0:  # 判断是否存在该标签
        title = amendName(titlelist[0].attrs['title'])
    count = 0
    imglist = soup.select('.BDE_Image')  # 取img标签
    if len(imglist) != 0:
        for source in imglist:
            url = source.attrs['src']
            content = requests.get(url, params=headers).content
            count += 1
            if title != '':
                with open(r'{}\{}-{}.jpg'.format(path, title, count), 'wb') as f:
                    print('Now downloading {}-{}.'.format(title, count))
                    f.write(content)
    return count


# 获取一整个页面内帖子的url
def retrieveUrl(indexurl, headers):
    '''retrieve all the link from the index.'''
    s = 'http://tieba.baidu.com'
    hreflist = []
    res = requests.get(indexurl, params=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    atag = soup.select('a.j_th_tit ')  # 取a标签中的链接
    for href in atag:
        hreflist.append(s + href.attrs['href'])  # 拼接字符串
    return hreflist


headers = {
    'Cookie': '[用户cookie]',
    'Host': 'tieba.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

if __name__ == '__main__':
    '''It can crawl picture of any page from any baidu teiba.'''
    picnum = 0
    hreflist = []
    cur = os.path.abspath(os.curdir)
    while True:
        path = input('请输入保存图片的文件夹名：')
        path = cur + '\\' + path
        if not os.path.exists(path):
            os.mkdir(path)
            break
        else:
            print('文件夹已存在，请重新输入文件名！')
    keyword = input('请输入吧名：')
    pagenum = input('请输入爬取的页数：')
    kw = quote(keyword)  # quote函数用于处理keyword中的中文字符
    for i in range(int(pagenum)):
        indexurl = 'http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(kw, str(i * 50))
        hreflist += retrieveUrl(indexurl, headers)
    hreflist = set(hreflist)
    for href in hreflist:
        picnum += downloadPictures(href, headers, path)
    print('{} pictures were totally downloaded'.format(picnum))
