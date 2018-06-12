import sys, json, requests, re

class RSSParser(object):
    items_regex = re.compile('<item.*?>(.*?)<\/item>', re.S)

    def parse(self, response, params):
        details = {}
        for param in params:
            details[param] =  re.compile('<{}.*?>(.*?)<\/{}>'.format(param, param), re.S)
        tmpItems = self.items_regex.findall(response)
        for tmpItem in tmpItems:
            print(tmpItem)
        items = []
        for tmpItem in tmpItems:
            dict = {}
            for param in params:
                dict[param] = details[param].search(tmpItem).group(1)
            items.append(dict)
        return items

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise Exception('The format is: python rss-parser.py <url>')

        url = sys.argv[1]
        response = requests.get(url).text

        parser = RSSParser()
        params = ["title", "link", "pubDate"]
        print(json.dumps(parser.parse(response, params)))
    except Exception as e:
        print('Error: %s' % e.message)
