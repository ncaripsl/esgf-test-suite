import urllib2
from lxml import etree
import multiprocessing
from multiprocessing import Queue
from operator import itemgetter

import configuration as config



class ThreddsUtils(object):
        def __init__(self):
		global q 
		q = multiprocessing.JoinableQueue()
		global out_q
		out_q = Queue()
		self.config = config.read_config()
		self.data_node = self.config['nodes']['data_node']

	def chunkIt(self, seq, num):
        	avg = len(seq) / float(num)
        	out = []
        	last = 0.0

        	while last < len(seq):
                	out.append(seq[int(last):int(last + avg)])
                	last += avg

        	return out


	def get_files(self, catalogrefs):
		res = []
		for cr in catalogrefs:
			try:
				content = urllib2.urlopen(cr)
			except:
				return res
			context = etree.iterparse(content, events=('end',), tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataset')
			for event, ds in context:
				if ds.get('urlPath') and  "aggregation" not in ds.get('urlPath'):
					dataset = []
					dataset.append(ds.get('urlPath'))
					for si in ds.iterchildren(tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataSize'):
						units = si.get('units')
						if units == 'Kbytes':
							size = float(si.text) / 1024
						elif units == 'Mbytes':
							size = float(si.text)
						elif units == 'Gbytes':
							size = float(si.text) * 1024
						else:
							size = float('inf')
						dataset.append(size)
					for sv in ds.iterchildren(tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}serviceName'):
                                        	dataset.append(sv.text)
					for acc in ds.iterchildren(tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}access'):
						dataset.append(acc.get('serviceName'))
					res.append(tuple(dataset))
		return res

	def worker(self):
		for item in iter(q.get, None):
			out_q.put(self.get_files(item))
			q.task_done()
		q.task_done()


	def get_catalogrefs(self):

		nb_procs = 32

		url = "http://{0}/thredds/esgcet/catalog.xml".format(self.data_node);
		content = urllib2.urlopen(url)
		context = etree.iterparse(content, events=('end',), tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}catalogRef')
		urllist = []
		for event, cr in context:
                        path = cr.get('{http://www.w3.org/1999/xlink}href')
                        urllist.append("http://{0}/thredds/esgcet/{1}".format(self.data_node, path))
		chunk =  self.chunkIt(urllist, nb_procs)

		procs = []
		for i in range(nb_procs):
			procs.append(multiprocessing.Process(target=self.worker))
			procs[-1].daemon = True
			procs[-1].start()

		for num in range(nb_procs):
			q.put(chunk[num])

		q.join()

		for p in procs:
			q.put( None )

		reslist = []
		for k in procs:
			reslist.extend(out_q.get())

		q.join()


		for p in procs:
			p.join()

		print min(reslist,key=itemgetter(1))

def test_thredds():
        tu = ThreddsUtils()
	catalogrefs = tu.get_catalogrefs()
