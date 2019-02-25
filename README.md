# 五条(FIVE-LINKS)

## 阅读五条

Visit https://gitpress.io/c/FIVE-LINKS to read articles

访问 https://gitpress.io/c/FIVE-LINKS 阅读文章，或者微信搜索公众号 `iamlyricw` 关注。


## 生成五条

生成无样式 HTML 文件

```bash
$ ./gears/process.py -t html -f ./source/2018/2018.07.26.md 
```

生成微信公众号排版 HTML 文件

```bash
$ ./gears/process.py -t wx -f ./source/2018/2018.07.26.md 
```

根据 Markdown 里独占一行的链接生成 QrCode

```bash
$ ./gears/process.py -m qr -f ./source/2018/2018.07.26.md 
```

如果要在微信加 QrCode，需要自己手工去 dist 目录编辑 index.html

## 为啥不定制 render

因为懒...

