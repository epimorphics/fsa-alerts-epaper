import Image
import ImageDraw
import ImageFont

def reconstruct_text_array(text_array):
    out_text = [' '.join(line) for line in text_array]
    return '\n'.join(out_text)

# checks that the next line of text doesn't overrun bounds
def next_line_height_check(font, text_array, y_height):
    image = Image.new('1', (1000, y_height))
    draw = ImageDraw.Draw(image)
    text_array = text_array + ["test line"]
    text = reconstruct_text_array(text_array)
    (x, y) = draw.multiline_textsize(text, font)
    if y > y_height:
        return False
    return True

# returns (line in boundary, overrunning text)
def fill_draw_line(font, word_array, minx, maxx):
    image = Image.new('1', (maxx-minx, 300))
    draw = ImageDraw.Draw(image)
    for index, word in enumerate(word_array):
      tmp_text = ' '.join(word_array[:index+1])
      (x, y) = draw.multiline_textsize(tmp_text, font)
      if x > (maxx - minx):
          return (word_array[:index], word_array[index:])
    return (word_array, [])

# adds newlines or truncates text such that it fits into defined area
def fill_draw_area(font, text, minx, maxx, miny, maxy):
    out_text = text.split('\n')
    remaining = out_text.pop().split(' ')
    while len(remaining) > 0:
        (line, remaining) = fill_draw_line(font, remaining, minx, maxx)
        out_text = out_text + [line]
        # If the more text is left and the next line will overrun the boundaried, add elipses
        if len(remaining) > 0 and next_line_height_check(font, out_text, maxy - miny) == False:
            out_text[-1][-1] = "..."
            return reconstruct_text_array(out_text)
    return reconstruct_text_array(out_text)

# alternates points between red and black buffers to create a shaded rectangle
def draw_shaded_rectange(red, black, minx, miny, maxx, maxy):
    redpoints = []
    blackpoints = []
    for j in range(miny, maxy):
        if (j % 2 == 1):
            redpoints = redpoints + [(x, j) for x in range(minx, maxx, 2)]
            blackpoints = blackpoints + [(x, j) for x in range(minx+1, maxx, 2)]
        else:
            redpoints = redpoints + [(x, j) for x in range(minx+1, maxx, 2)]
            blackpoints = blackpoints + [(x, j) for x in range(minx, maxx, 2)]
    red.point(redpoints, fill=0)
    red.point(blackpoints, fill=255)
    black.point(blackpoints, fill=0)
    black.point(redpoints, fill=255)

