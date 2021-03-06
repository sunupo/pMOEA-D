from PMOEAD import PMOEAD, PMOEAD_bytime
from store_result import store_result
from controller import parallel_run, parallel_run_bytime, naive_paralle

import time
import sys
import argparse


INF = 1E9


def run_test(file_name):
    feature_num = 13
    if file_name == 'clean1.txt':
        feature_num = 167
    if file_name == 'Wine.txt':
        feature_num = 13
    population_size = max(100, min(200, feature_num))
    run_time = 120
    iteration_num = 10
    test_times = 15
    begin = 0
    end = population_size
    cpu_num = 8
    overlapping_ratio = 0.2
    f = open('./result/chosenFile.txt', 'a')
    # parallel run
    # test_parallel_run_by_time(f, test_times, run_time, iteration_num, cpu_num, file_name, feature_num, population_size)
    # single run
    # test_PMOEAD_bytime(f, test_times, file_name, feature_num, population_size, run_time, begin, end)  # single
    # fix ratio
    #test_parallel_run_by_time_ratio(f, test_times, run_time, iteration_num, cpu_num, file_name, feature_num,
    #                                population_size, 0.1)
    #test_parallel_run_by_time_ratio(f, test_times, run_time, iteration_num, cpu_num, file_name, feature_num,
    #                                population_size, 0.3)
    #test_parallel_run_by_time_ratio(f, test_times, run_time, iteration_num, cpu_num, file_name, feature_num,
    #                                population_size, 0.4)
    #test_parallel_run_by_time_ratio(f, test_times, run_time, iteration_num, cpu_num, file_name, feature_num,
    #                               population_size, 0.5)

    # auto run
    test_parallel_run_by_time_auto(f, test_times, run_time, iteration_num, cpu_num, file_name, feature_num,
                                   population_size)

    f.close()


#     Wine 13 clean1 167
# Using hyper volume to choose th middle file
def chose_file(res):
    res = sorted(res, key=lambda x: x[1])
    l = int((len(res) + 1) / 2 - 1)
    return res[l][0]


def test_parallel_run_by_time(f, test_times, run_time, iteration_num, cpu_num, file_name, feature_num, population_size):
    res = []
    print('run parallel', file_name, 'starts')
    for i in range(test_times):
        population, obj = parallel_run_bytime(max_time=run_time, iteration_num=iteration_num, cpu_num=cpu_num,
                                              file_name=file_name,
                                              dimension=feature_num, population_size=population_size)
        name = '{}_cpu{}_{}'.format(file_name[:-4], cpu_num, i)
        hv = store_result(obj, name)
        res.append((i, hv))
    order = chose_file(res)
    name = '{}_cpu{}'.format(file_name[:-4], cpu_num)
    f.write('file:{}   chosen:the {} file\n'.format(name, order))
    print('run parallel', file_name, 'ends')


def test_PMOEAD_bytime(f, test_times, file_name, feature_num, population_size, run_time, begin, end):
    res = []
    print('run single', file_name, 'starts')
    for i in range(test_times):
        population, obj = PMOEAD_bytime(file_name=file_name, dimension=feature_num, population_size=population_size,
                                        max_time=run_time, begin=begin, end=end)
        name = '{}_single_{}'.format(file_name[:-4], i)
        hv = store_result(obj, name)
        res.append((i, hv))
    order = chose_file(res)
    name = '{}_single'.format(file_name[:-4])
    f.write('file:{}   chosen:the {} file\n'.format(name, order))
    print('run single', file_name, 'ends')


def test_parallel_run_by_time_ratio(f, test_times, run_time, iteration_num, cpu_num, file_name, feature_num,
                                    population_size, ratio):
    res = []
    print('run ratio', file_name, 'starts')
    for i in range(test_times):
        population, obj = parallel_run_bytime(max_time=run_time, iteration_num=iteration_num, cpu_num=cpu_num,
                                              file_name=file_name,
                                              dimension=feature_num, population_size=population_size,
                                              overlapping_ratio=ratio)
        name = '{}_cpu{}_o{}_{}'.format(file_name[:-4], cpu_num, ratio, i)
        hv = store_result(obj, name)
        res.append((i, hv))
    order = chose_file(res)
    name = '{}_cpu{}_o{}'.format(file_name[:-4], cpu_num, ratio)
    f.write('file:{}   chosen:the {} file\n'.format(name, order))
    print('run single', file_name, 'ends')


