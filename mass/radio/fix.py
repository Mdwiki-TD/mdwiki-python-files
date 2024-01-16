'''

python3 core8/pwb.py mass/radio/fix ask

'''
from new_api import printe
from mass.radio.start import ids_by_caseId, main

to_fix = [
    "180217",
    "178404",
    "173166",
    "169715",
    "167694",
    "164270",
    "158679",
    "158614",
    "156192",
    "156112",
    "155926",
    "153536",
    "153083",
    "152498",
    "151095",
    "148710",
    "100245",
    "100245",
    "100162",
    "99249",
    "99249",
    "98868",
    "97904",
    "97802",
    "97464",
    "97208",
    "96897",
    "94132",
    "91920",
    "87828",
    "87426",
    "87426",
    "85949",
    "85766",
    "84330",
    "84254",
    "82959",
    "81857",
    "81283",
    "81261",
    "80623",
    "80465",
    "79968",
    "78533",
    "77545",
    "76314",
    "76310",
    "75245",
    "75245",
    "74609",
    "73738",
    "73340",
    "72274",
    "72216",
    "71816",
    "71668",
    "71471",
    "67999",
    "67273",
    "66675",
    "66390",
    "66390",
    "65865",
    "65176",
    "63378",
    "61510",
    "61386",
    "61150",
    "60822",
    "59255",
    "58738",
    "58546",
    "55844",
    "55596",
    "55596",
    "55137",
    "54704",
    "53759",
    "51501",
    "51501",
    "50730",
    "49917",
    "49834",
    "49012",
    "49001",
    "47491",
    "45781",
    "44768",
    "44737",
    "44737",
    "44635",
    "44109",
    "43911",
    "43911",
    "43833",
    "43832",
    "43831",
    "42261",
    "41615",
    "40744",
    "40475",
    "40359",
    "40224",
    "39354",
    "39094",
    "38021",
    "37882",
    "36250",
    "36249",
    "36248",
    "36144",
    "36143",
    "36122",
    "36119",
    "36118",
    "36094",
    "36080",
    "36062",
    "35991",
    "35988",
    "35984",
    "35748",
    "33951",
    "33951",
    "33877",
    "33757",
    "33437",
    "32719",
    "31788",
    "28534",
    "27931",
    "27386",
    "27270",
    "27268",
    "25819",
    "22018",
    "21291",
    "19340",
    "19104",
    "18992",
    "18387",
    "18236",
    "18214",
    "18185",
    "18083",
    "18083",
    "17027",
    "16999",
    "15995",
    "15933",
    "14723",
    "14180",
    "12957",
    "12560",
    "11022",
    "8097",
    "8054",
    "6072",
    "5842",
    "4965",
    "2714",
]

new_ids = {}

for caseId in to_fix:
    if caseId not in ids_by_caseId:
        printe.output(f"caseId {caseId} not found in ids_by_caseId")
        continue
    new_ids[caseId] = ids_by_caseId[caseId]

main(new_ids)