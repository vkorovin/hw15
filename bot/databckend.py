import csv
import datetime


class DataStore():

    def __init__(self, filename, fieldnames):
        self.filename = filename
        self.data = list()
        self.fieldnames = fieldnames
        try:
            with open(self.filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for item in reader:
                    self.data.append(item)

        except FileNotFoundError:
            with open(self.filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()


    def save(self, dict):
        self.data.append(dict)
        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(dict)


    def get(self):
        for item in self.data:
            yield item

    def get_today(self):
        today = datetime.date.today().strftime('%d-%m')
        for item in self.data:
            if  datetime.datetime.strptime(item['birthday'],'%d-%m-%Y').strftime('%d-%m') == today:
                yield item


if __name__== '__main__':

    data = DataStore("data.csv", ['username','birthday'])
    data.save({'username':'Petya','birthday':'05-12-1978'})
    data.save({'username': 'Petya', 'birthday': '07-07-1978'})

    for item in data.get_today():
        print(item)