def test_parallel_run_by_time_auto(f, test_times, run_time, iteration_num, cpu_num, file_name, feature_num,
                                   population_size):
    res = []
    print('run auto', file_name, 'starts')
    for i in range(test_times):
        population, obj = parallel_run_bytime(max_time=run_time, iteration_num=iteration_num, cpu_num=cpu_num,
                                              file_name=file_name,
                                              dimension=feature_num, population_size=population_size,
                                              overlapping_ratio=0, auto_adjust=True)
        name = '{}_cpu{}_auto_{}'.format(file_name[:-4], cpu_num, i)
        hv = store_result(obj, name)
        res.append((i, hv))
    order = chose_file(res)
    name = '{}_cpu{}_auto'.format(file_name[:-4], cpu_num)
    f.write('file:{}   chosen:the {} file\n'.format(name, order))
    print('run auto', file_name, 'ends')



def load_dataset_prop():
    dataset = [
        {
            "name": "clean1",
            "file_name": "./src/dataset/clean1.txt",
            "features": 167,
            "population_size": 167
        },
        {
            "name": "wine",
            "file_name": "./src/dataset/Wine.txt",
            "features": 13,
            "population_size": 100
        }
    ]
    return dataset


def sys_args():
    dataset = load_dataset_prop()
    description = "OVERVIEW: pMOEA/D Interface\n\n" \
                  "USAGE: python3 reader.py -m [method] <inputs>\n" \
                  "    method: 1 for single core\n" \
                  "            2 for parallel\n" \
                  "            3 for parallel with overlapping\n" \
                  "            4 for parallel overlap auto adjust\n" \
                  "    inputs: Parameters\n" \
                  "    EXAMPLES:\n" \
                  "        python3 reader.py -h/--help\n" \
                  "        python3 -m 3 -o 0.1 -d wine\n" \
                  "        python3 -m 2 -t 600 -i 10 -c 8 -d clean1\n"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-m",
                        "--method",
                        help="Choose a method for running",
                        metavar="1/2/3/4",
                        choices=[1, 2, 3, 4],
                        type=int,
                        required=True
                        )
    parser.add_argument("-t",
                        "--time",
                        help="Time for one run (unit: second)",
                        metavar="600",
                        default=600,
                        type=int
                        )
    parser.add_argument("-i",
                        "--iter",
                        help="Iterations for each generation",
                        metavar="10",
                        default=10,
                        type=int
                        )
    parser.add_argument("-c",
                        "--cores",
                        help="Acquired cores for running(for method 2/3/4)",
                        metavar="8",
                        default=8,
                        type=int
                        )
    parser.add_argument("-o",
                        "--overlap",
                        help="Overlapping ratio(for method 3/4)",
                        metavar="0",
                        default=0,
                        type=float
                        )
    parser.add_argument("-n",
                        "--num",
                        help="setting serial of this task",
                        metavar="X",
                        default=0,
                        type=int
                        )
    parser.add_argument("-d",
                        "--dataset",
                        help="Choose a dataset for running",
                        metavar="Iris",
                        required=True
                        )
    args = parser.parse_args()
    method = args.method
    packs = {}
    if method == 1:
        packs['method'] = method
        if isinstance(args.time, int) and args.time > 0:
            packs['time'] = args.time
        else:
            print("[ERROR]: Invalid time format")
            sys.exit()
        file_exist = False
        for item in dataset:
            if item['name'] == args.dataset:
                file_exist = True
                packs['name'] = item['name']
                packs['file_name'] = item['file_name']
                packs['dimension'] = item['features']
                packs['population_size'] = item['population_size']
                packs['begin'] = 0
                packs['end'] = item['population_size']
                break
        if file_exist is False:
            print("[ERROR]: No such dataset exists: " + args.dataset)
            sys.exit()
    elif method == 2:
        packs['method'] = method
        if isinstance(args.time, int) and args.time > 0:
            packs["time"] = args.time
        else:
            print("[ERROR]: Invalid time format")
            sys.exit()
        if isinstance(args.iter, int) and args.iter > 0:
            packs["iter"] = args.iter
        else:
            print("[ERROR]: Invalid iteration format")
            sys.exit()
        if isinstance(args.cores, int) and args.cores > 0:
            packs["cores"] = args.cores
        else:
            print("[ERROR]: Invalid cores number format")
            sys.exit()
        file_exist = False
        for item in dataset:
            if item["name"] == args.dataset:
                packs["name"] = item["name"]
                file_exist = True
                packs["file_name"] = item["file_name"]
                packs["dimension"] = item["features"]
                packs["population_size"] = item["population_size"]
                break
        if file_exist is False:
            print("[ERROR]: No such dataset exists: " + args.dataset)
            sys.exit()
    elif method == 3:
        packs["method"] = method
        if isinstance(args.time, int) and args.time > 0:
            packs["time"] = args.time
        else:
            print("[ERROR]: Invalid time format")
            sys.exit()
        if isinstance(args.iter, int) and args.iter > 0:
            packs["iter"] = args.iter
        else:
            print("[ERROR]: Invalid iteration format")
            sys.exit()
        if isinstance(args.cores, int) and args.cores > 0:
            packs["cores"] = args.cores
        else:
            print("[ERROR]: Invalid cores number format")
            sys.exit()
        if isinstance(args.overlap, float) and args.overlap > 0:
            packs["overlap"] = args.overlap
        else:
            print("[ERROR]: Invalid overlap ratio format")
            sys.exit()
        file_exist = False
        for item in dataset:
            if item["name"] == args.dataset:
                packs["name"] = item["name"]
                file_exist = True
                packs["file_name"] = item["file_name"]
                packs["dimension"] = item["features"]
                packs["population_size"] = item["population_size"]
                break
        if file_exist is False:
            print("[ERROR]: No such dataset exists: " + args.dataset)
            sys.exit()
    elif method == 4:
        packs["method"] = method
        if isinstance(args.time, int) and args.time > 0:
            packs["time"] = args.time
        else:
            print("[ERROR]: Invalid time format")
            sys.exit()
        if isinstance(args.iter, int) and args.iter > 0:
            packs["iter"] = args.iter
        else:
            print("[ERROR]: Invalid iteration format")
            sys.exit()
        if isinstance(args.cores, int) and args.cores > 0:
            packs["cores"] = args.cores
        else:
            print("[ERROR]: Invalid cores number format")
            sys.exit()
        if isinstance(args.overlap, float) and args.overlap > 0:
            packs["overlap"] = args.overlap
        else:
            print("[ERROR]: Invalid overlap ratio format")
            sys.exit()
        file_exist = False
        for item in dataset:
            if item["name"] == args.dataset:
                packs["name"] = item["name"]
                file_exist = True
                packs["file_name"] = item["file_name"]
                packs["dimension"] = item["features"]
                packs["population_size"] = item["population_size"]
                break
        if file_exist is False:
            print("[ERROR]: No such dataset exists: " + args.dataset)
            sys.exit()
    else:
        print("[ERROR]: No such method: " + str(args.method))
        sys.exit()
    packs["num"] = args.num
    return packs


