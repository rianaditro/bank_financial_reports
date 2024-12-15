import time, json, os, argparse

# Revision import
from urllib.parse import urlparse, parse_qs

from spider.crawler import Crawler


def validator_reader(filename:str, mode:str):
    with open(filename, "r") as file:
        json_data = json.load(file)
    
    # for data_per_mode in json_data:
    #     if data_per_mode["mode"] == mode:
    #         return data_per_mode["data"]
    return json_data

def browser_loop(mode:str, filename:str):
    data = validator_reader(filename, mode)
    max = len(data)

    crawler = Crawler(mode)

    for i, d in enumerate(data):
        print(f"Processing {i} of {max}")
        try:
            
            if d["status"] == "downloaded" or d["status"] == "not_exist":
                continue
            else:
                if d["status"] == "corrupted":
                    os.remove(f"{crawler.download_folder}/{d['filename']}")
                    print(f"delete {d['filename']}")

                while True:
                    updated_status = crawler.get_excel(d)

                    if updated_status == "downloaded" or updated_status == "not_exist":
                        d["status"] = updated_status
                        break
                    elif updated_status == "object_reference_error" or updated_status == "download_incomplete":
                        crawler = Crawler(mode)
        except:
            with open(f"validator_{mode}.json", "w") as fp:
                json.dump(data, fp, indent=4)

    with open(f"validator_{mode}.json", "w") as fp:
                json.dump(data, fp, indent=4)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", type=str, help="['neraca', 'laba_rugi', 'rasio']")
    parser.add_argument("-f", "--filename", type=str, help="JSON filename")

    args = parser.parse_args()

    browser_loop(args.mode, args.filename)

def additional_download():
    with open("extension/missing_or_empty_rasio.json", "r") as file:
        json_data = json.load(file)
    
    mode = "rasio"
    crawler = Crawler(mode)

    for i,data in enumerate(json_data):
        print(f"Processing {i+1} of {len(json_data)}: {((i+1)/len(json_data))*100:.2f}%")
        url = json_data[data]
        
        # convert url to filename
        # Parse the URL
        parsed_url = urlparse(url)

        # Extract query parameters as a dictionary
        params = parse_qs(parsed_url.query)

        # Convert single-item lists to plain values (optional)
        params = {key: value[0] if len(value) == 1 else value for key, value in params.items()}
        report_code = params['FinancialReportTypeCode']
        if report_code == "PGWS-908-00021":
            mode = "neraca"
        elif report_code == "PGWS-908-00022":
            mode = "laba_rugi"
        else:
            mode = "rasio"

        filename = f"{params['BankCodeNumber']}-{params['BankCode'].replace(' ', '+')}_{params['Year']}_{params['Month']}_{mode}.xlsx"

        data = {
            "filename": filename,
            "file_url": url,
        }

        # check if file already downloaded
        if os.path.exists(f"{crawler.download_folder}/{filename}"):
            print(f"File already downloaded: {filename}")
            continue
        else:
            print(f"Processing {data['filename']}")
            result = crawler.get_excel(data)
            print(result)

def check_not_found_files():
    with open("check_result.json", "r") as file:
        all_data = json.load(file)
        all_data = all_data[2:]
    
    for data in all_data:
        mode = data["mode"]
        details = data["data"]
        max = len(details)

        crawler = Crawler(mode)

        for i, detail_data in enumerate(details):
            print(f"Processing {i+1} of {max}: {((i+1)/max)*100:.2f}%")
            check_result = detail_data["check_result"]
            filename = detail_data["filename"]
            # check if file already downloaded
            if check_result == "not_exist":
                if "2020" in detail_data["file_url"]:
                    detail_data["file_url"] += "A"
                    if os.path.exists(f"{crawler.download_folder}/{filename}"):
                        print(f"File already downloaded: {filename}")
                        result = "already downloaded"
                    else:
                        result = crawler.get_excel(detail_data)
                        detail_data["check_result"] = result
            else:
                continue
            # if os.path.exists(f"{crawler.download_folder}/{filename}"):
            #     print(f"File already downloaded: {filename}")
            #     result = "already downloaded"
            # else:
            #     print(f"Processing {detail_data['filename']}")
            #     result = crawler.get_excel(detail_data)
            # detail_data["check_result"] = result

    with open("check_result2.json", "w") as file:
        json.dump(all_data, file, indent=4)
                



if __name__ == "__main__":
    # main()
    # data_dict = additional_download()
    check_not_found_files()