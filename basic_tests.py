import csv

a_list = [
    {'name': 'mike', 'age': '8'},
    {'name': 'lisa', 'age': '9'}
]


def write_csv():
    # 创建一个新的csv文件，在此我们命名为tsinghua_data.csv
    csv_file = open("./data_process/data.csv", "w+")
    try:
        writer = csv.writer(csv_file)
        # 将输入写入csv文件
        writer.writerow(('name', 'age'))
        for item in a_list:
            writer.writerow((item['name'], item['age']))
    finally:
        csv_file.close()


if __name__ == '__main__':

    write_csv()
    pass


