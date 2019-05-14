# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DemoPipeline(object):
    def process_item(self, item, spider):
        url = item['url'][0]
        title = item['title'][0]
        timeT = item['time'][0]
        source = item['source'][0]
        img = item['img'][0]
        content = item['content']
        print(content)
        # 如title中有杂乱的空格和\r\n数据
        title = title.replace(' ', '').replace('\r\n', '')
        # 如需要将时间转换成时间戳存储
        from datetime import datetime
        import time
        datetimeTime = datetime.strptime(str(timeT).replace(' ', ''), '%Y-%m-%d%H:%M:%S')
        timestampTime = time.mktime(datetimeTime.timetuple())
        return item
