import os
from datetime import datetime
import subprocess
import json
import yaml
from operator import itemgetter
from multiprocessing import Pool

def sort_dict_by_value(dictionary):
    sorted_dict = dict(sorted(dictionary.items(), key=itemgetter(1), reverse=True))
    return sorted_dict

def get_subfolder_sizes(root_dir):
    folder_sizes = {}
    folder_sizes[root_dir] = {}
    # 获取当前文件夹下的子文件夹列表
    subfolders = [f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f))]
    for subfolder in subfolders:    
        # 执行 du -h 命令并获取输出结果
        command = ['du', '-h', '--max-depth=0', '--block-size=G', os.path.join(root_dir, subfolder)]
        print( help(subprocess.run))
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            output = result.stdout.strip()
        except Exception as e:
            output = os.popen(" ".join(command)).read()
        output = output.split('\t')
        # 解析输出结果以获取空间占用
        size = output[0]
        print(root_dir, output, size)

        # 将空间占用转换为以G为单位
        if size.endswith('G'):
            size_in_gb = float(size[:-1])
        elif size.endswith('M'):
            size_in_gb = float(size[:-1]) / 1024
        elif size.endswith('K'):
            size_in_gb = float(size[:-1]) / 1024 / 1024
        folder_sizes[root_dir][subfolder] = size_in_gb
    folder_sizes[root_dir] = sort_dict_by_value(folder_sizes[root_dir])
    return folder_sizes

def run(root_dir_list, save_dir = None):
    if isinstance(root_dir_list, str):       
        # load from yaml
        with open(root_dir_list, "r") as f:
            root_dir_list = yaml.load(f)
    else:
        pass
    size_dict = {}
    with Pool(8) as p:
        res_all = p.starmap(get_subfolder_sizes, [(x,) for x in root_dir_list])
    for res in res_all:
        size_dict.update(res)
    json_data = json.dumps(size_dict, indent = 4)
    print(json_data)
    if save_dir:
        save_path = os.path.join(save_dir, "log.du.%s" % datetime.now().strftime("%Y-%m-%d@%H:%M:%S"))
        with open(save_path, 'w') as file:
            file.write(json_data)
