## 本项目只是一个简单的网络视频爬取项目（支持m3u8视频文件的下载）

### 注意：

- 项目仅供了解使用
- 项目只支持未加密的数据流进行视频爬取，并未涉及到加密数据流视频爬取
- 目前只是单个视频爬取，如需批量进行爬取，可自行修改，创建多个下载对象进行视频下载

<hr>

### 功能：

- m3u8视频下载
- 采用`asyncio协程`和`httpx请求库`，支持异步视频爬取加快下载速度
- 可自选择输入最大的异步并发数，默认为10

<hr>

### 使用:

- 运行m3u8.py文件
- 输入要爬取的视频m3u8文件路径
  - 获取文件路径
    - 第一步，访问你要下载的视频网址，按f12打开开发者模式
    - ![第二步](/img/second.png)
    - ![第三步](/img/thrid.png)
- 输入ts分片文件路径（默认会从m3u8文件路径中进行截取）
- 输入最大并发数量（默认为10）







