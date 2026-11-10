# Instagram Username Discovery

A conservative research toolkit for generating and organizing short Instagram username candidates. The initial target is the complete two-character search space.

## What it does
- Generates all two-character candidates from lowercase letters, digits and underscore.
- Applies configurable syntax checks.
- Exports a CSV research ledger with profile URLs and evidence/status fields.
- Separates **format-valid**, **public-profile evidence**, and **claimability**.
- Supports manual evidence recording and reproducible candidate ranking.

## Important limitation
This project does **not** claim to determine Instagram availability automatically. Instagram does not provide a public bulk username-availability API. A profile URL that does not load is not proof that a username is claimable: names can be reserved, disabled, recently released, or otherwise unavailable. Final confirmation must be performed in Instagram's own username field.

The project deliberately does not automate high-volume scraping, evade rate limits, rotate proxies, or bypass access controls. Use manual checks and respect Instagram's Terms and platform controls.

## Username format assumptions
The generator uses the commonly documented character set:
- lowercase letters `a-z`
- digits `0-9`
- underscore `_`
- period `.`

For two-character handles, a period cannot appear because it cannot be at the beginning or end. The default two-character alphabet is therefore 37 symbols (26 letters + 10 digits + underscore), giving **1,369 candidates**. The tool does not assume that digit-only or underscore-containing handles are available; it simply keeps them in the candidate set for verification.

Platform rules can change. Treat syntax validation as a preliminary filter, not a guarantee of registration eligibility.

## Quick start

Requires Python 3.10+; no third-party packages required.

```bash
cd instagram_username_discovery
python -m username_discovery generate --length 2 --output data/two_character_candidates.csv
```

To generate 1–4 character candidates:

```bash
python -m username_discovery generate --min-length 1 --max-length 4 --output data/candidates_1_to_4.csv
```

To validate an existing CSV:

```bash
python -m username_discovery validate data/two_character_candidates.csv
```

## Verification workflow
1. Generate the candidate inventory.
2. Review known brand, abbreviation, product and public-figure associations using independent sources.
3. Open the profile URL only as a preliminary observation; record whether a public profile was actually observed.
4. Enter the exact candidate in Instagram's **Edit profile → Username** field.
5. Record the result and date. Only mark `CONFIRMED_AVAILABLE_IN_INSTAGRAM` when Instagram accepts the username in its own interface and allows the change to proceed.
6. If the result is ambiguous, use `UNKNOWN`, not available.

## Evidence statuses
- `NOT_CHECKED`: no review yet.
- `PUBLIC_PROFILE_OBSERVED`: public account evidence observed.
- `NO_PUBLIC_PROFILE_OBSERVED`: profile not observed; **not proof of availability**.
- `KNOWN_ASSOCIATION`: credible external brand/person/term association.
- `CONFIRMED_TAKEN_IN_INSTAGRAM`: Instagram explicitly rejects it as taken.
- `CONFIRMED_UNAVAILABLE_IN_INSTAGRAM`: Instagram explicitly says it cannot be used, reason may be reserved/restricted.
- `CONFIRMED_AVAILABLE_IN_INSTAGRAM`: Instagram accepts it in the registration/edit flow.
- `UNKNOWN`: inconclusive.

## Output columns
`username,length,format_valid,profile_url,evidence_status,association,source_url,checked_at,notes`

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```
instagram_username_discovery/
  README.md
  pyproject.toml
  username_discovery/
    __init__.py
    __main__.py
    generator.py
    ledger.py
  tests/
    test_generator.py
  data/
    known_associations.csv
```
