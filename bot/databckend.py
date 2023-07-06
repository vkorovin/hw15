import csv
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


if __name__== '__main__':

    data = DataStore("data.csv", ['username','birthdate'])
    data.save({'username':'Petya','birthdate':'05-12-1978'})
    data.save({'username': 'Petya', 'birthdate': '05-12-1978'})

    for item in data.get():
        print(item)
