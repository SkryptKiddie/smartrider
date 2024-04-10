# Reading a SmartRider

## Method 1 (smartrider_reader.py)
1. With your `dump.mfc` file, run `python3 smartrider_reader.py dump.mfc`.
2. The program will parse the dump and provide you with the information that is stored on the card, like tag on/offs, issue and expiry dates, concession type and balance.

## Method 2 (Hex editor)
With your hex editor of choice, you can browse the contents of the dump yourself.
Offsets of note:
- `0x280` to `0x340` is tag on and tag off records.
- `0xe0` is the card balance in cents.
- `0x50` is the card token and card issue date.
- `0x52` is the card token expiry date.

## Concession token values
| Token Hex | Value |
| --- | ----------- |
| 0x00 | Pre-issue (Before first use) |
| 0x01 | Standard Fare |
| ? | General Concession |
| 0x02 | Student Concession |
| 0x04 | Tertiary Concession |
| 0x06 | Seniors Conession |
| 0x07 | Health Care Conession |
| 0x0e | PTA Staff (Free travel) |
| 0x0f | Pensioner Concession (Free travel) |
| 0x10 | Free travel | 
| ? | Veteran's Concession | 
| ? | ASH Concession |
https://www.transperth.wa.gov.au/SmartRider/Types-of-SmartRider
