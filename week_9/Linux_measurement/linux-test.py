import os
import psutil
import subprocess
from memory_profiler import profile
import time
import multiprocessing
from sys import platform

cpu_corenumber = multiprocessing.cpu_count()
current_dir_path = os.path.dirname(os.path.realpath(__file__))

def get_proglist_by_progname():
    prog_dict = {}
    listfile = os.path.join(current_dir_path,'Instruction.txt')
    with open(listfile) as f:
        for line in f:
            if line[0] == '#':
                program_type = line[1:-1]
            elif not line[:-1] in prog_dict:
                prog_dict[line[:-1]] = [program_type]
            else:
                prog_dict[line[:-1]].append(program_type)
    return prog_dict

def get_proglist_by_interpreter():
    interpreter_dict = {}
    listfile = os.path.join(current_dir_path,'Instruction.txt')
    with open(listfile) as f:
        for line in f:
            if line[0] == '#':
                interpreter_type = line[1:-1]
            elif not interpreter_type in interpreter_dict:
                interpreter_dict[interpreter_type] = [line[:-1]]
            else:
                interpreter_dict[interpreter_type].append(line[:-1])
    return interpreter_dict

#for name consistency
def folder_name_modifier(name):
    try:
        if name == 'python':
            return 'CPython'
        elif name == 'jython':
            retun 'Jython'
        elif name == 'ironpython':
            return 'IronPython'
        elif name == 'pypy'
            return "PyPy"
        else
            raise ValueError('name wrong. Check your proglist')
    except ValueError as err:
        print(err.args)
        
def run_program(interpreter,programname,parameter):
    outputfilepath = os.path.join(current_dir_path,folder_name_modifier(interpreter))
	if not os.path.exists(outputfilepath):
        try:
            os.makedirs(outputfilepath)
        except:
            print("Error creating output file path: "+programname) 
            break
    outputfile = os.path.join(outputfilepath,programname.parse('.')[0]+'.out')
    mem_use = 0
    t = 0
    PERCPU_start = 0

    if parameter[-3:] == "txt":
        myinput = open(parameter)
        PERCPU_start = psutil.cpu_times(percpu=True)
        t=time.time()
        p=subprocess.Popen(interpreter+' '+programname, stdin=myinput, shell = True)
    else:
        PERCPU_start = psutil.cpu_times(percpu=True)
        t=time.time()
        p=subprocess.Popen(interpreter+' '+programname+' '+parameter, shell = True)
    pi=p.pid
    
    while p.poll()is None:
    	try:
    		cpu_time=psutil.Process(pi).cpu_times()
    		mem_use=max(psutil.Process(pi).memory_info().rss,mem_use)
    	except:
    		break
    elapsed_time = 	time.time()-t
    PERCPU_exit=psutil.cpu_times(percpu=True)
    
    memory_usage = str(round(mem_use/1024,0))+' KB'
    CPU_load=[]
    if platform == "win32":
        CPU_time = cpu_time.user+cpu_time.system
    elif platform == "linux" or platform == "linux2":
        CPU_time = cpu_time.children_user+cpu_time.children_system
        for i in range(cpu_corenumber):
        	CPU_load.append(((PERCPU_exit[i].user-PERCPU_start[i].user)/(PERCPU_exit[i].user-PERCPU_start[i].user+PERCPU_exit[i].idle-PERCPU_start[i].idle))*100//1)

    with open(outputfile,'a') as file:
        print 'Elapsed time: ',time.time()-t
        PERCPU_exit=psutil.cpu_times(percpu=True)
        print 'CPU time: ',cpu_time.children_user+cpu_time.children_system
        print 'memory usage: ',str(round(mem_use/1024,0))+' KB'
        CPU_load=[]
        for i in range(8):
        	CPU_load.append(((PERCPU_exit[i].user-PERCPU_start[i].user)/(PERCPU_exit[i].user-PERCPU_start[i].user+PERCPU_exit[i].idle-PERCPU_start[i].idle))*100//1)
        print 'CPU_load: ',CPU_load

def main():
    proglist = get_proglist_by_interpreter()
    print proglist
    for key,value in proglist.items():
        interpreter = key.lower()
        if interpreter == 'cpython':
            interpreter = 'python'
        for i in value:
            programname = i.parse(',')[0]
            parameter = i.parse(',')[1]
            run_program(interpreter,programname,parameter)
            
        
    
if __name__ == '__main__':
    main()