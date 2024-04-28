# @Author:  zcp
# @Date: 2024-04-22 14:00:00

# # -*- coding:utf-8 -*-

# 同步（速度慢）
# import requests
# import httpx
# import os
# import sys

# class getvideo(object):
#   def __init__(self) -> None:
#     self.baseurl = 'https://v91.sxzyhuij.com/ts/'  # ts视频的路径
#     self.m3u8url = 'https://v91.pe12369.com/202404/24/D0xQ1qsp5915/video/2000k_0X1080_64k_25/hls/index.m3u8' # m3u8文件的路径
#     self.ts_video = [] # 存放解析后的ts视频信息

#   '''
#     获取m3u8文件中的ts分片信息
#   '''
#   def geturlbyts(self):
#     res = requests.get(self.m3u8url)
#     m3u8_obj = res.text 
#     m3u8 = m3u8_obj.split('\n')
#     self.ts_video = [s for s in m3u8 if s.endswith('.ts')]


#   '''
#     下载ts分片视频
#   '''
#   def downloadvideobyts(self):
#     for i, url in enumerate(self.ts_video):
#       if url.startswith('https'):
#         url = url
#       else:
#         url = self.baseurl + url
#       response = requests.get(url, stream=True)
      
#       if os.path.exists(f'video/{i}.ts'):
#         continue
#       with open(f'video/{i}.ts', 'wb') as out_file:
#         sys.stdout.write("下载进度:{0:.2f}%" .format(float((i+1)/len(self.ts_video))*100)  + '\r')
#         sys.stdout.flush()
#         out_file.write(response.content)

#   '''
#     合并分片得到完整的视频
#   '''
#   def mergevideo(self):
#     file_names = os.listdir('video')
#     target_video = open('output.mp4','ab')
#     for file in file_names:
#       with open('./video/'+file,"rb") as f:
#         print("当前合并到{}".format(file))
#         target_video.write(f.read())
#       f.close()
#     target_video.close()


import asyncio
import os
import sys
import httpx
from httpx import AsyncClient

class GetVideo(object):
    def __init__(self, download_url : str, base_url : str = None, max_concurrency_num : int = 10) -> None:
        self.m3u8url = download_url
        self.baseurl = base_url if base_url is not None else "/".join(download_url.split('/')[:-1])
        self.max_concurrency_num = max_concurrency_num
        self.ts_video = []

    '''
    获取m3u8文件中的ts分片信息
    '''
    def get_url_by_ts(self) -> None: 
        response = httpx.get(self.m3u8url)
        m3u8_obj = response.text 
        m3u8 = m3u8_obj.split('\n')
        self.ts_video = [s for s in m3u8 if s.endswith('.ts')]

    '''
    下载ts分片视频
        args:
            session: httpx.AsyncClient
            url: str
            index: int
        return: None
    '''
    async def download_video_by_ts(self, session : AsyncClient, url : str, index : int) -> None:
        if url.startswith('https'):
            url = url
        else:
            url = self.baseurl + url
        try:
          if os.path.exists(f'video/{index}.ts'):
                return
          async with session.stream("GET", url) as response:
            with open(f'video/{index}.ts', 'wb') as out_file:
                async for chunk in response.aiter_bytes():
                  out_file.write(chunk)
          sys.stdout.write("下载进度:{0:.2f}%" .format(float((index+1)/len(self.ts_video))*100)  + '\r')
          sys.stdout.flush()
        except httpx.TimeoutException:
            print(f"下载超时：{url}")

    '''
    合并分片得到完整的视频
    '''
    def merge_video(self) -> None:
        file_names = os.listdir('video')
        file_names.sort(key=lambda x: int(x.split('.')[0]))
        os.makedirs('video', exist_ok=True)
        target_video = open('output_video/惜花芷40.mp4', 'ab')
        for file in file_names:
            with open('./video/' + file, "rb") as f:
                print(len(file_names))
                target_video.write(f.read())
                f.close()
            sys.stdout.write("当前合并进度:{0:.2f}%" .format(float((int(file.split('.')[0]) +1) / len(file_names) * 100)))
            sys.stdout.flush()
        target_video.close()

    '''
    下载ts分片视频并合并
    '''
    async def download_and_merge(self) -> None:
        limits = httpx.Limits(max_connections=self.max_concurrency_num, max_keepalive_connections=self.max_concurrency_num)  # 设置最大连接数和最大保持连接数为10
        async with httpx.AsyncClient(limits=limits, timeout=120) as client:
            tasks = []
            for index, url in enumerate(self.ts_video):
                tasks.append(self.download_video_by_ts(client, url, index))
            await asyncio.gather(*tasks)
        self.merge_video()
        self.clear_folder('video')
        
        
    '''
    清空文件夹
    '''  
    def clear_folder(self,folder_path : str) -> None:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)


if __name__ == '__main__':
    download_url = input("请输入m3u8文件的url:")
    base_url = input("请输入ts视频的url(如果没有特殊地址直接回车):")
    max_concurrency_num = int(input("请输入最大并发数(如果采用默认配置可以直接回车):"))
    dl_video = GetVideo(download_url=download_url, base_url=base_url)
    dl_video.get_url_by_ts()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(dl_video.download_and_merge())
