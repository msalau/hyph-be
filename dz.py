#!/usr/bin/python3

# General rule:
# if it is a verb and has form without a prefix => <prefix>7<root>,
# else <prefix>8<root>

PATTERNS = [
    '.ад8зін',
    '.ад7жал',
    '.ад7жат',
    '.ад7жац',
    '.ад7жаў',
    '.ад7жар',
    '.ад8жгір',
    '.ад7жлукц',
    '.ад7жлукч',
    '.ад7жыв',
    '.ад7жыл',
    '.ад7жын',
    '.ад7жыт',
    '.ад7жыць',
    '.ад7жыў',
    '.ад7зав',
    '.адзалі', #?
    '.адзалю', #?
    '.адзалён', #?
    '.ад7зван',
    '.ад7звон',
    '.ад8зеж',
    '.ад8зел',
    '.ад8зен',
    '.ад8зеравян',
    '.ад8зервянел',
    '.ад8зет',
    '.ад8зец',
    '.ад8зеў',
    '.ад7знак',
    '.ад7знач',
    '.ад7знац',
    '.адзол', #?
    '.ад7зыва',
    '.ад7зыўн',
    '.ад8зява',
    '.адзёр', #?
    '.ад8зіч',
    '.на8д7звычай',
    '.на7д8зея',
    '.на7д8зеі',
    '.на7д8зею',
    '.на7д8зей',
    '.на7д8зел',
    '.на8д7земн',
    '.на7д8зен',
    '.на7д8зер',
    '.на7д8зет',
    '.на7д8зец',
    '.на7д8зеў',
    '.на7д8зява',
    '.на7д8зьм',
    '.на7д8зял',
    '.на7д8зяр',
    '.на7д8зёр',
    '.на7д8зір',
    '.на7д8зён',
    '.на7д8зів',
    '.на7д8зім',
    '.на7д8зіўлюся',
    '.па8д7жар',
    '.па8д7жыв',
    '.па8д7жыць',
    '.па8д7жыў',
    '.па8д7жыл',
    '.па8д7зав',
    '.па8д7загалова',
    '.па8д7загалоў',
    '.па8д7закус',
    '.па8д7закуш',
    '.па8д7зараб',
    '.па8д7зароб',
    '.па7д8звіжнік',
    '.па7д8звіжніц',
    '.па7д8зе.',
    '.па7д8зеж',
    '.па7д8зяж',
    '.па7д8зей',
    '.па7д8зел',
    '.па7д8зял',
    '.па8д7земн',
    '.па8д7зяме',
    '.па7д8зен',
    '.па7д8зец',
    '.па7д8зеў',
    '.па7д8зер',
    '.па7д8зяр',
    '.па7д8зея',
    '.па7д8зеі',
    '.па7д8зею',
    '.падзеш.', #?
    '.падзол', #?
    '.па8д7зор',
    '.па8д7зыва',
    '.па7д8зьм',
    '.па7д8зяк',
    '.па7д8зяц',
    '.па7д8зяўб',
    '.па7д8зёўб',
    '.па7д8зём',
    '.па7д8зён',
    '.па7д8зі.',
    '.па7д8зіце.',
    '.па7д8зів',
    '.па7д8зіў',
    '.па7д8зішах',
    '.пера7д8звіжнік',
    '.пера7д8звіжніц',
    '.пера7д8зе.',
    '.пера7д8зел',
    '.пера7д8зял',
    '.пера7д8зер',
    '.пера7д8зёр',
    '.пера7д8зяр',
    '.пера7д8зір',
    # Names
    '.надзеждзін',
    '.на7д8зю.',
    '.на7д8зя.',
    '.на7д8зяй.',
    '.на7д8зяю.',
    '.на7д8зі.',
]

def main():
    from sys import exit, stderr
    import re
    import fileinput

    # Read words
    words = []
    pattern = re.compile('^(п|н|пер)?ад(з|ж)')
    for word in fileinput.input():
        word = word.strip().lower()
        if len(word) >= 5 and pattern.match(word):
            words.append(word)
    words = sorted(words)
    words_num = len(words)

    start = re.compile("^\.")
    end = re.compile("\.$")
    digits = re.compile("\d")

    # Remove words that match patterns
    root = 0
    prefix = 0
    todo = 0
    pattern_prefix = 0
    pattern_root = 0
    pattern_todo = 0
    rules = {}
    for pattern in PATTERNS:
        if "д8з" in pattern or "д8ж" in pattern:
            pattern_root = pattern_root + 1
        elif "д7з" in pattern or "д7ж" in pattern:
            pattern_prefix = pattern_prefix + 1
        else:
            pattern_todo = pattern_todo + 1

        p1 = start.sub("^", pattern)
        p2 = end.sub("$", p1)
        p3 = digits.sub("", p2)
        regex = re.compile(p3)

        tmp = []
        for word in words:
            if regex.match(word):
                if "д8з" in pattern or "д8ж" in pattern:
                    root = root + 1
                    if "7д8з" in pattern or "7д8ж" in pattern:
                        word = word.replace("д", "-д", 1)
                elif "д7з" in pattern or "д7ж" in pattern:
                    prefix = prefix + 1
                    word = word.replace("д", "д-", 1)
                else:
                    todo = todo + 1

                if pattern not in rules:
                    rules[pattern] = []
                rules[pattern].append(word)
            else:
                tmp.append(word)
        words = tmp

    # Check for conflicts
    for p1 in PATTERNS:
        p1s = digits.sub("", p1)
        for p2 in PATTERNS:
            p2s = digits.sub("", p2)
            if p1 != p2 and ((p1s in p2s) or (p2s in p1s)):
                print("Conflict: {} {}".format(p1, p2))

    if words:
        l = words[:20]
        print("Next {} word(s) from {}:".format(len(l), len(words)), file=stderr)
        print('\n'.join(l), file=stderr)
        exit(1)
    else:
        print("Congratulations! All words are examined!")
        #print("{} patterns cover {} words".format(len(PATTERNS), words_num))
        print("Words: prefix = {:4}, root = {:4}, todo = {:4}".format(prefix, root, todo))
        print("Rules: prefix = {:4}, root = {:4}, todo = {:4}".format(pattern_prefix, pattern_root, pattern_todo))

    print()
    print()
    todo_list = []
    for pattern in sorted(rules):
        if "7" not in pattern and "8" not in pattern:
            todo_list.append(pattern)
        else:
            print("{}: {}".format(pattern, " ".join(rules[pattern])))

    if todo_list:
        print()
        print("**************")
        print("**** TODO ****")
        print("**************")
        print()
        for pattern in todo_list:
            print("{}: {}".format(pattern, " ".join(rules[pattern])))

if __name__ == "__main__":
    main()
