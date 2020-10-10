# These are the emails you will be censoring. The open() function is opening the text file that the emails are contained in and the .read() method is allowing us to save their contexts to the following variables:
email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()
marking = 'X'
def hide_it(num):
        return marking * num

def mark_text(text, index, length):
	return text[0:index] + hide_it(length) + text[index+length:]

def format_text(text):
        return text.lower()

def format_phrase(phrase):
        return phrase.lower()

def get_index(text, phrase, offset=0):
        return format_text(text).find(format_phrase(phrase), offset)

def censor(text, phrase, siblings = False):

        censored_text = text
        index = get_index(censored_text, phrase)

        while index != -1:
                censored_text = mark_text(censored_text, index, len(phrase))

                if siblings != False:
                        censored_text = censor_siblings(censored_text, index, len(phrase))
                        
                index = get_index(censored_text, phrase)

        return censored_text

def censor_list(text, phrases, censor_siblings = False):

        for phrase in phrases:
                text = censor(text, phrase, censor_siblings)

        return text

def get_indexes(text, needle):
    search_text = text
    length = len(needle)
    indexes = []
    offset = 0
    index = get_index(text, needle, offset)

    while index != -1:
        offset = index + length
        indexes.append(index)
        index = get_index(text, needle, offset)

    return indexes

def censor_negative_words(text, negative_words, siblings = False):
    indexes = []
    lengths = []

    for negative_word in negative_words:
        length = len(negative_word)
        for index in get_indexes(text, negative_word):
            lengths.append(length)
            indexes.append(index)

    total = len(indexes)
    if total > 1:
        cuts = list(zip(indexes, lengths))
        cuts.sort()
        
        #shift an element
        cuts = cuts[1:]
        for cut in cuts:
            text = mark_text(text, cut[0], cut[1])
            if siblings != False:
                    text = censor_siblings(text, cut[0], cut[1])

    return text

def censor_siblings(text, index, length):
    left_word = get_left_word(text[:index])
    right_word = get_right_word(text[index+length:])
    if left_word != False:
        text = mark_text(text, left_word[0], left_word[1])
    if right_word != False:
        text = mark_text(text, right_word[0] + index + length, right_word[1])
    return text

def get_left_word(text):
        text_len = len(text)
        offset = text_len-len(text.rstrip())
        word_len = 0
        for i in range(text_len-offset-1, 0, -1):
                if text[i].strip() == "":
                        break
                
                word_len += 1

        if word_len > 0:
                return [text_len - (word_len+offset), word_len]

        return False

def get_right_word(text):
    text_len = len(text)
    offset = text_len-len(text.lstrip())
    word_len = 0
    for i in range(offset, text_len):
        if text[i].strip() == "":
            break;
        word_len += 1
    if word_len > 0:
        return [offset, word_len]

    return False

proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation", "learning algorithm", "her", "herself"]
negative_words = ["concerned", "behind", "danger", "dangerous", "alarming", "alarmed", "out of control", "help", "unhappy", "bad", "upset", "awful", "broken", "damage", "damaging", "dismal", "distressed", "distressed", "concerning", "horrible", "horribly", "questionable"]



#print(email_one)
email_one_cencored = censor(email_one, 'learning algorithms');
#print(email_one_cencored)

email_two_cencored = censor_list(email_two, proprietary_terms)
#print(email_two_cencored)

email_three_cencored = censor_list(email_three, proprietary_terms)
email_three_cencored_negative_words = censor_negative_words(email_three_cencored, negative_words)
#print(email_three_cencored_negative_words)
print(email_four)

print("__________________")

email_four_cencored = censor_list(email_four, proprietary_terms, True)
email_four_cencored_negative_words = censor_negative_words(email_four_cencored, negative_words, True)
print(email_four_cencored_negative_words)

#input("Press enter to exit ;)")
