import requests
from lib.network import WLAN
import pygame
import math



class hardware(object):

    backend_url = ""
    backend_port = 0
    buttons = []
    testtimer = 0
    network = None
    mode = None
    config = {}
    screen = None

    def __init__(self, connect):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 400))

        self.buttons = [False, False, False]
        self.connect = connect

    def update(self):
        self.screen.fill((0,0,0))
        self.getbuttons()
        blaat = self.connect.update_hardware(self.buttons)
        self.putonscreen(blaat)




    def makebutton(self, ev, buttonindex, offsetx=0, offsety=0):
        rect = pygame.Rect(offsetx,  offsety, 100, 80)
        for event in ev:
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                self.buttons[buttonindex] = False
            elif event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(pos):
                self.buttons[buttonindex] = True


        pygame.draw.ellipse(self.screen, (200, 0, 200), rect)



    def drawachar(self, char, offsetx=0, offsety=0):
        chars = {
          'A':0x0033333f33331e0c,
          'B':0x003f66663e66663f,
          'C':0x003c66030303663c,
          'D':0x001f36666666361f,
          'E':0x007f46161e16467f,
          'F':0x000f06161e16467f,
          'G':0x007c66730303663c,
          'H':0x003333333f333333,
          'I':0x001e0c0c0c0c0c1e,
          'J':0x001e333330303078,
          'K':0x006766361e366667,
          'L':0x007f66460606060f,
          'M':0x0063636b7f7f7763,
          'N':0x006363737b6f6763,
          'O':0x001c36636363361c,
          'P':0x000f06063e66663f,
          'Q':0x00381e3b3333331e,
          'R':0x006766363e66663f,
          'S':0x001e33380e07331e,
          'T':0x001e0c0c0c0c2d3f,
          'U':0x003f333333333333,
          'V':0x000c1e3333333333,
          'W':0x0063777f6b636363,
          'X':0x0063361c1c366363,
          'Y':0x001e0c0c1e333333,
          'Z':0x007f664c1831637f,
          ' ':0x0000000000000000,
          'a':0x006e333e301e0000,
          'b':0x003b66663e060607,
          'c':0x001e3303331e0000,
          'd':0x006e33333e303038,
          'e':0x001e033f331e0000,
          'f':0x000f06060f06361c,
          'g':0x1f303e33336e0000,
          'h':0x006766666e360607,
          'i':0x001e0c0c0c0e000c,
          'j':0x1e33333030300030,
          'k':0x0067361e36660607,
          'l':0x001e0c0c0c0c0c0e,
          'm':0x00636b7f7f330000,
          'n':0x00333333331f0000,
          'o':0x001e3333331e0000,
          'p':0x0f063e66663b0000,
          'q':0x78303e33336e0000,
          'r':0x000f06666e3b0000,
          's':0x001f301e033e0000,
          't':0x00182c0c0c3e0c08,
          'u':0x006e333333330000,
          'v':0x000c1e3333330000,
          'w':0x00367f7f6b630000,
          'x':0x0063361c36630000,
          'y':0x1f303e3333330000,
          'z':0x003f260c193f0000
        }

        index = 0
        row = 0
        col = 0

        if char in chars:
            binar = bin(chars[char])

            while index < len(binar):

                if binar[index] == '1':
                    pygame.draw.ellipse(self.screen, (80, 0, 0), ((8-col)*12+offsetx, (8-row)*12 + offsety, 10, 10))


                col = index % 8
                row = math.floor(index/8)
                index += 1


    def getbuttons(self):
        self.buttons = [False, False, False]

        ev = pygame.event.get()

        self.makebutton(ev, 0, offsety=200)
        self.makebutton(ev, 1, offsetx=100, offsety=200)
        self.makebutton(ev, 2, offsetx=200, offsety=200)

    def putonscreen(self, text):
        if text and len(text) > 0:
            self.drawachar(text[0])
            self.drawachar(text[1], 100)
            self.drawachar(text[2], 200)
            self.drawachar(text[3], 300)

            pygame.display.update()

    def change_if(self, net_if=None):
        if net_if is not None:
            self.network = WLAN(net_if)
            self.mode = net_if
