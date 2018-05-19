import csv


def save_info(info):
    dir = 'inscricoes.csv'
    with open(dir, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(info)
