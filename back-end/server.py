import BaseHTTPServer, re, urllib, urllib2, os, json, operator

PORT = 8080
DB_ADDR = 'http://115.146.89.147'
DB_PORT = '5984'
DB_NAME = 'aus_tweets'

RouteArray = [
    {'regexp': r'^/$', 'controller': 'HomeController', 'action': 'indexAction'},
    {'regexp': r'^/\d+$', 'controller': 'ScenarioController', 'action': 'contentAction'},
]

ScenarioArray = [
    {
        'action':'sourceSentiment',
        'title':'Sentiment stats from top 5 Tweet sources',
        'query':{'top':5, 'designName':'love_hate', 'viewName':'general', 'type':'bar', 'args':{'group':'true', 'group_level':'2'}},
    },
    {
        'action':'regionLang',
        'title':'Language distribution in different Australian cities',
        'queries':[
            {'title':'Adelaide', 'designName':'region_lang', 'viewName':'general', 'type':'pie', 'args':{'group':'true', 'group_level':'2', 'startkey':'["Adelaide"]', 'endkey':'["Adelaide", {}]'}},
            {'title':'Brisbane', 'designName':'region_lang', 'viewName':'general', 'type':'pie', 'args':{'group':'true', 'group_level':'2', 'startkey':'["Brisbane"]', 'endkey':'["Brisbane", {}]'}},
            {'title':'Melbourne', 'designName':'region_lang', 'viewName':'general', 'type':'pie', 'args':{'group':'true', 'group_level':'2', 'startkey':'["Melbourne"]', 'endkey':'["Melbourne", {}]'}},
            {'title':'Perth', 'designName':'region_lang', 'viewName':'general', 'type':'pie', 'args':{'group':'true', 'group_level':'2', 'startkey':'["Perth"]', 'endkey':'["Perth (WA)", {}]'}},
            {'title':'Sydney', 'designName':'region_lang', 'viewName':'general', 'type':'pie', 'args':{'group':'true', 'group_level':'2', 'startkey':'["Sydney"]', 'endkey':'["Sydney", {}]'}}]
    }
]

class Controller(object):
    def __init__(self, server):
        self.__server = server

    @property
    def server(self):
        return self.__server

class Router(object):
    def __init__(self, server):
        self.__routes = []
        self.__server = server

    def addRoute(self, regexp, controller, action):
        self.__routes.append({'regexp': regexp, 'controller': controller, 'action': action})

    def route(self, path):
        for route in self.__routes:
            if re.search(route['regexp'], path):
                cls = globals()[route['controller']]
                func = cls.__dict__[route['action']]
                obj = cls(self.__server)
                apply(func, (obj, ))
                return
        self.__server.send_response(404)
        self.__server.end_headers()

class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        routes = RouteArray
        self.__router = Router(self)
        for route in routes:
            self.__router.addRoute(route['regexp'], route['controller'], route['action'])
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        self.__router.route(self.path)

class HomeController(Controller):
    def __init__(self, server):
        Controller.__init__(self, server)

    def indexAction(self):
        self.server.send_response(200)
        self.server.send_header('Content-Type', 'application/json')
        self.server.end_headers()
        self.server.wfile.write('{"Content": ["hello", "world"]}')

class ScenarioController(Controller):
    def __init__(self, server):
        Controller.__init__(self, server)

    def contentAction(self):
        m = re.match(r'^/(\d+)$', self.server.path)
        index = int(m.group(1))
        if index > len(ScenarioArray) or index < 0:
            self.server.send_response(404)
            self.server.end_headers()
            return
        
        scenario = ScenarioArray[index-1]
        func = ScenarioController.__dict__[scenario['action']]
        result = apply(func, (self, scenario))
        
        self.server.send_response(200)
        self.server.send_header('Content-Type', 'application/json')
        self.server.send_header("Access-Control-Allow-Origin","*")
        self.server.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin")
        self.server.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.server.end_headers()
        self.server.wfile.write(result)

    def sourceSentiment(self, s):
        scenario = Scenario(s['title'])
        f = urllib2.urlopen(getURL(s['query']))
        result = json.loads(f.read())
        f.close()
        sum_dict = {}
        for k in result['rows']:
            sum_dict[k['key'][0]] = sum_dict.get(k['key'][0], 0) + k['value']
        top = min(s['query']['top'], len(sum_dict.keys()))
        topSources = [k for k, v in sorted(sum_dict.items(), key=operator.itemgetter(1), reverse=True)[:top]]
        for source in topSources:
            data = []
            for row in result['rows']:
                if source in row['key']:
                    data.append({'name':row['key'][1], 'value':row['value']})
            scenario.addChart(Chart(source, s['query']['type'], data))
        return json.dumps(scenario.reprJSON(), cls=JSONEncoder)

    def regionLang(self, s):
        scenario = Scenario(s['title'])
        for query in s['queries']:
            f = urllib2.urlopen(getURL(query))
            result = json.loads(f.read())
            f.close()
            result = {k['key'][1]:k['value'] for k in result['rows']}
            total = float(sum(result.values()))
            minorities = {k:v for k, v in result.iteritems() if v/total < 0.001}
            majorities = {k:v for k, v in result.iteritems() if v/total >= 0.001}
            other = sum(minorities.values())
            majorities['other'] = other
            data = []
            for k, v in majorities.iteritems():
                data.append({'name': k, 'value': v})
            scenario.addChart(Chart(query['title'], query['type'], data))
        return json.dumps(scenario.reprJSON(), cls=JSONEncoder)

class Chart:
    def __init__(self, title, chartType, data):
        self.title = title
        self.chartType = chartType
        self.data = data
        names = []
        for k in data:
            names.append(k['name'])
        self.names = names

    def reprJSON(self):
        return {'title':self.title, 'type':self.chartType, 'names':self.names, 'data':self.data}

class Scenario:
    def __init__(self, title):
        self.title = title
        self.charts = []

    def addChart(self, chart):
        self.charts.append(chart)

    def reprJSON(self):
        return {'title':self.title, 'charts':self.charts}

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


def getURL(queryInfo):
    url = os.path.join(DB_ADDR+':'+DB_PORT, DB_NAME, '_design', queryInfo['designName'], '_view', queryInfo['viewName'])
    params = urllib.urlencode(queryInfo['args'])
    return '%s?%s' % (url, params)

def main():
    httpd = BaseHTTPServer.HTTPServer(('', PORT), MyRequestHandler)
    try:
        httpd.serve_forever()
    except:
        httpd.socket.close()
        pass

if __name__ == '__main__':
    main()
