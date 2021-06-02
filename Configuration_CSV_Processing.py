import csv
import os


class result_save:

    def create_csv(self, path, titles):
        """
        Create a csv file in the path
        :param path: Path
        :param titles: The first line of the csv file is the title of each column,
        ['CP', 'PERSON_count', 'PERSON_percentage', 'PRODUCT_count', 'PRODUCT_percentage', 'EVENT_count', 'EVENT_percentage']
        :return:
        """
        # path = "../result/result.csv"
        with open(path, 'w+', newline='') as wf:
            csv_write = csv.writer(wf)
            csv_head = titles
            csv_write.writerow(csv_head)

    def write_csv(self, path, row):
        """
        Write a line of data to a csv file
        :param path: Path
        :param row: A line of data,
        ['..\\corpus\\W99-0632word.docx.txt', '110', '18.93%', '7', '1.20%', '2']
        :return:
        """
        with open(path, 'a+', newline='') as wf:
            csv_write = csv.writer(wf)
            # list
            data_row = row
            csv_write.writerow(data_row)

    def read_csv(self, path):
        """
        Read a csv file, the separator is a comma
        :param path: Path
        :return:
        """
        with open(path, "r+") as rf:
            csv_read = csv.reader(rf, delimiter=',')
            for line in csv_read:
                print(line)

    def txt2csv(self, txt_path, csv_path):
        """
        Convert a txt text to a csv file
        :param txt_path: txt text path
        :param csv_path: csv file path
        :return:
        """
        with open(txt_path, "r+") as rf:
            doc = csv.reader(rf)
            with open(csv_path, 'a+', newline='') as wf:
                out_csv = csv.writer(wf)
                out_csv.writerows(doc)

if __name__ == '__main__':
    result_save.read_csv()