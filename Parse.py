#!/usr/bin/env python3

__author__ = 'skyem123'

class ParseError(Exception):
    def __init__(self, description, position):
        """
        :param description: The description of the error
        :param position: The position of the error in the string, starts at 0
        """
        self.position = position
        self.description = description
    def __str__(self):
        return self.description

class ParseStringNotClosedError(ParseError):
    def __init__(self, position):
        """
        :param position: The position of the error in the string: position in the last character in the string, plus one
        """
        self.position = position
        self.description = "Reached end of line, string not closed"
    def __str__(self):
        return self.description


class LangEval:
    inc_dec_operators = ['++', '--']
    set_operators = ["=", '+=', '-=']

    def __init__(self, functions=[], variables=[]):
        # Set the initial variables
        self.functions = functions
        self.variables = variables

    def __eval_string(self, marker, string, position):
        # Get the part of the string we will need to process (the +1 cuts out the marker at the start)
        string = string[position+1:]
        final_string = ""
        l = len(string)
        # A Zero length string that is not closed cannot be detected by the other code
        if l == 0: raise ParseStringNotClosedError(position+1)
        # Loop through the string, finding the start and end, and the string
        i = 0
        while i < l:
            # Get the character
            char = string[i]
            # Check for the escape character
            if char == '\\':
                # make the loop skip once
                i += 1
                # get the character that is escaped
                escape_char = string[i:i+1]
                # escaped \
                if escape_char == '\\':
                    final_string += '\\'
                # escaped "
                elif escape_char == marker:
                    final_string += marker
                # newline
                elif escape_char == 'n':
                    final_string += "\n"
                # if there is an invalid escape character
                else:
                    raise ParseError("Invalid escape character", position + 1 + i + 1)
                # TODO: More escaped characters?
            # If the character found is the "marker" character, it's the end of the string
            elif char == marker:
                break
            # If it is just a normal character, add it to the found string!
            else:
                final_string += char
            # If we reached EOL without a closing "marker", we error.
            if i+1 == l:
                raise ParseStringNotClosedError(position + 2 + i)
            # Increment tne loop
            i += 1
        # return a tuple containing all the information found about the string
        return "string", final_string, position, i+1+position

    def __eval_number(self, string, position):  # TODO: allow forms of number other than base-10
        # Get the part of the string we need to process
        string = string[position:]
        # The string for storing our number before it is converted into a number
        number_string = ""
        number_type = "base10"  # TODO: more number types, and detect types. (TODO: use
        # Get the length of the string
        l = len(string)
        # Loop through the string to find the rest of the number
        for i, char in enumerate(string):
            # Is the character a digit?
            if char.isdigit():
                # Add the character to the number string
                number_string += char
            elif number_type == "base16" and ('A' or 'B' or 'C' or 'D' or 'E' or 'F' in char.upper()):
                number_string += char
            # Maybe it is a character that is meant to be in a number? Note: + and - are handled in other code
            # Is it a decimal point?
            elif char == '.':
                # If it is a base10 number, add it to the number string
                if number_type == "base10":
                    number_string += char
                    # And it is now are a decimal number
                    number_type = "base10-decimal"
                # Don't allow two decimal points
                elif number_type == "base10-decimal":
                    raise ParseError("More than one decimal point in a number", i)
                # Decimal point in a non base10 number?
                else:
                    raise ParseError("Decimal point in a non base10 number", i)
            # Is it an 'x', used for hexadecimal notation?
            elif char == 'x':
                if number_type == "base10":
                    number_string += char
                    number_type = "base16"
            else:  # We have encountered a character that is not a number, let the other
                # Return the number, along with position information.
                return "number", number_type, number_string, position, i-1+position
            # If this is the last character we return the needed information
            if i == l-1:
                return "number", number_type, number_string, position, i+position

    def __eval_unknown(self, string, position, terminators):
        # Get the part of the string we will need to process (the +1 cuts out the marker at the start)
        string = string[position:]
        found_token = ""
        l = len(string)
        # Loop through the string, finding the start and end, and the string
        i = 0
        while i < l:
            # Get the character
            char = string[i]
            # If the character is an allowed character, keep it.
            if char.isalnum() or char == '_':
                found_token += char
            else:  # If not, it's the last char!
                break

            # Increment tne loop
            i += 1
        # return a tuple containing all the information found about the string
        return "unknown", found_token, position, i+position-1

    def __tokenize(self, string):
        # List of operators
        operators = ['(', ')', '+', '-', '*', '/', '==', '!=','<', '>', '<=', '>=', '!', '\n', ';', '{', '}', '%',
                     '**', '\\', ',', '.', '[', ']'] + self.set_operators + self.inc_dec_operators
        # List of string markers
        string_markers = ['"', "'"]
        ## List of keywords
        #keywords = ["function", "class", "return", "extends", "implements"]
        # Where all the located and separated parts are
        parts = []
        # First, get rid of spaces before and after the string
        string = string.strip()
        # Get the length of the string
        string_length = len(string)
        # For finding known tokens
        found_token = ()
        # The loop (a for loop is not flexible enough)
        i = 0
        while i < string_length:
            # get the character at the current position
            char = string[i]

            # Is the character whitespace? (excluding newlines)
            if char.isspace() and char != '\n':
                i += 1  # increment the position
                continue  # If so, then skip checking for other stuff
            valid_token = False  # This thing is for detecting errors  TODO: Is there a better way to do this?

            # Is is the start of a string?
            if not valid_token:
                for marker in string_markers:  # TODO: is there a better way of doing this? if so, tell me how I can improve it. Don't just say it is bad!
                    if char == marker:
                        # Locate the string
                        located_string = self.__eval_string(marker, string, i)
                        # Make the loop skip to the end of the string to avoid reading it again. (located_string[3] is end)
                        i = located_string[3]
                        # We found a token!
                        found_token = located_string
                        # It's also a valid token
                        valid_token = True
                        break

            # Maybe it's an operator? (checked from longest to shortest order)
            # There is no function for locating operators as it is less messy doing it this way
            if not valid_token:
                for operator in sorted(operators, key=len, reverse=True):
                    # Check if the operator is in the string
                    if string[i:i+len(operator)] == operator:  # BASIC is case insensitive
                        # Skip the rest of the operator if it is in the string
                        i += len(operator) - 1
                        # We found a token!
                        found_token = ("operator", operator, i, i + len(operator) - 1)
                        # It's a valid token!
                        valid_token = True
                        break

            # What if it is a number?
            if char.isdigit() and not valid_token:
                # Locate the number
                located_number = self.__eval_number(string, i)
                # Make the loop skip till the end of the number to avoid reading it again (located_number[3] is the end)
                i = located_number[4]
                # We found the token!
                found_token = located_number
                # It's also a valid token
                valid_token = True

            # It could be unknown!
            if char.isalnum() and not valid_token:
                unknown = self.__eval_unknown(string, i, operators + string_markers)
                i = unknown[3]
                found_token = unknown
                valid_token = True

            # If the token is valid, add it to the parts list
            if valid_token:
                parts.append(found_token)
            else:  # If it isn't valid, we error!
                raise ParseError("Unrecognised token", i)

            # Increment the position
            i += 1
        return parts

    def __process_set_variable(self, next_token):
        if next_token[1] in self.set_operators:
            return (True, "set", next_token)
            # is it an increment / decrement operator?
        elif next_token[1] in self.inc_dec_operators:
            return True, ("inc_dec", next_token)
        else:
            return False
        pass

    def __process_raw_tokens(self, raw_tokens):
        if (len(raw_tokens) == 0) or len(raw_tokens[-1]) == 0 or (raw_tokens[-1][0] != "end_of_tokens"):
            raw_tokens.append(("end_of_tokens",))
        # Loop through the raw tokens
        i = 0
        while True:
            token = raw_tokens[i]
            print("[loop] token " + str(i) + " is: " + str(token))
            if token[0] == "end_of_tokens":
                break
            next_token = raw_tokens[i + 1]

            # If this token is unknown
            if token[0] == "unknown":
                print("[unknown] token " + str(i + 1) + " is: " + str(next_token))

                thing_name = token
                thing_modifiers = []
                thing_operation = ()

                # If the next token is unknown
                if next_token[0] == "unknown":
                    thing_modifiers += (token,)
                    while (next_token[0] == "unknown") and (raw_tokens[i + 2][0] == "unknown"):
                        thing_modifiers += (next_token,)
                        i+=1
                        next_token = raw_tokens[i + 1]
                        print("[type] token " + str(i + 1) + " is: " + str(next_token))
                    thing_name = next_token
                    i+=1
                    token = raw_tokens[i]
                    next_token = raw_tokens[i + 1]
                    thing_operation = ("variable_definition",)

                if next_token[0] == "operator":
                    # but / and if the next token is a set operator...
                    if next_token[1] in (self.set_operators + self.inc_dec_operators):
                        if (self.__process_set_variable(next_token))[0]:
                            thing_operation = ("variable_set", next_token)
                    else:
                        i-=1
                    i+=1

                print(thing_modifiers, thing_name, thing_operation)

            i+=1
            pass

    def eval(self, string):
        raw_tokens = self.__tokenize(string)
        print(raw_tokens)
        return self.__process_raw_tokens(raw_tokens)
        # TODO: process parts
        #for part in parts:

evalLine = LangEval().eval

inputData = ""
while True:
    inputData += input() + "\n"
    if inputData.endswith("\n\n"):
        try:
            print(evalLine(inputData))
            inputData = ""
        except ParseError as e:
            print(e.description + " at " + str(e.position))
            inputData = ""


