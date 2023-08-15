import json, requests

url = 'https://questions.aloc.com.ng/api/v2/m?subject=physics'

headers = {
	'Content-Type': 'application/json',
	'Accept': 'application/json',
	'AccessToken': 'ALOC-661b77989251576c6677 '
}

def get_questions(subject):
	r = requests.get(f'https://questions.aloc.com.ng/api/v2/m?subject={subject}', headers=headers)
	d = r.json()

	with open(f'Questions1/{subject} questions', 'w') as f:
		json.dump(d, f)

subjects = ['physics', 'chemistry', 'biology', 'commerce', 'accounting', 'mathematics', 'history', 'economics', 'geography', 'government', 'english',
			'englishlit', 'crk', 'irk', 'civiledu', 'government']

for subject in subjects:
	get_questions(subject)
