#TODO correct draw 'else'. Without delete connection. Don't draw connect to else. Mb markered blocks in else or something else
from languages import get_language
from bsdraw import draw
import pdb

#path = input('Enter path to file with code: ')
path = 'test.py'

# lang = input('Enter language in lowercase(if you don\'t now, just press key Enter): ')
language = get_language(path)

if language == 400:
    print("File doesn't found")
else:
    file = open(path, 'r')  
    draw(path, language)
    file.close()

