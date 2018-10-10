from subprocess import Popen, PIPE
from xml.etree.ElementTree import fromstring


def get_top(xml, name):
    return list(xml.iter(name))[0]

def extract_text(xml, name):
    return get_top(xml, name).text

def parse_nvidia_smi():
    p = Popen(['nvidia-smi', '-q', '-x'], stdout=PIPE)
    outs, errors = p.communicate()
    xml = fromstring(outs)
    results = []
    for gpu_id, gpu in enumerate(xml.iter('gpu')):
        gpu_data = {}

        name = extract_text(gpu, 'product_name')
        gpu_data['name'] = name

        # get memory
        memory_usage = get_top(gpu, 'fb_memory_usage')
        total_memory = extract_text(memory_usage, 'total')
        used_memory = extract_text(memory_usage, 'used')
        free_memory = extract_text(memory_usage, 'free')
        gpu_data['memory'] = {
            'total': total_memory,
            'used_memory': used_memory,
            'free_memory': free_memory
        }

        # get utilization
        utilization = get_top(gpu, 'utilization')
        gpu_util = extract_text(gpu, 'gpu_util')
        memory_util = extract_text(gpu, 'memory_util')
        gpu_data['utilization'] = {
            'gpu_util': gpu_util,
            'memory_util': memory_util
        }

        # processes
        processes = get_top(gpu, 'processes')
        infos = []
        for info in processes.iter('process_info'):
            pid = extract_text(info, 'pid')
            process_name = extract_text(info, 'process_name')
            used_memory = extract_text(info, 'used_memory')
            infos.append({
                'pid': pid,
                'process_name': process_name,
                'used_memory': used_memory
            })
        gpu_data['processes'] = infos

        results.append(gpu_data)
    return results
