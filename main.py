import epd4in2b
import Image
import ImageFont
import ImageDraw
import fsa
import epdHelpers
import time

COLORED = 0
UNCOLORED = 255 
HASHTAG_X = 10
HASHTAG_Y = 145 
ALERT_TYPE_X = 15
ALERT_TYPE_Y = 20
SLEEP_TIME = 60 * 15 #15 minutes
title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)
fsa_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
alert_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20) 

def draw_background(draw_black, draw_red):
    draw_red.rectangle((0, 0, 400, 140), fill = COLORED)
    epdHelpers.draw_shaded_rectange(draw_red, draw_black, 0, 140, 400, 300)
    draw_red.rectangle((10, 170, 390, 280), fill = COLORED)
    draw_black.rectangle((10, 170, 390, 280), fill = UNCOLORED)
    draw_red.text((210, ALERT_TYPE_Y), "Food\nStandards\nAgency", font=fsa_font, fill=UNCOLORED, align="right")
    draw_black.text((210, ALERT_TYPE_Y), "Food\nStandards\nAgency", font=fsa_font, fill=UNCOLORED, align="right")

def draw_alert_type(draw_black, draw_red, alert):
    alerttype = fsa.get_alert_type(alert)
    if alerttype == fsa.AlertType.PRIN:
        draw_red.multiline_text((ALERT_TYPE_X, ALERT_TYPE_Y), 'Product\nRecall', font = title_font, fill = UNCOLORED, align="left")
	draw_red.text((HASHTAG_X, HASHTAG_Y), '#FoodAlert', font = fsa_font, fill = UNCOLORED)
        draw_black.text((HASHTAG_X, HASHTAG_Y), '#FoodAlert', font = fsa_font, fill = UNCOLORED)
    elif alerttype == fsa.AlertType.AA:
        draw_red.multiline_text((ALERT_TYPE_X, ALERT_TYPE_Y), 'Allergy\nAlert', font = fsa_font, fill = UNCOLORED, align="left")
        draw_red.text((HASHTAG_X, HASHTAG_Y), '#FoodAllergy', font = alert_font, fill = UNCOLORED)
        draw_black.text((HASHTAG_X, HASHTAG_Y), '#FoodAllergy', font = alert_font, fill = UNCOLORED)
    else:
        draw_red.multiline_text((ALERT_TYPE_X, ALERT_TYPE_Y), 'Alert', font = fsa_font, fill = UNCOLORED, align="left")
        draw_red.text((HASHTAG_X, HASHTAG_Y), '#FoodAlert', font = alert_font, fill = UNCOLORED)
        draw_black.text((HASHTAG_X, HASHTAG_Y), '#FoodAlert', font = alert_font, fill = UNCOLORED)

def draw_text_area(draw_black, draw_red, alert):
    text = epdHelpers.fill_draw_area(alert_font, "latest alert: " + alert['shortURL'] + " " + alert['title'], 30, 370, 175, 280)
    draw_black.text((170, HASHTAG_Y), alert['modified'][0:19], font = alert_font, fill = UNCOLORED)
    draw_red.text((170, HASHTAG_Y), alert['modified'][0:19], font = alert_font, fill = UNCOLORED)
    draw_black.text((30, 175), text, font = alert_font, fill = UNCOLORED)
    draw_red.text((30, 175), text, font = alert_font, fill = UNCOLORED)

def main():
    oldalert = {'@id': ''}
    while True:
        alert = fsa.get_latest_alert()
        if alert['@id'] != oldalert['@id']:
            print("new alert")
            oldalert = alert
            alerttype = fsa.get_alert_type(alert)
            epd = epd4in2b.EPD()
            epd.init()
            # For simplicity, the arguments are explicit numerical coordinates
            image_red = Image.new('1', (epd4in2b.EPD_WIDTH, epd4in2b.EPD_HEIGHT), UNCOLORED)    # 255: clear the frame
            draw_red = ImageDraw.Draw(image_red)
            image_black = Image.new('1', (epd4in2b.EPD_WIDTH, epd4in2b.EPD_HEIGHT), UNCOLORED)    # 255: clear the frame
            draw_black = ImageDraw.Draw(image_black)

            draw_background(draw_black, draw_red)
            draw_alert_type(draw_black, draw_red, alert)
            draw_text_area(draw_black, draw_red, alert)
            # display the frames
            epd.display_frame(epd.get_frame_buffer(image_black), epd.get_frame_buffer(image_red))
            # sleep for 15 minutes and check for new alerts
            time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
