# Contributing

Thank you for helping keep the index useful. There are two ways to add a resource.

## Option 1: a registration issue (no YAML needed)
Open a [registration issue](../../issues/new?template=register.yml) and fill in the form. Brivellis Editorial writes the entry and links the pull request in your issue.

## Option 2: a pull request
1. Fork the repository and create a branch.
2. Copy `entries/_example.yaml.txt` to `entries/<id>.yaml`. The `id` is lower-case words joined by hyphens, and it must match the file name.
3. Fill in every field. Each field is described in `schema/entry.schema.json`.
   - `summary`: 20–300 characters, plain description, no ranking or sales words.
   - `frameworks`: use the values in the schema; do not write clause or control titles.
   - `ai_ready`: write `yes` only with a link to the maintainer's own documentation in the matching `*_source` field. Otherwise use `unknown`.
   - `sources`: the public pages that support your facts.
   - `last_checked`: today's date.
   - Put `"yes"`, `"no"` and dates in double quotes, so YAML keeps them as text.
   - `house`: always `false` (only Brivellis resources are house entries).
   - `maintainer_text`: `true` if you wrote the summary for your own resource.
4. Run the checks locally:
   ```bash
   pip install pyyaml jsonschema
   python3 scripts/validate.py
   python3 scripts/build_index.py
   ```
5. Commit the entry **and** the rebuilt `dist/` files, then open the pull request.

The automatic check must pass before review. A maintainer of Brivellis Editorial reviews against the [listing rules](LISTING-RULES.md).

## Corrections
Open a [correction issue](../../issues/new?template=correction.yml), or a pull request that edits the entry and updates `last_checked` and `sources`.

## Conduct
Be accurate and courteous. Do not submit personal data about private individuals.
