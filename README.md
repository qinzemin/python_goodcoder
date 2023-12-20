mini_spider for Python_good_coder
===
### Commemorating the Python Good Coder test passed in April 2023
# 项目结构说明：
```
pytest202304目录：
    mini_spider.py: 主程序入口  
    lib目录：存放不同模块的代码  
        config_load.py: 读取配置文件  
        seedfile_load.py: 读取种子文件  
        url_table.py: 构建url管理队列  
        res_table.py: 结果保存队列  
        crawl_thread.py: 实现抓取线程  
        webpage_download.py: 下载网页  
        webpage_parse.py: 对抓取网页的解析  
        webpage_save.py: 将网页保存到磁盘   
    logs目录: 存放日志文件  
    tests目录: 存放单测文件  
        test_config_load.py: 测试配置文件  
        test_parse_url.py: 测试抓取链接  
    conf目录: 存放配置文件  
        spider.conf: 配置文件  
    urls: 种子文件  
    output:输出文件

.gitignore：提交忽略规则
README.md: 说明文档
ci.yml setup.cfg setup.py：持续集成相关文件 
```

# 问题描述：
迷你定向网页抓取器 <br>
在调研过程中，经常需要对一些网站进行定向抓取。 <br>
由于python包含各种强大的库，使用python做定向抓取比较简单。请使用python开发一个迷你定向抓取器mini_spider.py，实现对种子链接的广度优先抓取，并把URL长相符合特定pattern的网页内容（图片或者html等）保存到磁盘上。

# 程序运行：
`python mini_spider.py -c conf/spider.conf`  
# 配置文件说明：
```
[spider] 
url_list_file: ./urls ; 种子文件路径 
output_directory: ./output ; 抓取结果存储目录 
max_depth: 1 ; 最大抓取深度(种子为0级) 
crawl_interval: 1 ; 抓取间隔. 单位：秒 
crawl_timeout: 1 ; 抓取超时. 单位：秒 
target_url: .*\.(html|gif|png|jpg|bmp)$ ; 需要存储的目标网页URL pattern(正则表达式) ,需要考虑兼容抓取html等情况，不止是抓取图片
thread_count: 8 ; 抓取线程数 
```
# 种子文件示例：
种子文件每行一条链接，例如： <br>
http://cup.baidu.com/spider/ <br>
http://www.baidu.com  <br>
http://www.sina.com.cn <br>

