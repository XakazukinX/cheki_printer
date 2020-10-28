import os
import re

import instax
import sys
import time
import logging
import csv
import glob
import random

from instax.sp2 import Color

my_instax = instax.SP2(ip='192.168.0.251', port=8080, pinCode=1111, timeout=10)
is_success = False

while True:
    inp = input('印刷を開始するにはエンターキーを押してください>>')
    if inp == '':
        break
print('start cheki print')


def print_progress(_count, total, status=''):
    logging.info(status)
    if "complete" in status:
        global is_success  # 大域変数にアクセス
        is_success = True
    bar_len = 60
    filled_len = int(round(bar_len * _count / float(total)))
    percents = round(100.0 * _count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)


instax_image = instax.InstaxImage(type=2)
log_path = './files/printout.log'
printed_list = []
count = 1

try:
    r_csv_file = open(log_path, 'r')
    printed_list = list(map(lambda x: x.replace('\n', ''), list(r_csv_file)))
    count = len(printed_list) + 1
    r_csv_file.close()
    print('continue')
except:
    print('error at create printed_list')

w_csv_file = open(log_path, 'a')
writer = csv.writer(w_csv_file, lineterminator='\n')

args = sys.argv
file_path_list = glob.glob("./files/*.jpg") + glob.glob("./files/*.png")

if (len(args) == 1) or (len(args) == 2 and args[1] != "random"):
    file_path_list = sorted(glob.glob("./files/*.jpg") + glob.glob("./files/*.png"),
                            key=lambda val: int(re.sub("\\D", "", val)))
    print("Sorted")
elif (len(args) > 1) and (args[1] == "random"):
    random.shuffle(file_path_list)

if os.name == 'nt':
    file_name_list = (map(lambda x: x.replace('./files\\', './files/'), file_path_list))
    print('on Windows')
elif os.name == 'posix':
    file_name_list = (map(lambda x: x.replace('./files\\', './files/'), file_path_list))
    print('on Mac or Linux')

for file_name in file_name_list:
    print(file_name)
print('start loop')
for file_name in file_name_list:
    is_success = False
    if file_name in printed_list:
        pass
    else:
        try:
            print(r"%s枚目: %s" % (count, file_name))
            instax_image.loadImage(file_name)
            try:
                instax_image.convert_image()
            except Exception as err:
                print(r"[エラー] 画像変換時にエラーが発生しました。 [%s]" % err)
                break
            try:
                encoded_image = instax_image.encodeImage()
            except Exception as err:
                print(r"[エラー] 画像のエンコード時にエラーが発生しました。画像のサイズを確認してください。 [%s]" % err)
                break

            err = my_instax.printPhoto(encoded_image, print_progress)
            # if err is not None:
            #     print("???????")
            #     w_csv_file.close()
            #     break
            if is_success:
                writer.writerow([file_name])
                count += 1
            else:
                w_csv_file.close()
                break
        except:
            print(sys.exc_info())
            w_csv_file.close()
            exit()
w_csv_file.close()
print("End")
exit(0)
