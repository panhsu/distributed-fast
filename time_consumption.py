
import ConfigParser
import os
import re
 
class record_time_consumption(ConfigParser.ConfigParser):
    time_consumtion = {}
    dict_time_cost = {}
	
    
 
    def as_dict(self):
        def upper_kdict(d):
            r = {}
            for k, v in d.items():
                K = k.upper()+"-"
                r[K] = v if not r.__contains__(K) else v + r[K]
            return r
        
        d = dict(self._sections)
        for k in d: 
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
            d[k] = upper_kdict(d[k])
        self.dict_time_cost = d
        return d 
		
    def get_dict_time_cost(self):
        return self.dict_time_cost
		
    def pa_reportfiles_to_ini(self,dir_path,filelist):
    	dict_cases_timecost = {}
        section = re.match("(.*)\-(.*)\-(.*).log",filelist[0]).group(2)
        self.time_consumtion.update({section:dict_cases_timecost})
        #dict_cases_timecost = self.time_consumtion[section]
        #print self.time_consumtion
        for f in filelist:
            full_filepath = os.path.join(dir_path,f)
            with open(full_filepath,'r') as rf:
                for line in rf.readlines(): 
                    
                    m = re.match("\[(.*)\-(\d*)\]\s*\[(\d+)\]\s*\[(.*)\]",line)
                    if not (m is None):
                    	#print line
                        case_id = m.group(1)
                        cost_time = m.group(3)
                        n = re.match("(.*)\-(\d*)",case_id)
                        if not (n is None):
                            case_id = n.group(1)
                     
                        if case_id in dict_cases_timecost.keys():
                            cost = dict_cases_timecost[str(case_id)] 
                            cost_time = int(cost)+ int(cost_time)
                        
                        dict_cases_timecost.update({str(case_id).upper():int(cost_time)})
        return self.time_consumtion


    def save_as_ini(self,ini_file,d):
        config = ConfigParser.RawConfigParser()
        for section in d.keys():
            config.add_section(section)
            dict_items = d[section]
            for cid in dict_items.keys():
                #print section,cid,dict_items[cid]
                config.set(section,cid,dict_items[cid])
        with open(ini_file,'w') as configfile:
            config.write(configfile)

    def get_optimize_caseslist(self,d,workers_count,cases_id,section_name):
        
        
        dict_items = dict([a, int(x)] for a, x in d[section_name].iteritems())
        total_config_cid_count = len(dict_items)
        total_cids_count = len(cases_id)
        cid_list = []
        opt_dict = {}
        avg_cid_num =  total_cids_count / workers_count 
        sorted_tuple = sorted(dict_items.items(),  key=lambda p: int(p[1]))
        sorted_cid_list = [ cid for (cid, cost) in sorted_tuple]
        cid_not_in_list= list(set(cases_id) - set(sorted_cid_list))
        cid_extra_in_config = list(set(sorted_cid_list)-set(cases_id))
        cid_list = list(set(sorted_cid_list) - set(cid_extra_in_config))
        cid_not_in_list_counts = len(cid_not_in_list)
        avg_best_cost = sum(dict_items.itervalues()) / workers_count
        print avg_best_cost
        cid_cost_dict = {}
        l = []
        sorted_cid_list = []
        worker_idx = 0
        total_cids_cost = 0
        acc_cid_cost = 0
        for cid, cid_cost in sorted_tuple:
            if cid in cid_list:
            	total_cids_cost += cid_cost
            	cid_cost_dict.update({cid:cid_cost})
            	sorted_cid_list.append(cid)
        counter = 0
        cid_list_len = len(sorted_cid_list)
        avg_cid_cost = total_cids_cost / workers_count
        while (workers_count - worker_idx) != 1:
           
            if acc_cid_cost >= avg_cid_cost:
                opt_dict.update({worker_idx:l})
                counter = 0
                acc_cid_cost = 0
                worker_idx += 1
                l =[]
                #re-calc
                remain_workers = workers_count - worker_idx
                avg_cid_cost = sum(cid_cost_dict.itervalues())/remain_workers
            elif(counter==0):
                cid = sorted_cid_list[-1]
                cid_cost = cid_cost_dict[cid]
                l.append(cid)
                acc_cid_cost = cid_cost
                sorted_cid_list.remove(cid)
                del cid_cost_dict[cid]
                counter+=1
            else:
            	cid = sorted_cid_list[0]
            	cid_cost = cid_cost_dict[cid]
            	l.append(cid)
            	acc_cid_cost += cid_cost
                sorted_cid_list.remove(cid)
                del cid_cost_dict[cid]
              

            cid_list_len -= 1
      
        

        opt_dict.update({worker_idx:sorted_cid_list})
        opt_list = [ opt_dict[k] for k in opt_dict.keys()] 

        return opt_list

