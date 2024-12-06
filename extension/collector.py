from bs4 import BeautifulSoup as bs


def collector(filename:str):
    with open(filename, "r") as f:
        html = f.read()
        soup = bs(html, "html.parser")
        
    banks = soup.find_all("span", class_="x-tree-node-text")

    banks = [bank.text for bank in banks]
    return banks


if __name__ == "__main__":
    banks = collector("Laporan Keuangan Perbankan.html")
    print(banks)