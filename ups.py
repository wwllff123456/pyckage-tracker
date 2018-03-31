import requests
from bs4 import BeautifulSoup


def ups_package(tracking_number):

    url = "https://wwwapps.ups.com/WebTracking/track?track=yes&trackNums=" + tracking_number
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 ' \
                              '(KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    source_code = s.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    data_table = soup.findAll("table", {"class": "dataTable"})[0]
    data_table_list = []
    item_list_by_row = []
    for each_row in data_table.findAll("tr"):

        for each in each_row.findAll("td"):
            each_item = str(each.string).replace("\n", "").replace("\t", "").replace("\r", "").replace("  ", "")[:100]
            item_list_by_row.append(each_item)

        data_table_list.append(item_list_by_row)
        item_list_by_row = []

    data_table_list.remove([])

    loc_list = []
    dt_list = []
    st_list = []

    for i in range(len(data_table_list)):
        # print(data_table_list[i])
        loc_list.append(str(data_table_list[i][0]).replace("United States", "US"))
        dt_list.append(str(data_table_list[i][1] + " " + data_table_list[i][2]).replace(".", "").lower())
        st_list.append(data_table_list[i][3])

    for i in range(len(st_list)):
        if len(st_list[i]) > 60:
            st_list[i] = st_list[i][:45] + "\n" + st_list[i][45:]
            dt_list[i] += "\n "
            loc_list[i] += "\n "

    # print("========================")
    # print("========================")
    # print("========================")
    #
    # print(dt_list)
    # print("========================")
    # print(st_list)
    # print("========================")
    # print(loc_list)

    return dt_list, st_list, loc_list, url