def run_task(packs: dict):
    test_times = 1
    if packs["method"] == 1:
        for i in range(test_times):
            population, obj = PMOEAD_bytime(
                file_name=packs["file_name"],
                dimension=packs["dimension"],
                population_size=packs["population_size"],
                max_time=packs["time"],
                begin=packs["begin"],
                end=packs["end"]
            )
            name = '[dataset_{}][method_{}][time_{}][{}]'.format(packs["name"],
                                                                 packs["method"],
                                                                 packs["time"],
                                                                 packs["num"])
            store_result(obj, name)
    elif packs["method"] == 2:
        for i in range(test_times):
            population, obj = parallel_run_bytime(
                max_time=packs["time"],
                iteration_num=packs["iter"],
                cpu_num=packs["cores"],
                file_name=packs["file_name"],
                dimension=packs["dimension"],
                population_size=packs["population_size"]
            )
            name = '[dataset_{}][method_{}][time_{}][cpu_{}][{}]'.format(packs["name"],
                                                                         packs["method"],
                                                                         packs["time"],
                                                                         packs["cores"],
                                                                         packs["num"])
            store_result(obj, name)
    elif packs["method"] == 3:
        for i in range(test_times):
            population, obj = parallel_run_bytime(
                max_time=packs["time"],
                iteration_num=packs["iter"],
                cpu_num=packs["cores"],
                file_name=packs["file_name"],
                dimension=packs["dimension"],
                population_size=packs["population_size"],
                overlapping_ratio=packs["overlap"]
            )
            name = '[dataset_{}][method_{}][time_{}][cpu_{}][ovlp_{}][{}]'.format(packs["name"],
                                                                                  packs["method"],
                                                                                  packs["time"],
                                                                                  packs["cores"],
                                                                                  packs["overlap"],
                                                                                  packs["num"])
            store_result(obj, name)
    else:
        for i in range(test_times):
            population, obj = parallel_run_bytime(
                max_time=packs["time"],
                iteration_num=packs["iter"],
                cpu_num=packs["cores"],
                file_name=packs["file_name"],
                dimension=packs["dimension"],
                population_size=packs["population_size"],
                overlapping_ratio=packs["overlap"],
                auto_adjust=True
            )
            name = '[dataset_{}][method_{}][time_{}][cpu_{}][ovlp_{}][auto][{}]'.format(packs["name"],
                                                                                        packs["method"],
                                                                                        packs["time"],
                                                                                        packs["cores"],
                                                                                        packs["overlap"],
                                                                                        packs["num"])
            store_result(obj, name)


