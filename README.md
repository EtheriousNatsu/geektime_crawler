# 说明
该项目仅仅只能用户个人学习使用，不能在商业中使用，若极客时间官方要求该代码仓库删除，请联系我进行删除

# 项目说明
本次项目参考[geek_crawler](https://github.com/zhengxiaotian/geek_crawler),与原项目比较，主要区别如下:
1. 项目代码结构更加清晰
2. 基于aiohttp

# 功能
- [✅] 文章及文章内嵌语音下载
- [×] 视频下载

# 运行环境
python3.8.2+

# 依赖包
```bash
pip install aiohttp
```

# 运行
```bash
python main.py
```

# 注意
1. 由于网站本身限流，所以太快抓取会被网站拒绝，返回状态码451
