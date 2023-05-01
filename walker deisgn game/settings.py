

level_0 = {

    'terrain':'map/levels/level0__player.csv',
    'player':'map/levels/level0__terrain.csv',


}
level_map = [
'                                          ',
'                                          ',
'                                          ',
'       xx                      xx         ',
'                 xx                       ',
'x                     xx         xx       ',
'    xx                   xx         xx    ',
' xx          P        xx         xx       ',
'   xx      xxxxxx             xx         x',
'xx            xxxxx       xx    xx xxxxx  ',
'xxxxxxxxx xxxxxxxx   xxxxxxxxxxxx   xxxxxx'
]
tilesize = 64
screen_width = 1200
# screen_height = 800
screen_height = len(level_map) * tilesize