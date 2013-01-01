import os
import sys
import fnmatch

interesting_types = ['jpg', 'jpeg', 'gif', 'bmp', 'png', 'ogg', 'wav']
def get_interesting_files(path):
    result = []
    for path, dirs, files in os.walk(path):
        for file in files:
            for interesting_type in interesting_types:
                if fnmatch.fnmatch(file.lower(), r'*.'+interesting_type):
                    result.append(os.path.join(path, file))
    return result

types = ['image', 'audio', 'other']
def get_type_by_ext(file):
	for interesting_type in interesting_types[0:5]:
		if fnmatch.fnmatch(file.lower(), r'*.'+interesting_type):
			return types[0]
		
	for interesting_type in interesting_types[5:7]:
		print interesting_type
		if fnmatch.fnmatch(file.lower(), r'*.'+interesting_type):
			return types[1]
		
	return types[2]
			
class ResourceLoader(object):
    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.cache = [Resource(file) for file in get_interesting_files(self.path)]
        
    def load_resources_by_name(self, name):
        return [res for res in self.cache if res.name == name]
    
    def load_resources_by_type(self, type):
        return [res for res in self.cache if res.type == type]
       
    def load_resource_by_name_and_type(self, name, type):
        return [res for res in self.cache if name == name and res.type == type][0]
    
class Resource(object):
    def __init__(self, path):
    	# two are here on purpose: use path or filepath interchangably
        self.path = path
        self.filepath = self.path
        
        self.name, self.extension = os.path.basename(path).split('.')
        self.type = get_type_by_ext(path)