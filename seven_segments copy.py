import re

regex_seven = '[0-9abcdefgABCDEFG-]'

def FindLongestWord(word_array):
    current_longest = ""
    for word in word_array:
        if len(word) >= len(current_longest):
            # print("Current word: " + word)
            contender = re.search(regex_seven, word)
            if contender == None:
                current_longest = word
            # print("Longest word so far: " + current_longest)
    return current_longest

def main():
    dictionary = open("english_dictionary.txt", 'r')
    # print(dictionary.readlines())
    all_words = dictionary.readlines()[1000:]
    longest_word = FindLongestWord(all_words)
    print(longest_word)

if __name__ == "__main__":
    main()
