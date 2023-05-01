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
level_0 = {
    'terrain' : 'map/levels/level0__terrain.csv',
    'coins' : 'map/levels/level0__coins.csv',
    'crates' : 'map/levels/level0__crates.csv',
    'player' : 'map/levels/level0__player.csv',
    'enemy' : 'map/levels/level0__enemy.csv',
    'grass' : 'map/levels/level0__grass.csv',
    'palms' : 'map/levels/level0__palms.csv',
    'enemy_constraints' : 'map/levels/level0__enemy_restraints.csv',
    'bg_palms' : 'map/levels/level0__bg_palms.csv'
     








}

tile_size = 64
screen_width = 1200
# height is basically our level map size it tile_size and that is 11*64 = 704
screen_height = 800
# screen_height = len(level_map) * tile_size
# print(len(level_map))
