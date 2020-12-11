python爬虫所选框架scrapy：

       
java爬虫所选框架jsoup：

            // 处理异常、其他参数
            Document doc = Jsoup.connect(url).timeout(3000).header(ProxyHeadKey, ProxyHeadVal).proxy(proxy).get();
