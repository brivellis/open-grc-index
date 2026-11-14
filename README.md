# Brivellis Open GRC Index

A free, open index of governance, risk and compliance (GRC) resources:

- **open-source tools**
- **free templates and kits**
- **free courses**
- **MCP servers and AI connectors**
- **open datasets and mappings**
- **official free guidance**

It covers ISO/IEC 27001, ISO/IEC 20000-1, ISO 22301, ISO/IEC 42001 and NIST CSF 2.0, plus Gulf frameworks: NCA ECC, SAMA CSF, the Saudi PDPL and the UAE Information Assurance standard.

The index is published at **https://brivellis.com/open-grc-index/** and as data at **https://brivellis.com/open-grc-index/index.json**.

## How the index works
- **Free to be listed, free to use.** Listings cannot be bought, and nothing is ranked.
- **Alphabetical everywhere.** No "best" lists and no popularity order.
- **Sourced facts only.** Every entry lists the public pages its facts come from and the date they were checked. A feature flag (MCP server, API, `llms.txt`, Arabic) says **yes** only when the maintainer documents it. **Unknown does not mean no.**
- **Our own words.** Brivellis Editorial writes the summaries. A summary supplied by a maintainer is marked as such.
- **House entries are labelled.** Resources made by Brivellis are marked **House**, meet the same rules and are never placed above others.
- **No personal data.** Registration happens on GitHub; we collect no email addresses and run no forms of our own.

## Register a resource
1. Read the [listing rules](LISTING-RULES.md).
2. Open a **[registration issue](../../issues/new?template=register.yml)**, or open a pull request that adds one file to `entries/` (see [CONTRIBUTING.md](CONTRIBUTING.md)).
3. Brivellis Editorial reviews it against the rules. We aim to answer within 7 days, and explain any refusal in the issue.
4. Once listed, you can add the badge to your README or site:

   [![Listed in the Brivellis Open GRC Index](badge/listed.svg)](https://brivellis.com/open-grc-index/)

## Correct or remove an entry
Open a **[correction issue](../../issues/new?template=correction.yml)**. Removal requests from a maintainer are always honoured.

## Repository layout
| Path | What it holds |
|---|---|
| `entries/` | One YAML file per resource, named `<id>.yaml` |
| `schema/entry.schema.json` | The fields every entry must have |
| `scripts/validate.py` | Checks entries against the schema and the rules (runs on every pull request) |
| `scripts/build_index.py` | Builds `dist/index.json` and `dist/llms.txt` for the site |
| `badge/` | The "Listed in" badge |

```bash
pip install pyyaml jsonschema
python3 scripts/validate.py
python3 scripts/build_index.py
```

## Licences
- Index data (`entries/`, `dist/`): [CC BY 4.0](LICENSE-DATA). Credit "Brivellis Open GRC Index".
- Scripts, schema and workflow: [MIT](LICENSE).
- Names of products and standards are trademarks of their owners and are used only to identify them. Listing is not an endorsement, and the index does not certify anything.

Maintained by Brivellis Editorial · https://brivellis.com
