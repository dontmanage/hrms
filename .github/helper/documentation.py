import sys
import requests
from urllib.parse import urlparse


docs_repos = [
	"dontmanage_docs",
	"dontmanageerp_documentation",
	"dontmanageerp_com",
	"dontmanage_io",
]


def uri_validator(x):
	result = urlparse(x)
	return all([result.scheme, result.netloc, result.path])

def docs_link_exists(body):
	for line in body.splitlines():
		for word in line.split():
			if word.startswith('http') and uri_validator(word):
				parsed_url = urlparse(word)
				if parsed_url.netloc == "github.com":
					parts = parsed_url.path.split('/')
					if len(parts) == 5 and parts[1] == "dontmanage" and parts[2] in docs_repos:
						return True
				elif parsed_url.netloc == "docs.dontmanageerp.com":
					return True


if __name__ == "__main__":
	pr = sys.argv[1]
	response = requests.get("https://api.github.com/repos/dontmanage/dontmanageerp/pulls/{}".format(pr))

	if response.ok:
		payload = response.json()
		title = (payload.get("title") or "").lower().strip()
		head_sha = (payload.get("head") or {}).get("sha")
		body = (payload.get("body") or "").lower()

		if (title.startswith("feat")
			and head_sha
			and "no-docs" not in body
			and "backport" not in body
		):
			if docs_link_exists(body):
				print("Documentation Link Found. You're Awesome! 🎉")

			else:
				print("Documentation Link Not Found! ⚠️")
				sys.exit(1)

		else:
			print("Skipping documentation checks... 🏃")
