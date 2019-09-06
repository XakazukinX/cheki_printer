import instax
import sys
import time
import logging
import csv
import glob

my_instax = instax.SP2(ip='192.168.0.251', port=8080, pinCode=1111,timeout=10)
is_success = False

def printProgress(count, total, status=''):
    logging.info(status)
    if "complete" in status:
        global is_success # 大域変数にアクセス
        is_success = True
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
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
    print('印刷を継続します')
except:
    print('初期作業を開始します')

w_csv_file = open(log_path, 'a')
writer = csv.writer(w_csv_file, lineterminator='\n')

file_path_list = glob.glob("./files/*.jpg") + glob.glob("./files/*.png")
file_name_list = (map(lambda x: x.replace('./files/', ''), file_path_list))

for file_name in file_name_list:
    is_success = False
    if file_name in printed_list:
        pass
    else:
        try:
            print("%s枚目: %s" % (count, file_name))
            instax_image.loadImage('./files/' + file_name)
            instax_image.convertImage()
            encoded_image = instax_image.encodeImage()
            my_instax.printPhoto(encoded_image, printProgress)
            # つらい感じの実装. successだったら継続. Timeout だったら殺す
            if is_success:
                writer.writerow([file_name])
                count += 1
            else:
                print('印刷エラー. 用紙切れかも')
                w_csv_file.close()
                exit()
        except:
            print('印刷エラー. 用紙切れかも')
            w_csv_file.close()
            exit()

w_csv_file.close()
