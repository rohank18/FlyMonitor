from flask import Flask, jsonify, request
import bs4 as bs
import sys
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

app = Flask(__name__)

City = {'Silchar':'IXS','Delhi':'DEL','Guwahati':'GAU','Hyderabad':'HYD','Bangalore':'BLR','Mumbai':'BOM','Jaipur':'JAI','Kolkata':'CCU'}


class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def main():
    source = "Silchar"
    destination = "Delhi"
    @app.route('/test', methods=['GET', 'POST'])
    def desc():
        source = request.args.get('source')
        destination = request.args.get('destin')
        sCode = City.get(str(source))
        print(source)
        dCode = City.get(destination)
        address='https://in.via.com/flight/search?returnType=one-way&destination={1}&bdestination={1}&destinationL={3}&destinationCity=&destinationCN=&source={0}&bsource={0}&sourceL={2},{2}&sourceCity={2}&sourceCN=India&month=2&day=1&year=2018&date=2/1/2018&numAdults=1&numChildren=0&numInfants=0&validation_result=&domesinter=international&livequote=-1&flightClass=ALL&travType=INTL&routingType=ALL&preferredCarrier=&prefCarrier=0&isAjax=false'.format(sCode,dCode,source,destination)
        print(address)
        page = Page(address)
        soup = bs.BeautifulSoup(page.html, 'html.parser')

        Path = soup.find("div", {"class":"route js-toolTip"})['data-tip']
        sTime = soup.find('div', class_='depTime')
        sChildren = sTime.findChildren()
        dTime = soup.find('div', class_='arrTime')
        dChildren = dTime.findChildren()
        duration = soup.find('div', class_='fltDur')
        durChildren = duration.findChildren()
        flightName = soup.find("div", class_="name js-toolTip")
        price = soup.find("span", class_="price")
        details = {
            'sTime': sChildren[0].text,
            'sCity': sChildren[1].text,
            'stop': durChildren[1].text.strip(),
            'path': Path,
            'dTime': dChildren[0].text,
            'dCity': dChildren[1].text,
            'flightName':flightName.text.strip(),
            'price': price.text
        }
        return jsonify({'Details': details})
        print(details)

    @app.route('/', methods=['GET'])
    def test():
        return jsonify({'Message': 'API is Working'})

    # @app.route('/details', methods=['GET'])
    # def getDetails():
    #     return jsonify({'Details': details})


if __name__== '__main__':
    main()
    app.run()
