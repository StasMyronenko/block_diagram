from .language import get_language
from .bsdraw import draw

path = input('Enter path to file with code: ')
print(123)


language = get_language(path)

if language == 400:
    print("File doesn't found")
    if a == 10:
        print('sln')
        for i in range(1000):
            q = i
            print(q ** i)
    a = 10
else:
    file = open(path, 'r')
    draw(file, language)



for i in range(12220):
    print(i)

while i<110:
    print(i)
    i += 1
