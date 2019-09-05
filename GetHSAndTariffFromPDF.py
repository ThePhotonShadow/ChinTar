import PyPDF2 as pypdf
import pandas as pd

class TariffData:
    def __init__(self, pdf_reader: pypdf.PdfFileReader):
        self._pdf_reader = pdf_reader
        self._rate_data = {}

    def get_reader(self):
        return self._pdf_reader

    @staticmethod
    def check_number(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def add_rate(self, hs_number, rate):
        self._rate_data[hs_number] = rate


class TariffData2018(TariffData):
    def __init__(self, pdf_reader: pypdf.PdfFileReader):
        TariffData.__init__(self, pdf_reader)

    def get_data(self):
        for page in range(self.get_reader().getNumPages()):
            print("Reading page {}".format(page))
            pagetext = self.get_reader().getPage(page).extractText().split("\n")
            iterindex = 0
            maxiter = len(pagetext)
            while iterindex < maxiter:
                if len(pagetext[iterindex]) == 8 and self.check_number(pagetext[iterindex]):
                    self.add_rate(pagetext[iterindex], pagetext[iterindex + 2])
                    iterindex += 3
                else:
                    iterindex += 1
        return self._rate_data


class TariffData2019(TariffData):
    def __init__(self, pdf_reader: pypdf.PdfFileReader):
        TariffData.__init__(self, pdf_reader)

    @staticmethod
    def check_tariff(string):
        try:
            int(string)
            return True
        except ValueError:
            if len(string) >= 2 and len(string) <= 4:
                try:
                    float(string[0])
                    if any(char in string for char in ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "∆"]):
                        print("Caught Exception")
                        return True
                    else:
                        return False
                except ValueError:
                    return False
            else:
                return False

    def add_rate(self, hs_number, rate):
        self._rate_data[hs_number] = rate

    def get_data(self):
        for page in range(self.get_reader().getNumPages()):
            print("Reading page {}".format(page))
            pagetext = self.get_reader().getPage(page).extractText().split("\n")
            iterindex = 0
            maxiter = len(pagetext)
            while iterindex < maxiter:
                if len(pagetext[iterindex]) == 9 \
                        and self.check_number(pagetext[iterindex][:3])\
                        and pagetext[iterindex][4] == "."\
                        and self.check_number(pagetext[iterindex][5:]):
                    hs_num = pagetext[iterindex]
                    while not self.check_tariff(pagetext[iterindex]):
                        iterindex += 1
                    self.add_rate(hs_num, pagetext[iterindex])
                    iterindex += 1
                else:
                    if len(pagetext[iterindex]) == 4 and self.check_number(pagetext[iterindex + 1][1:]):
                        if pagetext[iterindex + 1][0] == ".":
                            hs_num = pagetext[iterindex] + pagetext[iterindex + 1]
                            iterindex += 2
                            while not self.check_tariff(pagetext[iterindex]):
                                iterindex += 1
                            self.add_rate(hs_num, pagetext[iterindex])
                    iterindex += 1
        return self._rate_data

file18 = pypdf.PdfFileReader("2018_baserates.pdf")
file19 = pypdf.PdfFileReader("2019_baserates.pdf")

# out = file19.getPage(40).extractText().split("\n")
# out.remove("-")
# print(out)

data2018 = TariffData2018(file18)
data_dict18 = data2018.get_data()
print(data_dict18)
print(len(data_dict18))

data2019 = TariffData2019(file19)
data_dict19 = data2019.get_data()
print(data_dict19)
print(len(data_dict19))

biglist = []

# print(file19.getPage(550).extractText())

# for page in range(file19.getNumPages()):
#     pagelist = file19.getPage(page).extractText().split("\n")
#     for item in pagelist:
#         if len(item) == 4 and data2019.check_number(item[:3]):
#             biglist.append(item)
#
# print(biglist)
# print(len(biglist))

fixed_18 = []
for item in data_dict18.keys():
    new_item = item[0:4] + "." + item[4:]
    fixed_18.append(new_item)

for item in fixed_18:
    if len(item) < 9:
        print(item)

shortcount = 0
for item in fixed_18:
    if len(item) < 9:
        shortcount += 1

shortcount19 = 0
for item in data_dict19.keys():
    if len(item) < 9:
        shortcount19 +=1

print("shortcount: " + str(shortcount))
print("shortcount19: " + str(shortcount19))

missing = list(set(fixed_18).difference(set(data_dict19.keys())))

print("Done.")
print("fixed18 " + str(len(fixed_18)))
print(len(missing))
print(missing)

fincount = 0
for item in missing:
    if len(item) < 9:
        fincount += 1

print(fincount)