if __name__ == '__main__':
#    file_name = 'clean1.txt'
#    run_test(file_name)

    pack = sys_args()
    run_task(pack)

    # feature_num = 167
    # population_size = max(100, min(200, feature_num))
    # iteration_num = 1000
    #
    # begin = 0
    # end = population_size

    # ------ This is the single core--------

    # population, obj = PMOEAD(file_name=file_name, dimension=feature_num, population_size=population_size,
    #                              max_iteration=iteration_num, begin=begin, end=end)
    # file_name = 'clean1-single'
    # ------------------------------------

    # -----------This is the multiple cores
    # round, iteration_num, cpu_num, file_name, dimension, population_size
    # population, obj = parallel_run(rounds=100, iteration_num=10, cpu_num=4, file_name=file_name, dimension=166, population_size=population_size)
    # file_name = 'clean1-PMOEAD-1000'
    # ------------------------------------

    # -------------Run by time parallel----------------------

    # max_time,iteration_num, cpu_num, file_name, dimension, population_size
    # run_time = 3600
    # population, obj = parallel_run_bytime(max_time=run_time, iteration_num=10, cpu_num=8, file_name=file_name,
    #                                       dimension=13, population_size=population_size)
    # a = 'clean1_pmoead_t3600_c8'
    # store_result(obj, a, population_size, run_time)

    # ------------------------------------------

    # ----------------Run by time single core---------------
    # file_name, dimension, population_size, max_time, begin, end

    # run_time = 3600
    # population, obj = PMOEAD_bytime(file_name=file_name, dimension=feature_num, population_size=population_size,
    #                                 max_time=run_time, begin=begin, end=end)
    # a = 'clean1_single_t3600'
    # store_result(obj, a, population_size, run_time)

    # --------------------------------------------------------
    # naive run by the same iteration
    # total_iteration = 1000
    # population, obj = naive_paralle(total_iteration=total_iteration, cpu_num=4, file_name=file_name, dimension=166, population_size=population_size)
    # file_name = 'clean1-naive-1000'
    # --------------------------------------------------------
    # naive run by same time

    # population, obj = naive_paralle(total_iteration=INF, cpu_num=4, file_name=file_name, dimension=13, population_size=population_size)
    # a = 'Wine-naive-time-3600'
    # store_result(obj, a, population_size, 3600)
    # --------------------------------------------------------
    # store_result(obj, file_name, population_size, iteration_num)
    # get_pf(obj, file_name, population_size, iteration_num)
    # print(time.time()-begin_time)
    # ---------------------------------------------------------------------------------
    # run_time = 3600
    # population, obj = parallel_run_bytime(max_time=run_time, iteration_num=10, cpu_num=8, file_name=file_name,
    #                                       dimension=13, population_size=population_size, overlapping_ratio=0.2)
    # a = 'clean1_overlapping_t3600_o0.2_c8'
    # store_result(obj, a, population_size, run_time)
