from bsdraw import create_func_list_python, file_to_list, change_coor
import settings
from PIL import Image, ImageDraw

def connections(img, _coor, _slist):
    coor = _coor.copy()
    slist = _slist.copy()
    while slist != []:
        el = slist.pop(0)
        connection(img, coor)
        change_coor(img, coor)


def connection(img, _coor):
    coor = [_coor[0] + settings.WIDTH / 2, _coor[1] + settings.HEIGHT]
    if coor[1] >= img.im.size[1] - settings.SPACE_HEIGHT:
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

def draw_connections(img, coor, dlist):
    smpl_list = simple_list(dlist)
    connections(img, coor, smpl_list)

def simple_list(_dlist, res=[]):
    dlist = _dlist.copy()
    while dlist != []:
        el = dlist.pop(0)
        if type(el) != list:
            res.append(el)
        else:
            simple_list(el, res)
    return res



path = 'test.py'

size = 5
end_size = [size * (settings.WIDTH + settings.SPACE_WIDTH), size * (settings.HEIGHT + settings.SPACE_HEIGHT)]
img = Image.new('RGB', end_size, settings.BACKGROUND_COLOR)
draw = ImageDraw.Draw(img)
coor = settings.START_POSITION.copy()

dlist = create_func_list_python(file_to_list(path))

draw_connections(draw, coor.copy(), dlist)

img.save('ex.png')



