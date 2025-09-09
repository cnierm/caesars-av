# caesars-av
Caesar's Avalanche is a simple cypher written in Python. Small changes in input create large changes in output (the avalanche effect), but any encoded text can easily be decoded to it's original form.

## Usage

Caesar's Avalanche is a command line, file based tool. Here is the help menu found from passing the `-h` flag through

`options:`

`  -h, --help           show this help message and exit`

`  -d, --decode DECODE  File to decode`

`  -e, --encode ENCODE  File to encode`


output files will have a `.e` added to them (ex: file.txt -> file.e.txt) when encoded. The .e is removed upon decoding. If decoding and no .e exists, a `.d` is added.

## How does it work?
At a basic level, Caesar's Avalanche is able to compute a seed from any valid text input. While shifting each character, this seed is maintained. This means that if one were to decode the text, the program is able to find the original seed and shift each character back to it's original position. 

The avalanche effect comes from a perceived randomness through computing the seed, even though it is actually predictable. At a surface level, integers are fed into a sine curve that outputs in a "predictably random" fashion.
