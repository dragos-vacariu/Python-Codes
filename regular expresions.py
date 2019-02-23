#A regular expression is a special sequence of characters that helps you match or find other strings or sets
#of strings, using a specialized syntax held in a pattern.

#The match() function -> This function attempts to match RE pattern to string with optional flags.
#Syntax: re.match(pattern, string, flags=0)
#pattern    This is the regular expression to be matched.
#string	    This is the string, which would be searched to match the pattern at the beginning of string.
#flags	    You can specify different flags using bitwise OR (|). These are modifiers, which are listed in the table below.

#The re.match function returns a match object on success, None on failure. We usegroup(num) or groups()
#function of match object to get matched expression.

import re #This library is used for regular expressions (re)

line = "Cats are smarter than dogs"

matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I) #find something at the beginning of the string and return a match object.

if matchObj:
   print ("matchObj.group() : {0}" .format(matchObj.group()))
   print ("matchObj.group(1) : {0}" .format (matchObj.group(1)))
   print ("matchObj.group(2) : {0}" .format(matchObj.group(2)))
else:
   print ("No match!!")

matchObj = re.match( "Cats", line, 0)
if matchObj:
   print ("matchObj.group() : {0}" .format(matchObj.group()))
   #print ("matchObj.group(1) : {0}" .format(matchObj.group(1)))
   #print ("matchObj.group(2) : {0}" .format(matchObj.group(2)))
else:
   print ("No match!!")

#The search() function - This function searches for first occurrence of RE pattern within string with optional flags.
searchObj = re.search( r'dogs*', line, re.M|re.I) #re* -> Matches 0 or more occurrences of preceding expression.
if searchObj:
   print ("searchObj.group() : {0}" .format(searchObj.group()))
   #print ("searchObj.group(1) : {0}" .format (searchObj.group(1)))
   #print ("searchObj.group(2) : {0}" .format(searchObj.group(2)))
else:
   print ("No match!!")

#Match checks for a match only at the beginning of the string, while search checks for a match anywhere in the string.

#The sub() function - replaces all occurrences of the pattern in the string with 'repl'
#Syntax: re.sub(pattern, repl, string, max=0)

phone = "2004-959-559 # This is Phone Number"

# Delete Python-style comments
num = re.sub(r'#.*$', "", phone)
print ("Phone Num : {0}" .format(num))

# Remove anything other than digits
num = re.sub(r'\D', "", phone)    
print ("Phone Num : {0}" .format(num))

#THIS STATEMENT WILL THE COMMAND PROMPT OPEN UNTIL THE NEXT BUTTON PRESS:
input("\nPress any key to exit: ")

#Following table lists the regular expression syntax that is available in Python :

#Pattern	Description
#^	Matches beginning of line.
#$	Matches end of line.
#.	Matches any single character except newline. Using m option allows it to match newline as well.
#[...]	Matches any single character in brackets.
#[^...]	Matches any single character not in brackets
#re*	Matches 0 or more occurrences of preceding expression.
#re+	Matches 1 or more occurrence of preceding expression.
#re?	Matches 0 or 1 occurrence of preceding expression.
#re{ n}	Matches exactly n number of occurrences of preceding expression.
#re{ n,}	Matches n or more occurrences of preceding expression.
#re{ n, m}	Matches at least n and at most m occurrences of preceding expression.
#a| b	Matches either a or b.
#(re)	Groups regular expressions and remembers matched text.
#(?imx)	Temporarily toggles on i, m, or x options within a regular expression. If in parentheses, only that area is affected.
#(?-imx)	Temporarily toggles off i, m, or x options within a regular expression. If in parentheses, only that area is affected.
#(?: re)	Groups regular expressions without remembering matched text.
#(?imx: re)	Temporarily toggles on i, m, or x options within parentheses.
#(?-imx: re)	Temporarily toggles off i, m, or x options within parentheses.
#(?#...)	Comment.
#(?= re)	Specifies position using a pattern. Doesn't have a range.
#(?! re)	Specifies position using pattern negation. Doesn't have a range.
#(?> re)	Matches independent pattern without backtracking.
#\w	Matches word characters.
#\W	Matches nonword characters.
#\s	Matches whitespace. Equivalent to [\t\n\r\f].
#\S	Matches nonwhitespace.
#\d	Matches digits. Equivalent to [0-9].
#\D	Matches nondigits.
#\A	Matches beginning of string.
#\Z	Matches end of string. If a newline exists, it matches just before newline.
#\z	Matches end of string.
#\G	Matches point where last match finished.
#\b	Matches word boundaries when outside brackets. Matches backspace (0x08) when inside brackets.
#\B	Matches nonword boundaries.
#\n, \t, etc.	Matches newlines, carriage returns, tabs, etc.
#\1...\9	Matches nth grouped subexpression.
#\10	Matches nth grouped subexpression if it matched already. Otherwise refers to the octal representation of a character code.

#Option flags:

#Modifier	Description
#re.I	Performs case-insensitive matching.
#re.L	Interprets words according to the current locale. This interpretation affects the alphabetic group (\w and \W), as well as word boundary behavior (\b and \B).
#re.M	Makes $ match the end of a line (not just the end of the string) and makes ^ match the start of any line (not just the start of the string).
#re.S	Makes a period (dot) match any character, including a newline.
#re.U	Interprets letters according to the Unicode character set. This flag affects the behavior of \w, \W, \b, \B.
#re.X	Permits "cuter" regular expression syntax. It ignores whitespace (except inside a set [] or when escaped by a backslash) and treats unescaped # as a comment marker.

#Character classes
#Example	Description
#[Pp]ython	Match "Python" or "python"
#rub[ye]	Match "ruby" or "rube"
#[aeiou]	Match any one lowercase vowel
#[0-9]	Match any digit; same as [0123456789]
#[a-z]	Match any lowercase ASCII letter
#[A-Z]	Match any uppercase ASCII letter
#[a-zA-Z0-9]	Match any of the above
#[^aeiou]	Match anything other than a lowercase vowel
#[^0-9]	Match anything other than a digit

#Special Character Classes
#Example	Description
#.	Match any character except newline
#\d	Match a digit: [0-9]
#\D	Match a nondigit: [^0-9]
#\s	Match a whitespace character: [ \t\r\n\f]
#\S	Match nonwhitespace: [^ \t\r\n\f]
#\w	Match a single word character: [A-Za-z0-9_]
#\W	Match a nonword character: [^A-Za-z0-9_]


#Repetition Cases
#Example	Description
#ruby?	Match "rub" or "ruby": the y is optional
#ruby*	Match "rub" plus 0 or more ys
#ruby+	Match "rub" plus 1 or more ys
#\d{3}	Match exactly 3 digits
#\d{3,}	Match 3 or more digits
#\d{3,5}	Match 3, 4, or 5 digits
