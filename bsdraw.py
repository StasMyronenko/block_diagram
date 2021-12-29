from PIL import Image, ImageDraw
import pdb
import settings
from math import ceil
import random


def draw(path, language):
    if language == "python":
        code = file_to_list(path)
        draw_list = create_func_list_python(code.copy())
    elif language == "c++":
        draw_cpp(file)
    elif language == "c#":
        draw_cs(file)

    draw_list.append(block_count(code))
    draw_from_list(draw_list)

def file_to_list(path):
    code = []

    file = open(path, 'r')
    for line in file:
        if '#' in line:
            if line.count("'", 0, line.index('#')) % 2 == 0 and line.count('"', 0, line.index('#')) % 2 == 0:
                line = line[:line.index('#')]
        if line.strip() != '':
            code.append(line)
    file.close()
    return code

def create_func_list_python(code, space_count=0):
    res = []

    while code != []:
        line = code.pop(0)
        if line[:space_count] == ' ' * space_count and line[space_count] != ' ':
            if 'input(' in line[line.find('='):]:
                var = line[space_count:line.find('=')].strip()
                res.append(f'input {var}')
            elif line[space_count:space_count+6] == 'print(':
                var = line.strip()[6:-1]
                res.append(f'output {var}')
            elif line[space_count:space_count+2] == 'if':
                var = line[line.find('if') + 2:-2].strip()
                added = ['if', var]
                added.extend(create_func_list_python(code, space_count=space_count+4))
                res.append(added)
            elif line[space_count:space_count+4] == 'else':
                added = ['else']
                added.extend(create_func_list_python(code, space_count=space_count+4))
                res.append(added)

            elif line[space_count:space_count+3] == 'for':
                var = line[line.find('for') + 3:-2].strip()
                added = ['for', var]
                added.extend(create_func_list_python(code, space_count=space_count+4))
                res.append(added)

            elif line[space_count:space_count + 5] == 'while':
                var = line[line.find('while') + 5:-2].strip()
                added = ['while', var]
                added.extend(create_func_list_python(code, space_count=space_count+4))
                res.append(added)

            else:
                res.append(line.strip())

        elif line[:space_count] != ' ' * space_count:
            code.insert(0, line)
            return res


    return res

