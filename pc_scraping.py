#div1 > table:nth-child(1)

#div1 > table:nth-child(1)


# from lxml import html
import requests
from bs4 import BeautifulSoup
import json
import logging
import argparse


from parsers import parse_results_page

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("--log", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="set logging verbosity")
	parser.add_argument("--output-file", type=str, default="results_2019_loksabha_incl_UTs.json", help="provide output file name (w/extension. supported types: csv, json)")
	args = parser.parse_args()
	

	logger = logging.getLogger()
	handler = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s PID:%(process)d Line:%(lineno)d %(levelname)-8s %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.setLevel(getattr(logging, args.log.upper()))

	base_url = "http://results.eci.gov.in/pc/en/constituencywise/Constituencywise<state_code><pc_code>.htm?ac=<pc_code>"
	state_codes = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 
	'S10',  'S11',  'S12',  'S13',  'S14',  'S15',  'S16',  'S17',  'S18',  'S19',  
	'S20',  'S21',  'S22',  'S23',  'S24',  'S25',  'S26',  'S27',  'S28',  'S29']
	ut_codes = ['U01', 'U02', 'U03', 'U04', 'U05', 'U06', 'U07']

	with open("pc_counts.json", "r") as f:
		pc_counts = json.load(f)

	logging.info('Loaded PC Counts')

	results = []

	for state_code in state_codes + ut_codes:
		pc_codes = range(1, pc_counts[state_code]['pc_count']+1)
		state_name = pc_counts[state_code]['name']

		logging.info('Starting Scraping State: %s' % state_name)

		for pc_code in pc_codes:
			constituency_results_url = base_url.replace("<state_code>", state_code).replace("<pc_code>",str(pc_code))

			logging.info('Scraping %s' % constituency_results_url)

			page = requests.get(constituency_results_url)
			if "*************TEST******" not in str(page.content): # exclude constituencies without election
				result_dict = parse_results_page(page, state_name, pc_code)
			results.append(result_dict)

	if "json" in args.output_file:
		with open(args.output_file, "w") as f:
			json.dump(results, f)
		
if __name__ == '__main__':
	main()		

