# 说明

该项目仅仅只能用户个人学习使用，不能在商业中使用，若极客时间官方要求该代码仓库删除，请联系我进行删除

## 项目说明

本次项目参考[geek_crawler](https://github.com/etheriousnatsu/geek_crawler),与原项目比较，主要区别如下:

1. 密码输入时不可见
2. 把音频下载到本地
3. 支持下载所有音频课程，或菜单交互式，选择一门课程下载

## 功能

- [✅] 文章及文章内嵌语音下载
- [×] 视频下载

## 运行环境

python3.8.2+

## 依赖包

```bash
pip install aiohttp
```

## 运行

```bash
python main.py # 默认菜单交互式下载
# or
python main.py --mode all # 下载所有的音频课程
```

## 注意

1. 由于网站本身限流，所以太快抓取会被网站拒绝，返回状态码451
