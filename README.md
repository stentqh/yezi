python爬虫所选框架scrapy：

        class ProxyMiddleware(object):                
            def process_request(self, request, spider):
                # 代理服务器(产品官网 www.16yun.cn)
                proxyHost = "t.16yun.cn"
                proxyPort = "31111"

                # 代理验证信息
                proxyUser = "username"
                proxyPass = "password"

                request.meta['proxy'] = "http://{0}:{1}".format(proxyHost,proxyPort)

                # 添加验证头
                encoded_user_pass = base64ify(proxyUser + ":" + proxyPass)
                request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass                    

                # 设置IP切换头(根据需求)
                tunnel = random.randint(1,10000)
                request.headers['Proxy-Tunnel'] = str(tunnel)
java爬虫所选框架jsoup：

{
    // 代理验证信息
    final static String ProxyUser = "username";
    final static String ProxyPass = "password";

    // 代理服务器(产品官网 www.16yun.cn)
    final static String ProxyHost = "t.16yun.cn";
    final static Integer ProxyPort = 31111;

    // 设置IP切换头
    final static String ProxyHeadKey = "Proxy-Tunnel";


    public static String getUrlProxyContent(String url)
    {
        Authenticator.setDefault(new Authenticator() {
            public PasswordAuthentication getPasswordAuthentication()
            {
                return new PasswordAuthentication(ProxyUser, ProxyPass.toCharArray());
            }
        });
        // 设置Proxy-Tunnel
        Random random = new Random();
        int tunnel = random.nextInt(10000);
        String ProxyHeadVal = String.valueOf(tunnel);

        Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress(ProxyHost, ProxyPort));

        try
        {
            // 处理异常、其他参数
            Document doc = Jsoup.connect(url).timeout(3000).header(ProxyHeadKey, ProxyHeadVal).proxy(proxy).get();
