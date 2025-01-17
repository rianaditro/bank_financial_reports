"""
Generate JSON file to validate whether the file is already downloaded, not exist on server, or missed
"""

import json
import os
import pandas
from zipfile import BadZipFile


def check_existence(mode:str, filename:str):
    if os.path.exists(f"{mode}/{filename}"):
        status = "file found"
    else:
        status = "file not found"
    return status

def generate_url(bank:str, year:int, month:int, mode:str):
    # Convert bank input into url format
    bank_code, bank_name = bank.split("-", 1)
    bank_name = bank_name.replace(" ", "+").replace(",", "%2C")

    if mode == "neraca":
        report_code = "PGWS-908-00021"
    elif mode == "laba_rugi":
        report_code = "PGWS-908-00022"
    else:
        report_code = "PGWS-908-00027"
    
    # Change the report code for 2020+
    if year > 2020:
        report_code += "A"
    
    # Formating URL
    base_url = "https://cfs.ojk.go.id/cfs/ReportViewerForm.aspx?"
    tail_url = "FinancialReportPeriodTypeCode=B&FinancialReportTypeCode={}".format(report_code)

    return f"{base_url}BankCodeNumber={bank_code}&BankCode={bank_name}&Month={month}&Year={year}&{tail_url}"

def generate_json():
    MONTHS = [3, 6, 9, 12]
    YEARS = [i for i in range(2010, 2024)]
    BANK_NAMES = ['002-PT BANK RAKYAT INDONESIA (PERSERO), Tbk', '003-PT BANK EKSPOR INDONESIA (PERSERO)', '008-PT BANK MANDIRI (PERSERO)', '009-PT BANK NEGARA INDONESIA (PERSERO), Tbk ', '200-PT BANK TABUNGAN NEGARA (PERSERO), Tbk', '026-PT.LIPPOBANK TBK', '060-PT.RABO BANK DUTA INDONESIA', '110-PT BPD JAWA BARAT DAN BANTEN, Tbk', '111-PT BPD DKI', '112-PT BPD DAERAH ISTIMEWA YOGYAKARTA', '113-PT BPD JAWA TENGAH', '114-PT BPD JAWA TIMUR Tbk', '115-PT BPD JAMBI ', '116-PT BANK ACEH', '117-PT BPD SUMATERA UTARA ', '118-PT BANK NAGARI', '119-PT BPD RIAU DAN KEPULAUAN RIAU ', '120-PT BPD SUMATERA SELATAN DAN BANGKA BELITUNG', '121-PT BPD LAMPUNG', '122-PT BPD KALIMANTAN SELATAN', '123-BPD KALIMANTAN BARAT', '124-PT BPD KALIMANTAN TIMUR DAN KALIMANTAN UTARA', '125-PT BPD KALIMANTAN TENGAH', '126-PT BPD SULAWESI SELATAN DAN SULAWESI BARAT ', '127-PT BPD SULAWESI UTARA GORONTALO', '128-PT BPD NUSA TENGGARA BARAT', '129-PT BPD BALI ', '130-PT BPD NUSA TENGGARA TIMUR ', '131-PT BPD MALUKU DAN MALUKU UTARA', '132-PT BPD PAPUA', '133-PT BPD BENGKULU', '134-PT.  BPD SULAWESI TENGAH', '135-PT BPD SULAWESI TENGGARA', '137-PT BANK PEMBANGUNAN DAERAH BANTEN, Tbk (d.h SANDI 558-BANK PUNDI )', '140-BANK CITRA MAKMUR ASIA (eks.YAMA BANK)', '011-PT BANK DANAMON INDONESIA, Tbk ', '013-PT BANK PERMATA, Tbk', '014-PT BANK CENTRAL ASIA, Tbk', '016-PT BANK MAYBANK INDONESIA, Tbk', '019-PT PAN INDONESIA BANK, Tbk ', '020-PT BANK ARTA NIAGA KENCANA', '022-PT BANK CIMB NIAGA, Tbk', '023-PT BANK UOB INDONESIA', '027-PT PRIMA EXPRESS BANK', '028-PT BANK OCBC NISP, Tbk', '034-PT ING INDONESIA BANK', '035-PT BANK SOCIETE GENERALE INDONESIA', '036-PT BANK CHINA CONSTRUCTION BANK INDONESIA, Tbk', '037-PT BANK ARTHA GRAHA INTERNASIONAL, Tbk', '038-PT BANK PARIBAS - BBD INDONESIA', '039-PT. BANK CREDIT AGRICOLE INDOSUEZ', '044-PT BANK IBJ INDONESIA', '045-PT BANK SUMITOMO INDONESIA ', '046-PT BANK DBS INDONESIA ', '047-PT BANK RESONA PERDANIA', '048-PT BANK MIZUHO INDONESIA', '049-PT. BANK UFJ INDONESIA', '053-PT.KEPPEL TAT LEE BUANA BANK', '054-PT BANK CAPITAL INDONESIA, Tbk', '055-PT BANK SAKURA SWADHARMA', '056-PT TOKAI LIPPO BANK', '057-PT BANK BNP PARIBAS INDONESIA', '059-PT BANK KEB INDONESIA', '061-PT BANK ANZ INDONESIA', '062-PT BANK DAI-ICHI KANGYO INDONESIA', '068-PT BANK WOORI INDONESIA', '072-PT BANK DAGANG BALI', '073-PT BANK UNIVERSAL Tbk.', '075-PT BANK UNIBANK Tbk', '076-PT BANK BUMI ARTA, Tbk', '085-PT BANK ARTHA GRAHA', '087-PT BANK HSBC INDONESIA', '088-PT BANK ANTARDAERAH', '089-PT BANK INTERIM INDONESIA', '093-PT BANK IFI', '095-PT BANK JTRUST INDONESIA, TBK', '097-PT BANK MAYAPADA INTERNATIONAL, Tbk', '145-PT BANK NUSANTARA PARAHYANGAN,Tbk', '146-PT BANK OF INDIA INDONESIA, Tbk', '151-PT BANK MESTIKA DHARMA ', '152-PT BANK SHINHAN INDONESIA', '153-PT BANK SINARMAS, Tbk', '157-PT BANK MASPION INDONESIA ', '158-PT ARTAMEDIA BANK', '159-PT BANK HAGAKITA', '161-PT BANK GANESHA ', '162-PT BANK WINDU KENTJANA', '164-PT BANK ICBC INDONESIA', '166-PT BANK HARMONI INTERNATIONAL', '167-PT BANK QNB INDONESIA, Tbk', '168-PT BANK PIKKO Tbk', '212-PT BANK WOORI SAUDARA INDONESIA 1906, Tbk', '213-PT BANK SMBC INDONESIA, TBK (PT BANK BTPN, Tbk)', '332-PT.BANK JAKARTA', '369-PT BANK PATRIOT', '405-PT BANK SWAGUNA ', '422-PT. BANK JASA ARTA', '426-PT BANK MEGA, Tbk ', '441-PT BANK KB BUKOPIN, Tbk', '459-PT BANK BISNIS INTERNASIONAL ', '466-PT BANK OKE INDONESIA', '472-PT BANK JASA JAKARTA ', '484-PT BANK KEB HANA INDONESIA', '485-PT BANK MNC INTERNASIONAL, Tbk', '490-PT BANK NEO COMMERCE TBK', '491-PT BANK MITRANIAGA', '494-PT BANK RAYA INDONESIA TBK', '498-PT BANK SBI INDONESIA ', '501-PT BANK DIGITAL BCA', '503-PT BANK NATIONALNOBU', '504-PT BANK ASIATIC', '506-PT BANK UMUM TUGU', '513-PT BANK INA PERDANA ', '520-PT PRIMA MASTER BANK ', '521-PT BANK PERSYARIKATAN INDONESIA ', '523-PT BANK SAHABAT SAMPOERNA', '526-PT BANK OKE INDONESIA TBK', '531-PT BANK AMAR INDONESIA', '532-PT BANK PRASIDHA UTAMA', '533-PT BANK DANPAC', '535-PT BANK SEABANK INDONESIA', '542-PT BANK JAGO Tbk', '546-PT GLOBAL INTERNATIONAL BANK', '547-PT BANK SAHABAT PURBA DANARTA', '548-PT BANK MULTIARTA SENTOSA ', '552-PT BANK RATU', '553-PT BANK HIBANK INDONESIA', '555-PT BANK INDEX SELINDO ', '558-PT BANK PEMBANGUNAN DAERAH BANTEN, TBK', '559-PT CENTRATAMA NASIONAL BANK', '562-PT Super Bank Indonesia', '564-PT BANK MANDIRI TASPEN', '566-PT BANK VICTORIA INTERNATIONAL, Tbk', '567-PT ALLO BANK INDONESIA Tbk', '945-PT BANK IBK INDONESIA Tbk', '946-PT BANK MERINCORP', '949-PT BANK CTBC INDONESIA', '950-PT BANK COMMONWEALTH ', '030-AMERICAN EXPRESS BANK LTD.', '031-CITIBANK NA ', '032-JP. MORGAN CHASE BANK, N.A.', '033-BANK OF AMERICA, N.A ', '040-THE BANGKOK BANK COMP. LTD', '041-THE HONGKONG AND SHANGHAI BANKING CORP', '042-MUFG Bank, Ltd', '050-STANDARD CHARTERED BANK ', '052-THE ROYAL BANK OF SCOTLAND N.V.', '067-DEUTSCHE BANK AG. ', '069-BANK OF CHINA (HONGKONG) LIMITED']
    MODES = ['neraca', 'laba_rugi', 'rasio']

    results = []
    for mode in MODES:
        
        data_per_mode = []
        for bank in BANK_NAMES:
            for year in YEARS:
                for month in MONTHS:

                    file_url = generate_url(bank, year, month, mode)

                    # Formating bank input for filename
                    bank = bank.replace(" ", "+")
                    filename = f"{bank}_{year}_{month}_{mode}.xlsx"

                    validator = {
                        "filename": filename,
                        "file_url": file_url,
                        "status": check_existence(mode, filename)
                    }

                    data_per_mode.append(validator)
        
        results.append(
            {
                "mode": mode,
                "data": data_per_mode
            }
        )
    
    with open("validator.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print("validator.json is generated")

def validate_temp_result(filename:str):
    mode = filename.replace("validator_","").replace(".json", "")
    with open(filename, 'r') as file:
        json_data = json.load(file)
    
    updated_status = 0
    for data in json_data:
        # Check if file is readable
        try:
            print(f"Checking file {data['filename']}")
            df = pandas.read_excel(f"{mode}/{data['filename']}")
        except BadZipFile:
            data["status"] = "corrupted"
            print("Corrupted file found.")
            updated_status += 1
        except:
            data["status"] = "unknown_error"
            print("Unknown error")
            updated_status += 1
    print(f"Updated Status: {updated_status}")
    
    with open(f"{filename.replace('.json', '')}_2.json", 'w') as file:
        json.dump(json_data, file, indent=4)
            

if __name__ == "__main__":
    # # Run for the first time
    generate_json()

    # validate_temp_result("validator_neraca.json")
