import requests
from bs4 import BeautifulSoup


def usps_package(tracking_number):

    url = "https://tools.usps.com/go/TrackConfirmAction?tLabels=" + tracking_number
    s = requests.Session()
    s.headers['User-Agent'] =  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 ' \
                               '(KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    source_code = s.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    def create_list(key_word, limit=35):
        """
        keyword need to be "date-time", "status", or "location".
        """
        list_ = []

        for each_item in soup.findAll("td", {"class": key_word}):
            data = str(each_item.p.string)
            data = data.replace("\t", "").replace("\r", "").replace("\n,", ", ").replace("\n", "")

            if data == "None":
                data=str(each_item.span.string)
                data = data.replace("\t", "").replace("\r", "").replace("\n,", ", ").replace("\n", "")
            elif data == "":
                data = "-"

            list_.append(data[:limit])

        return list_

    dt_list = create_list("date-time")
    st_list = create_list("status", 100)
    loc_list = create_list("location")

    for i in range(len(st_list)):
        if len(st_list[i]) > 60:
            st_list[i] = st_list[i][:45] + "\n" + st_list[i][45:]
            dt_list[i] += "\n "
            loc_list[i] += "\n "

    month_dict = {"january": "Jan.",
                  "february": "Feb.",
                  "march": "Mar.",
                  "april": "Apr.",
                  "may": "May.",
                  "june": "Jun.",
                  "july": "Jul.",
                  "august": "Aug.",
                  "september": "Sep.",
                  "october": "Oct.",
                  "november": "Nov.",
                  "december": "Dec."}

    for i in range(len(dt_list)):
        month = dt_list[i].lower()
        for key in month_dict:
            month = month.replace(key, month_dict[key])
            dt_list[i] = month

    # print(dt_list)
    # print("========================")
    # print(st_list)
    # print("========================")
    # print(loc_list)

    return dt_list, st_list, loc_list, url

