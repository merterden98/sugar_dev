import requests
import re
import argparse
import tqdm
from time import sleep
from typing import Optional, Set
from collections import defaultdict


ROOT_URL = "https://www.genome.jp/dbget-bin/www_bget"

def construct_url(rid : str) -> str:
    return ROOT_URL + "?rn:" + rid

def parse_html_to_rclass(html : str) -> Set[str]:
    # construct a regex that matches a <tr> tag containing a class attribute that contains the <th> tag with a <span> that says "Reaction class"
    rclass_regex = r'<tr>\s*<th class=\"[\w\s]*\">\s*<span class=\"[\w\s]*\">Reaction class</span>\s*</th>(.*?)</table></td></tr>'
    rclass_match = re.search(rclass_regex, html, re.DOTALL)
    
    if rclass_match:
        # extract all text that starts with RC and contains numbers
        rclass = re.findall(r"RC\d+", rclass_match.group(1))
        return set(rclass)
    return set()

    
def get_rclass(rid : str) -> Optional[Set[str]]:
    url = construct_url(rid)
    r = requests.get(url)
    if r.status_code == 200:
        return parse_html_to_rclass(r.text)
    else:
        return None

def rids_to_rclasses(rids : Set[str]) -> defaultdict:
    rclasses = defaultdict(set)
    for rid in tqdm.tqdm(rids):
        sleep(0.5)
        rclass = get_rclass(rid)
        if rclass:
            for rc in rclass:
                rclasses[rc].add(rid)
    return rclasses

def main(rids_file : str) -> None:
    rids = set()
    with open(rids_file, "r") as f:
        for line in f:
            rids.add(line.strip())
    rclasses = rids_to_rclasses(rids)
    with open("rclasses.txt", "w") as f:
        for rc in rclasses:
            f.write(rc + "\t" + " ".join(rclasses[rc]) + "\n")
        
if __name__ == "__main__":
    # contruct a parser that takes in a file with a list of rids
    parser = argparse.ArgumentParser(description="Get the reaction classes for a list of rids")
    parser.add_argument("rids", type=str, help="A file containing a list of rids")
    main(parser.parse_args().rids)