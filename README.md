# LeetHelix

Practice your Helix editor skills with code challenges.

## Installation

```bash
git clone https://github.com/yourusername/leet-helix.git
cd leet-helix
pip install -e .
```

## Usage

### Initialize

First, initialize the database and example challenges:

```bash
leet init
```

### Play

Start a challenge session. The system will intelligently select a challenge for you.

```bash
leet play
```

To play a specific challenge:

```bash
leet play <challenge_id>
```

The challenge will open in Helix (`hx`). Edit the file to match the goal. When done, save and quit (`:wq`).

### List Challenges

See all available challenges.

```bash
leet list
```

### Stats

Check your progress.

```bash
leet stats
```

### Add Challenge

Create your own challenges.

```bash
leet add
```

## Development

Run tests:

```bash
pytest
```
