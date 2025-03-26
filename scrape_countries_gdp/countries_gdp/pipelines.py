from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import sqlite3


class CountriesGdpPipeline:
    def process_item(self, item, spider):
        gdp_value = item.get('gdp')  # Use .get() to avoid KeyError

        if gdp_value is None or not isinstance(gdp_value, float):
            raise DropItem(f"Missing or invalid GDP value: {gdp_value}. Item excluded.")

        return item  # Return the item if valid


class RemoveDuplicatesPipeline:

    def __init__(self):
        self.countries_seen = set()

    def process_item(self, item, spider):
        for contry in item['country_name']:
            if item['country_name'] in self.countries_seen:
                raise DropItem(f"Removing Duplicates: {item}. Item excluded.")

            else:
                self.countries_seen.add(item['country_name'])
                return item  # Return the item if valid


class SaveToDatabasePipeline:
    def __init__(self):
        self.con = sqlite3.connect("countries_gdp.db")
        self.cur = self.con.cursor()

    def open_spider(self, spider):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS countries_gdp
            (country_name TEXT PRIMARY KEY,
            gdp REAL,
            year INTEGER)
            """
        )
        self.con.commit()

    def process_item(self, item, spider):
        self.con.execute(""" INSERT INTO countries_gdp (country_name, year, gdp) VALUES(?, ?, ?) """,
                         (item["country_name"], item["year"], item["gdp"]))

        self.con.commit()

    def close_spider(self, spider):
        self.con.close()
