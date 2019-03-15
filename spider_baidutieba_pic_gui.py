import os
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import tkinter as tk
from tkinter.filedialog import askdirectory
import tkinter.messagebox

import requests
from bs4 import BeautifulSoup


def getPageUrl(index_url):
    s = 'http://tieba.baidu.com'
    page_list = []
    res = requests.get(index_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    atag = soup.select('a.j_th_tit ')
    for href in atag:
        page_list.append(s + href.attrs['href'])
    return page_list


def getImageUrl(page_url):
    url = []
    res = requests.get(page_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    img_list = soup.select('.BDE_Image')
    if len(img_list) != 0:
        for source in img_list:
            url.append(source.attrs['src'])
    return url


def downloadPictures(url, path):
    title = url.split('/')[-1]
    content = requests.get(url).content
    with open(r'{}\{}'.format(path, title), 'wb') as f:
        f.write(content)


def selectPath():
    path_ = askdirectory()
    path.set(path_)


def main():
    page_url = []
    img_url = []
    path = path_entry.get()
    keyword = name_entry.get()
    pagenum = int(num_entry.get())
    kw = quote(keyword)
    index_url_list = ['http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}'.format(kw, str(i * 50)) for i in range(pagenum)]
    pool = ThreadPoolExecutor()
    for li in pool.map(getPageUrl, index_url_list):
        page_url += li
    for li in pool.map(getImageUrl, page_url):
        img_url += li
    partial_downloadPictures = partial(downloadPictures, path=path)  # 使用偏函数将path传入map
    pool.map(partial_downloadPictures, img_url)
    tk.messagebox.showinfo('提示', '总计{}张图片下载完成'.format(len(img_url)))


if __name__ == '__main__':
    main_window = tk.Tk()
    main_window.title('百度贴吧图片爬虫')
    main_window.geometry('400x300')

    name_label = tk.Label(main_window,
                          text='贴吧名称:',
                          font=('Arial', 15),
                          width=15, height=2
                          )
    name_label.place(x=10, y=20)
    name_entry = tk.Entry(main_window)
    name_entry.place(x=150, y=35)

    num_label = tk.Label(main_window,
                         text='爬取页数:',
                         font=('Arial', 15),
                         width=15, height=2
                         )
    num_label.place(x=10, y=80)
    num_entry = tk.Entry(main_window)
    num_entry.place(x=150, y=95)

    path_label = tk.Label(main_window,
                          text='目标路径:',
                          font=('Arial', 15),
                          width=15, height=2
                          )
    path_label.place(x=10, y=140)
    path = tk.StringVar()
    path_entry = tk.Entry(main_window, textvariable=path)
    path_entry.place(x=150, y=155)
    path_button = tk.Button(main_window, text="路径选择", command=selectPath)
    path_button.place(x=300, y=150)

    det = tk.Button(main_window, text='确定', width=10, command=main)
    det.place(x=50, y=210)

    quit = tk.Button(main_window, text='退出', width=10, command=main_window.quit)
    quit.place(x=250, y=210)

    main_window.mainloop()
