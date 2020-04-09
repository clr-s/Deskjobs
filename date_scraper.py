import email
import os
import csv
def scrape_date(fname):
    with open(fname) as f:
        try:
            return [items[1] for items in email.message_from_string(f.read()).items() if items[0]=="Date"] +[1]
        except:
            return ''

def write_row(rows):
     with open("C:/Users/3301/Desktop/Files/bid_date.csv","a+") as my_csv_writer:
        writer=csv.writer(my_csv_writer)
        writer.writerow(rows)

if __name__=='__main__':
    fieldnames=["Bid_Date","Labels"]
    with open("C:/Users/3301/Desktop/Files/bid_date.csv","w") as my_csv_writer:
        writer=csv.DictWriter(my_csv_writer,fieldnames=fieldnames)
        writer.writeheader()

    for fnames in os.listdir("C:/Users/3301/Desktop/Files/Test_Data"):
        fnames="C:/Users/3301/Desktop/Files/Test_Data/"+fnames
        rv=scrape_date(fnames)
        if rv:
            write_row(rv)
