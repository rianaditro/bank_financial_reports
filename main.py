import time, json, os, argparse

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


if __name__ == "__main__":
    main()