# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from opensearchpy import OpenSearch


class PruebaPipeline:
    def process_item(self, item, spider):
        return item


class ElasticsearchPipeline:
    def __init__(self):
        self.client = OpenSearch(
            hosts=[{"host": "localhost", "port": 9200}],
            http_auth=("admin", "admin"),
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.client.index(index="turism_routes_madrid", body=item)
        return item
