import urllib2
from lxml import etree
import multiprocessing
from multiprocessing import Queue
from operator import itemgetter
from StringIO import StringIO

import configuration as config



class ThreddsUtils(object):
        def __init__(self):
		global in_queue 
		in_queue = multiprocessing.JoinableQueue()
		global out_queue
		out_queue = Queue()

		self.config = config.read_config()
		self.data_node = self.config['nodes']['data_node']
		#self.data_node = 'esg.cnrm-game-meteo.fr'
		#self.data_node = 'bmbf-ipcc-ar5.dkrz.de'
		#self.data_node = 'tds.ucar.edu'
		#self.data_node = 'vesg.ipsl.fr'
		#self.data_node = 'cmip-dn1.badc.rl.ac.uk'

	def chunk_it(self, seq, num):
        	avg = len(seq) / float(num)
        	out = []
        	last = 0.0

        	while last < len(seq):
                	out.append(seq[int(last):int(last + avg)])
                	last += avg

        	return out


	def get_files(self, catalogrefs):
		datasetlist = []
		for cr in catalogrefs:
			try:
				content = urllib2.urlopen(cr)
				data = content.read()
			except:
				return datasetlist
			
			services_def = {}
			context = etree.iterparse(StringIO(data), tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}service')
			for events, sv in context:
				if sv.get('serviceType') != 'Compound':
					services_def.update({sv.get('name'):sv.get('serviceType')})

			context = etree.iterparse(StringIO(data), tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataset')
			for events, ds in context:
				if ds.get('urlPath'):
					dataset = []
					dataset.append(ds.get('urlPath'))

					if "aggregation" in ds.get('urlPath'):
						dataset.append(float('inf'))
					else:
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

					ds_services = []
					for sv in ds.iterchildren(tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}serviceName'):
                                        	ds_services.append(services_def[sv.text])
					for acc in ds.iterchildren(tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}access'):
						try:
							ds_services.append(services_def[acc.get('serviceName')])
						except:
							pass
					dataset.append(ds_services)
					datasetlist.append(dataset)
		return datasetlist

	def worker(self, catalogrefs):
		datasetlist = []
			
		#

		return self.get_files(catalogrefs)

	def queue_manager(self):
		for item in iter(in_queue.get, None):
			out_queue.put(self.worker(item))
			in_queue.task_done()
		in_queue.task_done()

	def map_mprocesses(self, catalogrefs):
		
		processes = []

		for i in catalogrefs:
			processes.append(multiprocessing.Process(target=self.queue_manager))
			processes[-1].daemon = True
			processes[-1].start()

		for cr in catalogrefs:
			in_queue.put(cr)

		in_queue.join()

		for p in processes:
			in_queue.put(None)

		reslist = []
		for p in processes:
			reslist.extend(out_queue.get())

		in_queue.join()

		for p in processes:
			p.join()

		return reslist

	def get_catalogrefs(self):
        	url = "http://{0}/thredds/esgcet/catalog.xml".format(self.data_node);
        	content = urllib2.urlopen(url)
        	doc = etree.iterparse(content, events=('end',), tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}catalogRef')
        	catalogrefs = []
        	for event, cr in doc:
        		path = cr.get('{http://www.w3.org/1999/xlink}href')
        		if ".mon." in path:
        			catalogrefs.append("http://{0}/thredds/esgcet/{1}".format(self.data_node, path))
        	return catalogrefs


	def get_endpoints(self):

		nb_processes = multiprocessing.cpu_count() * 16

		catalogrefs = self.get_catalogrefs()
		catalogrefs = self.chunk_it(catalogrefs, nb_processes)
		
		res = self.map_mprocesses(catalogrefs)

		res = [i for i in res if 'HTTPServer' in i[2]]
		print min(res,key=itemgetter(1))

def test_thredds():
        tu = ThreddsUtils()
	catalogrefs = tu.get_endpoints()
