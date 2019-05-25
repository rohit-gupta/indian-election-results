
from bs4 import BeautifulSoup


def parse_results_page(page, state_name, constituency_code):
	soup = BeautifulSoup(page.content, "lxml")
	result_table = soup.select_one("#div1 > table:nth-of-type(1)") #find_all(id="div1")[0].

	rows = result_table.find_all('tr')

	state_head, constituency_name_head = tuple(rows[0].text.strip().split("-", maxsplit=1))
	result_head = rows[1].text.strip()
	headers_second_row = tuple([ele.text.strip() for ele in rows[2].find_all('th')])
	if state_name != "Jammu and Kashmir": # migrant voters are a special provision in J&K
		osn_head, candidate_name_head, party_name_head, evm_votes_head, postal_votes_head, total_votes_head, percent_votes_head = headers_second_row
	else:
		osn_head, candidate_name_head, party_name_head, evm_votes_head, migrant_votes_head, postal_votes_head, total_votes_head, percent_votes_head = headers_second_row

	# print(state_head, constituency_name_head)
	# print([result_head.lower()])
	# print([osn_head.lower(), candidate_name_head.lower(), party_name_head.lower(), evm_votes_head.lower(), postal_votes_head.lower(), total_votes_head.lower(), percent_votes_head.lower()])

	# sanity checks
	assert state_head.replace("&", "and") == state_name, "state name mismatch"
	# assert result_head.lower() == "results", "text mismatch"
	assert osn_head.lower() == "o.s.n.", "text mismatch"
	assert candidate_name_head.lower() == "candidate", "text mismatch"
	assert party_name_head.lower() == "party", "text mismatch"
	assert evm_votes_head.lower() == "evm votes", "text mismatch"
	assert postal_votes_head.lower() == "postal votes", "text mismatch"
	assert total_votes_head.lower() == "total votes", "text mismatch"
	assert percent_votes_head.lower() == "% of votes", "text mismatch"

	if state_name != "Jammu and Kashmir":
		keys = ["state_name", "constituency_name", "constituency_code", "sl_no", "candidate_name", "party_name", "evm_votes", "postal_votes", "total_votes"]
	else:
		keys = ["state_name", "constituency_name", "constituency_code", "sl_no", "candidate_name", "party_name", "evm_votes", "migrant_votes", "postal_votes", "total_votes"]

	result = []
	for row in rows[3:-1]: # exclude header rows and total row
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]
		result.append(dict(zip(keys, [state_name, constituency_name_head, constituency_code] + cols)))

	return result