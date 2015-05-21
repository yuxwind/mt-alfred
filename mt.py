import StringIO, gzip, alfred, urllib, urllib2, datetime
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

theQuery = u'{query}'
theQuery = urllib.quote_plus(theQuery)
#url = 'http://dict-co.iciba.com/api/dictionary.php?key=F8B564ADA8E6D4FCB81ACFF2B0BC5478&w=%s' % theQuery
url = 'http://www.meituan.com/s/?w=%s&mtt=1.index%2Fchangecity.0.0.i9xsufr8' % theQuery

request = urllib2.Request(url)
request.add_header('Accept-encoding', 'gzip')
req_open = urllib2.build_opener()
conn = req_open.open(request)
req_data = conn.read()

data_stream = StringIO.StringIO(req_data)
gzip_stream = gzip.GzipFile(fileobj=data_stream)
actual_data = gzip_stream.read()

dict = ET.fromstring(actual_data)
poses = dict.findall('pos')
acceptations = dict.findall('acceptation')

results = []

if len(poses) > 0 :
	index = 0
	for acceptation in acceptations:
		title = acceptation.text
		pattern = poses[index]
		subtitle = pattern.text
		item = alfred.Item({'uid': 1, 'arg' : theQuery}, title, subtitle)
		results.append(item)
		index += 1
else :
	item = alfred.Item({'uid': 1, 'arg' : theQuery}, 'Not Found', '')
	results.append(item)

xml = alfred.xml(results)
alfred.write(xml)
