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
		out_queue = multiprocessing.Queue()

		self.config = config.read_config()
		self.data_node = self.config['nodes']['data_node']

	def chunk_it(self, seq, num):
        	avg = len(seq) / float(num)
        	out = []
        	last = 0.0

        	while last < len(seq):
                	out.append(seq[int(last):int(last + avg)])
                	last += avg

        	return out

	def get_dataset_size(self, dataset):
		# Set aggregations size to inf
		if "aggregation" in dataset.get('urlPath'):
			size = float('inf')
		else:
			for si in dataset.iterchildren(tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataSize'):
				units = si.get('units')
				if units == 'Kbytes':
                        		size = float(si.text) / 1024
                        	elif units == 'Mbytes':
                        		size = float(si.text)
                        	elif units == 'Gbytes':
                                	size = float(si.text) * 1024
                        	else:
                        		size = float('inf')
		return size


	def get_dataset_list(self, data, services_def):
		dataset_list = []
		# Parsing datasets
		doc = etree.iterparse(StringIO(data), tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}dataset')
		for events, ds in doc:
			
			# Only if dataset is requestable
			if ds.get('urlPath'):
				dataset = []
				dataset.append(ds.get('urlPath'))

                                dataset.append(self.get_dataset_size(ds))

                                ds_services = []
                                for sv in ds.iterchildren(tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}serviceName'):
                                	ds_services.append(services_def[sv.text])
                                for acc in ds.iterchildren(tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}access'):
                                	try:
                                        	ds_services.append(services_def[acc.get('serviceName')])
                                        except:
                                        	pass
                                dataset.append(ds_services)
                                dataset_list.append(dataset)
		return dataset_list
	

	def get_services_def(self, data):
		services_def = {}
		doc = etree.iterparse(StringIO(data), tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}service')
		for events, sv in doc:
                	if sv.get('serviceType') != 'Compound':
                        	services_def.update({sv.get('name'):sv.get('serviceType')})
		return services_def

	def worker(self, catalogrefs):
		for cr in catalogrefs:
			try:
				content = urllib2.urlopen(cr)
				data = content.read()
			except:
				continue	
			services_def = self.get_services_def(data)
			dataset_list = self.get_dataset_list(data, services_def)
		return dataset_list

	def queue_manager(self):
		for item in iter(in_queue.get, None):
			out_queue.put(self.worker(item))
			in_queue.task_done()
		in_queue.task_done()

	def map_processes(self, chunks):
		# Starting nb_chunk processes calling the queue manager
		processes = []
		for i in chunks:
			processes.append(multiprocessing.Process(target=self.queue_manager))
			processes[-1].daemon = True
			processes[-1].start()

		# Feeding the input queue with chunks
		for cr in chunks:
			in_queue.put(cr)

		# Waiting for everything to be processed
		in_queue.join()

		# Feeding the input queue with None to be sure
		for p in processes:
			in_queue.put(None)

		# Collecting results from output queue
		reslist = []
		for p in processes:
			reslist.extend(out_queue.get())

		return reslist

	def get_catalogrefs(self):
        	url = "http://{0}/thredds/esgcet/catalog.xml".format(self.data_node);
        	content = urllib2.urlopen(url)
		
		# Parsing catalogRef xml entries
        	doc = etree.iterparse(content, events=('end',), tag='{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}catalogRef')
        	catalogrefs = []
        	for event, cr in doc:
			# Keeping monthly ones only 
        		path = cr.get('{http://www.w3.org/1999/xlink}href')
        		if ".mon." in path:
        			catalogrefs.append("http://{0}/thredds/esgcet/{1}".format(self.data_node, path))
        	return catalogrefs


	def get_endpoints(self):
		# Determining number of processes and chunks
		nb_chunks = multiprocessing.cpu_count() * 16

		# Getting and chunking catalogrefs href links from http://my-data-node/thredds/esgcet/catalog.xml
		catalogrefs = self.get_catalogrefs()
		chunked_catalogrefs = self.chunk_it(catalogrefs, nb_chunks)
		
		# Starting multiprocessed work
		res = self.map_processes(chunked_catalogrefs)

		res = [i for i in res if 'HTTPServer' in i[2]]
		print min(res,key=itemgetter(1))

def test_thredds():
        tu = ThreddsUtils()
	catalogrefs = tu.get_endpoints()
