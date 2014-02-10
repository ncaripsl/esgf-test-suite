import configuration as config

from lxml import etree
import urllib
import re

class ThreddsUtils(object):
        def __init__(self):
                #self.config = config.read_config()
                #self.data_node = self.config['nodes']['data_node'];
                self.data_node = "esgf-node.ipsl.fr";


        def get_projects(self):
                url = "http://{0}/thredds/catalog.xml".format(self.data_node);
                content = urllib.urlopen(url).read();
                projects = re.findall(r'"([/A-Za-z0-9_-]*)/catalog.xml"', content);
                for pindex, pname in enumerate(projects):
                        if '/' not in pname:
				format_string = "/thredds/{0}/catalog.xml";
			else:
				format_string = "{0}/catalog.xml";
			projects[pindex] = format_string.format(projects[pindex]);
		return(projects);
			

	def get_datasets(self, projects):
		for pindex, pname in enumerate(projects):
			url = "http://{0}{1}".format(self.data_node, projects[pindex])
                	content = urlib.urlopen(url).read();


	def get_projects2(self):
		url = "http://{0}/thredds/pmip3/catalog.xml".format(self.data_node);
		doc = etree.parse(url);

		#list_tmp=doc.xpath("/catalog/catalogRef")
		#list_tmp=doc.xpath("/*")
		#list_tmp=doc.xpath("/*/*")
		#list_tmp=doc.xpath("/*/*")
		#print "\nlist size=%d"%len(list_tmp)
		#for cr in list_tmp:
		#for cr in doc.xpath("/[local-name()='catalog']", namespaces={'thredds': 'http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0'}):
		for cr in doc.xpath("//ns:catalog/ns:catalogRef",namespaces={'ns':'http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0'}): 
			print "+++";


#		a = etree.tostring(doc);
#		print a;


def test_thredds():
        tu = ThreddsUtils();

	tu.get_projects2();

        #projects = tu.get_projects();
	#datasets = tu.get_datasets(projects)

