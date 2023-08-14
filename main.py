# main_program.py
from scrape_website import scrape_website
from comparison_data import compare_data

def main():
    # 调用爬取网站的函数
    scrape_website()

    # 调用比较数据的函数
    compare_data()

if __name__ == "__main__":
    main()