def draw_from_list(dlist):
    el_count = dlist.pop() + 2
    size = ceil(el_count ** 0.5)
    end_size = [size * (settings.WIDTH + settings.SPACE_WIDTH), size * (settings.HEIGHT + settings.SPACE_HEIGHT)]
    img = Image.new('RGB', end_size, settings.BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    coor = settings.START_POSITION.copy()
    el_draw(draw, coor, 'start')
    #pdb.set_trace()
    #draw_connections(draw, coor.copy(), dlist)
    create_img(draw, coor, dlist)
    el_draw(draw, coor, 'end')

    img.save(settings.PATH)


def create_img(img, coor, dlist=[]):
    while dlist != []:
        el = dlist.pop(0)
        next_else = (len(dlist) > 0 and dlist[0][0] == 'else')
        el_draw(img, coor, el, next_else)


def el_draw(img, coor, el, next_else=False):
    if el in ['start', 'end']:
        start_or_end(img, coor, text=el)
        if el == 'start':
            #connection(img, coor, img.im.size)
            change_coor(img, coor)
        
    elif type(el) == str:
        if el[:6] in ['input ', 'output']:
            draw_io(img, coor, el)
        else:
            draw_block(img, coor, el)


        #connection(img, coor, img.im.size)
        change_coor(img, coor)

    elif type(el) == list:
        block_type = el.pop(0)
        
        if block_type == 'if':

            block_body = el.pop(0)
            draw_if(img, coor, block_body)
            #connection(img, coor, img.im.size, True, block_count(el))
            change_coor(img, coor)
            create_img(img, coor, el)

        elif block_type == 'else':
            create_img(img, coor, el)

        elif block_type in ['for', 'while']:
            block_body = el.pop(0)
            draw_cycle(img, coor, block_body)
            #connection(img, coor, img.im.size)
            change_coor(img, coor)
            create_img(img, coor, el)
            draw_end_cycle(img, coor)
            #connection(img, coor, img.im.size)
            change_coor(img, coor)


def change_coor(img, coor):
    if coor[1] + settings.HEIGHT + settings.SPACE_HEIGHT >= img.im.size[1]:
            coor[0] += settings.WIDTH + settings.SPACE_WIDTH
            coor[1] = settings.START_POSITION[1]
    else:
        coor[1] += settings.SPACE_HEIGHT + settings.HEIGHT


def start_or_end(img, coor, text):
    img.ellipse([(coor[0], coor[1]), (coor[0] + settings.WIDTH, coor[1] + settings.HEIGHT)], outline=(0,0,0), fill=(255,255,255), width=3)
    text_size = settings.FONT.getsize(text)
    img.text([(coor[0] + settings.WIDTH/2 - text_size[0]/2), (coor[1] + settings.HEIGHT/2 - text_size[1]/2) - 10], text, font=settings.FONT, fill=(0,0,0), align="center")
    return img

def draw_block(img, coor, body):
    img.polygon(
                [
                    (coor[0], coor[1]), 
                    (coor[0] + settings.WIDTH, coor[1]), 
                    (coor[0] + settings.WIDTH, coor[1] + settings.HEIGHT),
                    (coor[0], coor[1] + settings.HEIGHT)
                ],
                fill=(255, 255,255),
                )
    img.line(
                [
                    (coor[0], coor[1]), 
                    (coor[0] + settings.WIDTH, coor[1]), 
                    (coor[0] + settings.WIDTH, coor[1] + settings.HEIGHT),
                    (coor[0], coor[1] + settings.HEIGHT),
                    (coor[0], coor[1])
                ],
                fill=(0, 0, 0),
                width=3
            )
    text_size = settings.FONT.getsize(body)
    img.text([(coor[0] + settings.WIDTH/2 - text_size[0]/2), (coor[1] + settings.HEIGHT/2 - text_size[1]/2) - 10], body, font=settings.FONT, fill=(0,0,0), align="center")
    return img

def draw_io(img, coor, body):
    img.polygon(
                [
                    (coor[0] + settings.WIDTH * 0.2 , coor[1]), 
                    (coor[0] + settings.WIDTH, coor[1]), 
                    (coor[0] + settings.WIDTH * 0.8, coor[1] + settings.HEIGHT),
                    (coor[0], coor[1] + settings.HEIGHT)
                ],
                fill=(255, 255,255),
                )
    img.line(
                [
                    (coor[0] + settings.WIDTH * 0.2 , coor[1]), 
                    (coor[0] + settings.WIDTH, coor[1]), 
                    (coor[0] + settings.WIDTH * 0.8, coor[1] + settings.HEIGHT),
                    (coor[0], coor[1] + settings.HEIGHT),
                    (coor[0] + settings.WIDTH * 0.2 , coor[1])
                ],
                fill=(0, 0, 0),
                width=3
            )
    text_size = settings.FONT.getsize(body)
    img.text([(coor[0] + settings.WIDTH/2 - text_size[0]/2), (coor[1] + settings.HEIGHT/2 - text_size[1]/2) - 10], body, font=settings.FONT, fill=(0,0,0), align="center")
    return img

def draw_if(img, coor, body):
    img.polygon(
                [
                    ((coor[0] + settings.WIDTH/2), coor[1]),
                    (coor[0], (coor[1] + settings.HEIGHT/2)),
                    ((coor[0] + settings.WIDTH/2), coor[1] + settings.HEIGHT),
                    (coor[0] + settings.WIDTH, (coor[1] + settings.HEIGHT/2))

                ],
                fill=(255, 255,255),
                )
    img.line(
                [
                    ((coor[0] + settings.WIDTH/2), coor[1]),
                    (coor[0], (coor[1] + settings.HEIGHT/2)),
                    ((coor[0] + settings.WIDTH/2), coor[1] + settings.HEIGHT),
                    (coor[0] + settings.WIDTH, (coor[1] + settings.HEIGHT/2)),
                    ((coor[0] + settings.WIDTH/2), coor[1])
                ],
                fill=(0, 0, 0),
                width=3
            )
    text_size = settings.FONT.getsize(body)
    img.text([(coor[0] + settings.WIDTH/2 - text_size[0]/2), (coor[1] + settings.HEIGHT/2 - text_size[1]/2) - 10], body, font=settings.FONT, fill=(0,0,0), align="center")
    return img

def draw_else(img, coor):
    pass

def draw_cycle(img, coor, body):
    img.polygon(
                [
                    (coor[0] + settings.WIDTH/4, coor[1]),
                    (coor[0], coor[1] + settings.HEIGHT),
                    (coor[0] + settings.WIDTH, coor[1] + settings.HEIGHT),
                    (coor[0] + settings.WIDTH * 0.75, coor[1])
                ],
                fill=(255, 255,255)
            )
    img.line(
            [
                (coor[0] + settings.WIDTH/4, coor[1]),
                (coor[0], coor[1] + settings.HEIGHT),
                (coor[0] + settings.WIDTH, coor[1] + settings.HEIGHT),
                (coor[0] + settings.WIDTH * 0.75, coor[1]),
                (coor[0] + settings.WIDTH/4, coor[1])
            ],
                fill=(0, 0, 0),
                width=3
            )
    text_size = settings.FONT.getsize(body)
    img.text([(coor[0] + settings.WIDTH/2 - text_size[0]/2), (coor[1] + settings.HEIGHT/2 - text_size[1]/2) - 10], body, font=settings.FONT, fill=(0,0,0), align="center")
    return img

def draw_end_cycle(img, coor):
    img.polygon(
                [
                    (coor[0], coor[1]),
                    (coor[0] + settings.WIDTH/4, coor[1] + settings.HEIGHT),
                    (coor[0] + settings.WIDTH * 0.75, coor[1] + settings.HEIGHT),
                    (coor[0] + settings.WIDTH, coor[1])
                ],
                fill=(255, 255,255)
            )
    img.line(
            [
                (coor[0], coor[1]),
                (coor[0] + settings.WIDTH/4, coor[1] + settings.HEIGHT),
                (coor[0] + settings.WIDTH * 0.75, coor[1] + settings.HEIGHT),
                (coor[0] + settings.WIDTH, coor[1]),
                (coor[0], coor[1])
            ],
                fill=(0, 0, 0),
                width=3
            )

def draw_func_or_class(img, x, y, body):
    pass

def connection(img, _coor, img_size=None, block_if=False, count=0):


    if block_if:
        connection(img, _coor, img_size)
        coor = _coor.copy()
        last_coor = _coor.copy()
        for _ in range(count + 1):
            change_coor(img, last_coor)


        last_coor[1] += settings.HEIGHT / 2
        if coor[0] == last_coor[0]:
            last_coor[0] += settings.WIDTH
        
        coor[0] += settings.WIDTH
        coor[1] += settings.HEIGHT / 2


        #TODO connections for every option separately(in this column, in next column (up row), in next column(down row) and in column + 2 and more up/down (5 options)

        if last_coor[1] == coor[1] and last_coor[0] == coor[0] + settings.SPACE_WIDTH:
            img.line(
                        [
                            (coor[0], coor[1]),
                            (last_coor[0] + settings.WIDTH / 2, last_coor[1])
                        ],

                        fill=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                        width=settings.CONNECTION_WIDTH
                    )
        elif coor[0] == last_coor[0]:
            img.line(
                        [
                            (coor[0], coor[1]),
                            (coor[0] + settings.SPACE_WIDTH / 3, coor[1]),
                            (coor[0] + settings.SPACE_WIDTH / 3, last_coor[1]),
                            (coor[0] - settings.WIDTH / 2, last_coor[1]),                            
                        ],

                        fill=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                        width=settings.CONNECTION_WIDTH
                    )
        elif last_coor[1] > coor[1]:
            img.line(
                        [
                            (coor[0], coor[1]),
                            (coor[0] + settings.SPACE_WIDTH / 3, coor[1]),
                            (coor[0] + settings.SPACE_WIDTH / 3, last_coor[1] - settings.HEIGHT / 2 - settings.SPACE_HEIGHT / 2),
                            (last_coor[0] - settings.SPACE_WIDTH * 2 / 3, last_coor[1] - settings.HEIGHT / 2 - settings.SPACE_HEIGHT / 2),
                            (last_coor[0] - settings.SPACE_WIDTH * 2 / 3, last_coor[1]),
                            (last_coor[0] + settings.WIDTH / 2, last_coor[1]),
                        ],

                        fill=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                        width=settings.CONNECTION_WIDTH
                    )
        else:
            img.line(
                        [
                            (coor[0], coor[1]),
                            (coor[0] + settings.SPACE_WIDTH / 3, coor[1]),
                            (coor[0] + settings.SPACE_WIDTH / 3, last_coor[1] + settings.HEIGHT / 2 + settings.SPACE_HEIGHT / 2),
                            (last_coor[0] - settings.SPACE_WIDTH * 2 / 3, last_coor[1] + settings.HEIGHT / 2 + settings.SPACE_HEIGHT / 2),
                            (last_coor[0] - settings.SPACE_WIDTH * 2 / 3, last_coor[1]),
                            (last_coor[0] + settings.WIDTH / 2, last_coor[1]),
                        ],

                        fill=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                        width=settings.CONNECTION_WIDTH
                    )


        return

    coor = [_coor[0] + settings.WIDTH / 2, _coor[1] + settings.HEIGHT]

    if img_size != None and coor[1] >= img_size[1] - settings.SPACE_HEIGHT:
        img.line(
                [
                    (coor[0], coor[1]),
                    (coor[0], coor[1] + settings.SPACE_HEIGHT/2),
                    (coor[0] + settings.WIDTH/2 + settings.SPACE_WIDTH * 2 / 3, coor[1] + settings.SPACE_HEIGHT/2),
                    (coor[0] + settings.WIDTH/2 + settings.SPACE_WIDTH * 2 / 3, settings.HEIGHT/2),
                    (coor[0] + settings.WIDTH/2 + settings.SPACE_WIDTH + settings.WIDTH/2, settings.HEIGHT/2)
                ],
                fill=settings.CONNECTION_COLOR,
                width=settings.CONNECTION_WIDTH 
                )
    else:

        img.line(
                [
                    (coor[0], coor[1]),
                    (coor[0], coor[1] + settings.SPACE_HEIGHT)
                ],
                fill=settings.CONNECTION_COLOR,
                width=settings.CONNECTION_WIDTH 
                )


def block_count(_el_list, res = 0):
    el_list = _el_list.copy()
    if type(el_list) == list:
        while el_list != []:
            el = el_list.pop()
            if type(el) != list:
                if el != 'else' and el.strip() != 'else:':
                    res += 1

                if el == 'if':
                    res -= 1
                if 'for ' in el or 'while ' in el:
                    res += 1
            else:
                res = block_count(el, res)
    return res
