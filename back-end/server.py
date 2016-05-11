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
        'query':{'top':5, 'designName':'love_hate', 'viewName':'general', 'type':'pie', 'args':{'group':'true', 'group_level':'2'}},
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
    },
    {
        'action':'timeLength',
        'title':'Tweet length in accordance with local time',
        'query':{'designName':'time_length', 'viewName':'general', 'type':'line', 'args':{'group':'true', 'group_level':'2'}}     
    },
    {
        'action':'employment',
        'title':'Tweets sentiment in accordance with unemployment rate',
        'queries':[
            {'title':'number of Tweets', 'designName':'Employment', 'viewName':'Multiple%20cities', 'type':'bar', 'args':{'group':'true', 'group_level':'1'}},
            {'title':'number of sentiment Tweets', 'designName':'Employment', 'viewName':'Multiple%20cities%20Sentiment', 'type':'bar', 'args':{'group':'true', 'group_level':'1'}},
            {'title':'number of local positive Tweets', 'designName':'Employment', 'viewName':'Multiple_cities_location_match_positive', 'type':'bar', 'args':{'group':'true', 'group_level':'1'}},
            {'title':'local positive rate from Aurin', 'dbName':'do_not_delete', 'designName':'cty', 'viewName':'local_positive_rate', 'type':'bar', 'args':{}},
            {'title':'positive rate from Aurin', 'dbName':'do_not_delete', 'designName':'cty', 'viewName':'positive_rate', 'type':'bar', 'args':{}},
            {'title':'unemployment rate from Aurin', 'dbName':'do_not_delete', 'designName':'cty', 'viewName':'unemployment_rate', 'type':'bar', 'args':{}}
        ]
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
            scenario.addChart(PieChart(source, data))
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
            scenario.addChart(PieChart(query['title'], data))
        return json.dumps(scenario.reprJSON(), cls=JSONEncoder)

    def timeLength(self, s):
        scenario = Scenario(s['title'])
        f = urllib2.urlopen(getURL(s['query']))
        result = json.loads(f.read())['rows']
        f.close()
        tmp_result = [{row['key'][1]:(row['key'][0],row['value'][2])} for row in result]
        result = {}
        for item in tmp_result:
            key = item.keys()[0]
            arr = result.get(key, [])
            arr.append({item.values()[0][0]:item.values()[0][1]})
            result[key] = arr
        data = {}
        data['values'] = []
        x_label = []
        for city in result.keys():
            d = {}
            d['name'] = city
            values = []
            for row in result[city]:
                values.append(float("%.1f"%row.values()[0]))
            d['values'] = values
            data['values'].append(d)
            x_label = [row.keys()[0] for row in result[city]]
        data['x_label'] = x_label
        scenario.addChart(LineChart(s['title'],data))
        return json.dumps(scenario.reprJSON(), cls=JSONEncoder)

    def employment(self, s):
        scenario = Scenario(s['title'])
        for query in s['queries']:
            f = urllib2.urlopen(getURL(query))
            result = json.loads(f.read())['rows']
            f.close()
            print(result)
            x_label = []
            values = {'name':query['title'], 'values':[]}
            for item in result:
                x_label.append(item['key'])
                values['values'].append(item['value'])
            data = {'x_label': x_label, 'values':values}
            scenario.addChart(BarChart(query['title'], data))
        return json.dumps(scenario.reprJSON(), cls=JSONEncoder)

class PieChart:
    def __init__(self, title, data):
        self.title = title
        self.chartType = "pie"
        self.data = data
        names = []
        for k in data:
            names.append(k['name'])
        self.names = names

    def reprJSON(self):
        return {'title':self.title, 'type':self.chartType, 'names':self.names, 'data':self.data}

class LineChart:
    def __init__(self, title, data):
        self.title = title
        self.chartType = "line"
        self.x_label = data['x_label']
        self.values = data['values']

    def reprJSON(self):
        return {'title':self.title, 'type':self.chartType, 'x_label':self.x_label, 'values':self.values}

class BarChart(LineChart):
    def __init__(self, title, data):
        LineChart.__init__(self, title, data)
        self.chartType = "bar"
        
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
    db_name = queryInfo.get('dbName', DB_NAME)
    url = os.path.join(DB_ADDR+':'+DB_PORT, db_name, '_design', queryInfo['designName'], '_view', queryInfo['viewName'])
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
