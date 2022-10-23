# epub-crawler

寫了一些爬小說的工具，有幾種功能：

-   [爬小說](#爬小說)
-   [爬完轉 epub](#爬完轉-epub)
-   [中文數字轉阿拉伯數字](#中文數字轉阿拉伯數字)
-   [txt 轉 epub](#txt-轉-epub)

## 爬小說

```shell
$ scrapy runspider \
  -a website=czbooks2 \
  -a novelId=c77d63 \
  src/spiders/novel.py
```

可使用的網站：

-   `69shu`
-   `wfxs`
-   `czbooks`
-   `czbooks2` 和 `czbooks` 一樣，只是使用第一行作為標題
-   `zgdyjz`
-   `twfanti`
-   `fantinovels`

其他參數：

-   `novelId`
-   `limit` 爬幾章
-   `offset` 忽略前幾章
-   [`src/setting.py`](src/setting.py) 裡的 `DOWNLOAD_DELAY` 預設使用 0.5 秒，代表每秒只會爬兩個頁面，爬蟲是要講武德的？

## 爬完轉 epub

爬完的資料預設會放進 `data/result.jl`，這時這個 jl 檔就可以轉成 epub 囉。

需要先安裝：

-   [`opencc`](http://opencc.byvoid.com) 幫你把簡體中文轉成繁體中文
-   [`pandoc`](https://pandoc.org) 幫你把 txt 轉成 epub

```shell
$ tree .
.
├── data
│   └── result.jl
└── to-epub.sh
$ bash to-epub.sh data/result 妖刀記
$ tree .
.
├── data
│   ├── result.txt
│   └── result.jl
├── to-epub.sh
└── 妖刀記.epub
```

## 中文數字轉阿拉伯數字

有時標題會有中文數字，這樣到時候在排序的時候會沒辦法根據章節去排序，這時你可以使用 `trans-ch-num.py`：

```shell
python src/trans-ch-num.py input-file.jl output-file.jl '章'
```

> 第三個參數要是數字後的第一個字元

上述 `input-file.jl` 格式可能為：

```jl
{"title": "第十一章：名字", "content":"..."}
{"title": "第一章：你的", "content":"..."}
```

輸出的結果（`output-file.jl`）就會是：

```jl
{"title": "第11章：名字", "content":"..."}
{"title": "第1章：你的", "content":"..."}
```

這時你就可以排序他：

```shell
$ sort --version-sort output-file.jl
{"title": "第1章：你的", "content":"..."}
{"title": "第11章：名字", "content":"..."}
```

## txt 轉 epub

特定格式的 TXT 檔會轉成 ePub 前置的 TXT，需要再透過 [`pandoc`](https://pandoc.org) 轉成真正的 epub

```shell
$ tree .
.
├── src
│   └── text-to-epub.py
└── my-file.txt
$ python src/text-to-epub.py my-file
$ tree .
.
├── src
│   └── text-to-epub.py
├── my-file.txt
└── my-file.epub.txt
$ pandoc -o my-file.epub my-file.epub.txt
$ tree .
.
├── src
│   └── text-to-epub.py
├── my-file.txt
├── my-file.epub.txt
└── my-file.epub
```
