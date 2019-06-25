#This function opens a file and converts each line to a list element
def open_file_to_list(filepath):
    with open(filepath, 'r') as file:  # open the file
        list_of_lines = file.readlines()  # put the lines to a variable (list).
    return list_of_lines

#This function takes the list from previous function and strips the /n character
def open_file_to_list_clean(dirty_list):
    previous = open_file_to_list(dirty_list)
    list_of_lines_real = [i.rstrip() for i in previous] #strip new line character
    return list_of_lines_real

#This function creates two lists, one that is a matrix and the other that are the words
def categorize_lines(clean_list):
    previous = open_file_to_list_clean(clean_list)
    matrix = []
    words = []
    for i in previous:
        if ' ' in i:   #Looks for spaces in line to check for matrix letters
            matrix.append(i)
        elif i.isalpha(): #Looks for ONLY alphas in line
            words.append(i)
    matrix_final = "\n".join(matrix)
    return words,matrix_final

#Combine letters into a matrix without spaces and get the length of the matrix
def cleanse(orig_puzzle):
  letters_combined = categorize_lines(orig_puzzle)[1].replace(' ','')
  length_of_matrix = letters_combined.index('\n')+1 #Look for newline and add one
  return letters_combined,length_of_matrix

#Create a list of tuples where the first elements in each tuple is the letter and the second element
# is another tuple with index elements of the row and column
def add_indexes(matrix):
  letters_combined = cleanse(matrix)[0]
  length = cleanse(matrix)[1]
  character_index = []
  for idx, letter in enumerate(letters_combined):
    character_index.append((letter,divmod(idx,length)))
  return character_index, length

#This functions goes letter by letter, column by columns and goes in each possible directions
# specified below and captures the letter indices and returns a dictionary where the keys are the
# possible directions and values are tuples that include the letter and its corresponding index
def combinations(letters_and_indicies):
  d_word_combos = {}
  letter_indices_matrix = add_indexes(letters_and_indicies)[0]
  length = add_indexes(letters_and_indicies)[1]
  possible_directions = {'down': 0, 'down-left': -1, 'down-right': 1}

  for word_direction, combo in possible_directions.items():
    d_word_combos[word_direction] = []
    for x in range(length):
      for i in range(x, len(letter_indices_matrix), length + combo):
        d_word_combos[word_direction].append(letter_indices_matrix[i])
      d_word_combos[word_direction].append('\n')
  return d_word_combos, letter_indices_matrix

#This functions gets the reversed combinations for the backwards solutions.
# It's easier to reverse a matrix and add the list of potential solutions to the dictionary.
def all_combinations(dictionary):
  word_dict = combinations(dictionary)[0]
  chars = combinations(dictionary)[1]

  word_dict['right'] = chars
  word_dict['left'] = [i for i in reversed(chars)]
  word_dict['up'] = [i for i in reversed(word_dict['down'])]

  word_dict['up-left'] = [i for i in reversed(word_dict['down-right'])]

  word_dict['up-right'] = [i for i in reversed(word_dict['down-left'])]

  return word_dict


#This function looks for the words parsed out in the file and checks each direction to see if it applys to the specific puzzle
#If it does it prints it with the first letter index and the last letter index
def find_words(lines,solutions):
  letter_indices = all_combinations(lines)

  for direction, tuple_indices in letter_indices.items():
    string = ''.join([i[0] for i in tuple_indices])
    for word in solutions:
        if word in string and direction == "up":
            coordinates = tuple_indices[string.index(word)][1]
            print(word, coordinates[0], ':', coordinates[1], coordinates[0]-len(word)+1, ':', coordinates[1])
        elif word in string and direction == "down":
            coordinates = tuple_indices[string.index(word)][1]
            print(word, coordinates[0], ':', coordinates[1], coordinates[0]+len(word)-1, ':', coordinates[1])
        elif word in string and direction == "right":
            coordinates = tuple_indices[string.index(word)][1]
            print(word, coordinates[0], ':', coordinates[1], coordinates[0], ':', coordinates[1]+len(word)-1)
        elif word in string and direction == "left":
            coordinates = tuple_indices[string.index(word)][1]
            print(word, coordinates[0], ':', coordinates[1], coordinates[0], ':', coordinates[1]-len(word)+1)
        elif word in string and direction == "down-left":
            coordinates = tuple_indices[string.index(word)][1]
            print(word, coordinates[0], ':', coordinates[1], coordinates[0]+len(word)-1, ':', coordinates[1]-len(word)+1)
        elif word in string and direction == "down-right":
            coordinates = tuple_indices[string.index(word)][1]
            print(word, coordinates[0], ':', coordinates[1], coordinates[0]+len(word)-1, ':', coordinates[1]+len(word)-1)
        elif word in string and direction == "up-right":
            coordinates = tuple_indices[string.index(word)][1]
            print(word, coordinates[0], ':', coordinates[1], coordinates[0]-len(word)+1, ':', coordinates[1]+len(word)-1)
        elif word in string and direction == "up-left":
            coordinates = tuple_indices[string.index(word)][1]
            print(word, coordinates[0], ':', coordinates[1], coordinates[0]-len(word)+1, ':', coordinates[1]-len(word)+1)

#Main function
def main():
    file_path = input("Please type the full path of the file: ")
    #Example: C:\\Users\\Drew Nicolette\\Desktop\\misc\\test.txt
    find_words(file_path,categorize_lines(file_path)[0])

main()
