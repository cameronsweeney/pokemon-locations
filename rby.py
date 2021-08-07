global current_version
global rom
import yaml, re, bs4, copy
from natdex import natdex_names

###########################################################
### source: https://bulbapedia.bulbagarden.net/wiki/    ###
### List_of_Pok%C3%A9mon_by_index_number_(Generation_I) ###
###########################################################

pkmn_indices = {
    1: 'Rhydon',
    2: 'Kangaskhan',
    3: 'Nidoran M',
    4: 'Clefairy',
    5: 'Spearow',
    6: 'Voltorb',
    7: 'Nidoking',
    8: 'Slowbro',
    9: 'Ivysaur',
    10: 'Exeggutor',
    11: 'Lickitung',
    12: 'Exeggcute',
    13: 'Grimer',
    14: 'Gengar',
    15: 'Nidoran F',
    16: 'Nidoqueen',
    17: 'Cubone',
    18: 'Rhyhorn',
    19: 'Lapras',
    20: 'Arcanine',
    21: 'Mew',
    22: 'Gyarados',
    23: 'Shellder',
    24: 'Tentacool',
    25: 'Gastly',
    26: 'Scyther',
    27: 'Staryu',
    28: 'Blastoise',
    29: 'Pinsir',
    30: 'Tangela',
    33: 'Growlithe',
    34: 'Onix',
    35: 'Fearow',    
    36: 'Pidgey',
    37: 'Slowpoke',
    38: 'Kadabra',
    39: 'Graveler',
    40: 'Chansey',
    41: 'Machoke',
    42: 'Mr. Mime',
    43: 'Hitmonlee',
    44: 'Hitmonchan',
    45: 'Arbok',
    46: 'Parasect',
    47: 'Psyduck',
    48: 'Drowzee',
    49: 'Golem',
    51: 'Magmar',
    53: 'Electabuzz',
    54: 'Magneton',
    55: 'Koffing',
    57: 'Mankey',
    58: 'Seel',
    59: 'Diglett',
    60: 'Tauros',
    64: "Farfetch'd",
    65: 'Venonat',
    66: 'Dragonite',
    70: 'Doduo',
    71: 'Poliwag',
    72: 'Jynx',
    73: 'Moltres',
    74: 'Articuno',
    75: 'Zapdos',
    76: 'Ditto',
    77: 'Meowth',
    78: 'Krabby',
    82: 'Vulpix',
    83: 'Ninetales',
    84: 'Pikachu',
    85: 'Raichu',
    88: 'Dratini',
    89: 'Dragonair',
    90: 'Kabuto',
    91: 'Kabutops',
    92: 'Horsea',
    93: 'Seadra',
    96: 'Sandshrew',
    97: 'Sandslash',
    98: 'Omanyte',
    99: 'Omastar',
    100: 'Jigglypuff',
    101: 'Wigglytuff',
    102: 'Eevee',
    103: 'Flareon',
    104: 'Jolteon',
    105: 'Vaporeon',
    106: 'Machop',
    107: 'Zubat',
    108: 'Ekans',
    109: 'Paras',
    110: 'Poliwhirl',
    111: 'Poliwrath',
    112: 'Weedle',
    113: 'Kakuna',
    114: 'Beedrill',
    116: 'Dodrio',
    117: 'Primeape',
    118: 'Dugtrio',
    119: 'Venomoth',
    120: 'Dewgong',
    123: 'Caterpie',
    124: 'Metapod',
    125: 'Butterfree',
    126: 'Machamp',
    128: 'Golduck',
    129: 'Hypno',
    130: 'Golbat',
    131: 'Mewtwo',
    132: 'Snorlax',
    133: 'Magikarp',
    136: 'Muk',
    138: 'Kingler',
    139: 'Cloyster',
    141: 'Electrode',
    142: 'Clefable',
    143: 'Weezing',
    144: 'Persian',
    145: 'Marowak',
    147: 'Haunter',
    148: 'Abra',
    149: 'Alakazam',
    150: 'Pidgeotto',
    151: 'Pidgeot',
    152: 'Starmie',
    153: 'Bulbasaur',
    154: 'Venusaur',
    155: 'Tentacruel',
    157: 'Goldeen',
    158: 'Seaking',
    163: 'Ponyta',
    164: 'Rapidash',
    165: 'Rattata',
    166: 'Raticate',
    167: 'Nidorino',
    168: 'Nidorina',
    169: 'Geodude',
    170: 'Porygon',
    171: 'Aerodactyl',
    173: 'Magnemite',
    176: 'Charmander',
    177: 'Squirtle',
    178: 'Charmeleon',
    179: 'Wartortle',
    180: 'Charizard',
    185: 'Oddish',
    186: 'Gloom',
    187: 'Vileplume',
    188: 'Bellsprout',
    189: 'Weepinbell',
    190: 'Victreebel'
}

################################################################################
###  source: https://github.com/pret/pokemon-reverse-engineering-tools/blob/ ###
###  5e0715f2579adcfeb683448c9a7826cfd3afa57d/redtools/extract_maps.py#L27   ###
################################################################################

map_names = {
         0x00: "Pallet Town",
         0x01: "Viridian City",
         0x02: "Pewter City",
         0x03: "Cerulean City",
         0x04: "Lavender Town",
         0x05: "Vermilion City",
         0x06: "Celadon City",
         0x07: "Fuchsia City",
         0x08: "Cinnabar Island",
         0x09: "Indigo Plateau",
         0x0A: "Saffron City",
        #0x0B: "FREEZE",
         0x0C: "Route 1",
         0x0D: "Route 2",
         0x0E: "Route 3",
         0x0F: "Route 4",
         0x10: "Route 5",
         0x11: "Route 6",
         0x12: "Route 7",
         0x13: "Route 8",
         0x14: "Route 9",
         0x15: "Route 10",
         0x16: "Route 11",
         0x17: "Route 12",
         0x18: "Route 13",
         0x19: "Route 14",
         0x1A: "Route 15",
         0x1B: "Route 16",
         0x1C: "Route 17",
         0x1D: "Route 18",
         0x1E: "Route 19",
         0x1F: "Route 20",
         0x20: "Route 21",
         0x21: "Route 22",
         0x22: "Route 23",
         0x23: "Route 24",
         0x24: "Route 25",
         0x25: "Pallet Red's House 1F",
         0x26: "Pallet Red's House 2F",
         0x27: "Pallet Blue's House",
         0x28: "Pallet Professor Oak's Laboratory",
         0x29: "Viridian Pokémon Center",
         0x2A: "Viridian Poké Mart",
         0x2B: "Viridian Trainers' School",
         0x2C: "Viridian House",
         0x2D: "Viridian Gym",
         0x2E: "Route 2 Diglett's Cave Entrance",
         0x2F: "Viridian Forest North Gate",
         0x30: "Route 2 House",
         0x31: "Route 2 Gate",
         0x32: "Viridian Forest South Gate",
         0x33: "Viridian Forest",
         0x34: "Pewter Museum 1F",
         0x35: "Pewter Museum 2F",
         0x36: "Pewter Gym",
         0x37: "Pewter House NE",
         0x38: "Pewter Poké Mart",
         0x39: "Pewter House SW",
         0x3A: "Pewter Pokémon Center",
         0x3B: "Mt. Moon 1F",
         0x3C: "Mt. Moon B1",
         0x3D: "Mt. Moon B2",
         0x3E: "Cerulean House (Trashed)",
         0x3F: "Cerulean House (Trade)",
         0x40: "Cerulean Pokémon Center",
         0x41: "Cerulean Gym",
         0x42: "Cerulean Bike Shop",
         0x43: "Cerulean Poké Mart",
         0x44: "Mt. Moon Pokémon Center",
        #0x45: "COPY OF: Cerulean House (Trashed)",
         0x46: "Route 5 Gate",
         0x47: "Route 5 Underground Path Entrance",
         0x48: "Route 5 Day Care",
         0x49: "Route 6 Gate",
         0x4A: "Route 6 Underground Path Entrance",
        #0x4B: "COPY OF: Route 6 Underground Tunnel Entrance",
         0x4C: "Route 7 Gate",
         0x4D: "Route 7 Underground Path Entrance",
        #0x4E: "COPY OF: Underground Path Entrance (Route 7)",
         0x4F: "Route 8 Gate",
         0x50: "Route 8 Underground Path Entrance",
         0x51: "Rock Tunnel Pokémon Center",
         0x52: "Rock Tunnel 1F",
         0x53: "Power Plant",
         0x54: "Route 11 Gate 1F",
         0x55: "Route 11 Diglett's Cave Entrance",
         0x56: "Route 11 Gate 2F",
         0x57: "Route 12 Gate 1F",
         0x58: "Route 25 Bill's House",
         0x59: "Vermilion Pokémon Center",
         0x5A: "Vermilion Pokémon Fan Club",
         0x5B: "Vermilion Poké Mart",
         0x5C: "Vermilion Gym",
         0x5D: "Vermilion House SE",
         0x5E: "Vermilion Dock",
         0x5F: "S.S. Anne 1F Corridor",
         0x60: "S.S. Anne 2F Corridor",
         0x61: "S.S. Anne Corridor to Deck",
         0x62: "S.S. Anne B1 Corridor",
         0x63: "S.S. Anne Deck",
         0x64: "S.S. Anne Kitchen",
         0x65: "S.S. Anne Captain's Room",
         0x66: "S.S. Anne 1F Rooms",
         0x67: "S.S. Anne 2F Rooms",
         0x68: "S.S. Anne B1 Rooms",
        #0x69: "FREEZE",
        #0x6A: "FREEZE",
        #0x6B: "FREEZE",
         0x6C: "Victory Road 1F",
        #0x6D: "FREEZE",
        #0x6E: "FREEZE",
        #0x6F: "FREEZE",
        #0x70: "FREEZE",
         0x71: "Indigo Plateau Lance's Room",
        #0x72: "FREEZE",
        #0x73: "FREEZE",
        #0x74: "FREEZE",
        #0x75: "FREEZE",
         0x76: "Indigo Plateau Hall of Fame Room",
         0x77: "Underground Path (N/S)",
         0x78: "Indigo Plateau Champion's Room",
         0x79: "Underground Path (W/E)",
         0x7A: "Celadon Department Store 1F",
         0x7B: "Celadon Department Store 2F",
         0x7C: "Celadon Department Store 3F",
         0x7D: "Celadon Department Store 4F",
         0x7E: "Celadon Department Store Roof",
         0x7F: "Celadon Department Store Elevator",
         0x80: "Celadon Mansion 1F",
         0x81: "Celadon Mansion 2F",
         0x82: "Celadon Mansion 3F",
         0x83: "Celadon Mansion Rooftop",
         0x84: "Celadon Mansion Rooftop Room",
         0x85: "Celadon Pokémon Center",
         0x86: "Celadon Gym",
         0x87: "Celadon Game Corner",
         0x88: "Celadon Department Store 5F",
         0x89: "Celadon Game Corner Prize Exchange",
         0x8A: "Celadon Diner",
         0x8B: "Celadon House",
         0x8C: "Celadon Hotel",
         0x8D: "Lavender Pokémon Center",
         0x8E: "Pokémon Tower 1F",
         0x8F: "Pokémon Tower 2F",
         0x90: "Pokémon Tower 3F",
         0x91: "Pokémon Tower 4F",
         0x92: "Pokémon Tower 5F",
         0x93: "Pokémon Tower 6F",
         0x94: "Pokémon Tower 7F",
         0x95: "Lavender Mr. Fuji's House",
         0x96: "Lavender Poké Mart",
         0x97: "Lavender House SW",
         0x98: "Fuchsia Poké Mart",
         0x99: "Fuchsia House SW",
         0x9A: "Fuchsia Pokémon Center",
         0x9B: "Fuchsia Warden's House",
         0x9C: "Safari Zone Entrance",
         0x9D: "Fuchsia Gym",
         0x9E: "Safari Zone Meeting Room",
         0x9F: "Seafoam Islands B1",
         0xA0: "Seafoam Islands B2",
         0xA1: "Seafoam Islands B3",
         0xA2: "Seafoam Islands B4",
         0xA3: "Vermilion Fishing Guru's House",
         0xA4: "Fuchsia Fishing Guru's Older Brother's House",
         0xA5: "Pokémon Mansion 1F",
         0xA6: "Cinnabar Gym",
         0xA7: "Cinnabar Pokémon Lab Entrance",
         0xA8: "Cinnabar Pokémon Lab Meeting Room",
         0xA9: "Cinnabar Pokémon Lab R&D Room",
         0xAA: "Cinnabar Pokémon Lab Testing Room",
         0xAB: "Cinnabar Pokémon Center",
         0xAC: "Cinnabar Poké Mart",
        #0xAD: "COPY: Cinnabar Mart",
         0xAE: "Indigo Plateau Lobby",
         0xAF: "Saffron Copycat's House 1F",
         0xB0: "Saffron Copycat's House 2F",
         0xB1: "Saffron Fighting Dojo",
         0xB2: "Saffron Gym",
         0xB3: "Saffron House NW",
         0xB4: "Saffron Poké Mart",
         0xB5: "Silph Co 1F",
         0xB6: "Saffron Pokémon Center",
         0xB7: "Saffron Mr. Psychic's House",
         0xB8: "Route 15 Gate 1F",
         0xB9: "Route 15 Gate 2F",
         0xBA: "Route 16 Gate 1F",
         0xBB: "Route 16 Gate 2F",
         0xBC: "Route 16 House",
         0xBD: "Route 12 House",
         0xBE: "Route 18 Gate 1F",
         0xBF: "Route 18 Gate 2F",
         0xC0: "Seafoam Islands 1F",
         0xC1: "Route 22 Gate",
         0xC2: "Victory Road 2F",
         0xC3: "Route 12 Gate 2F",
         0xC4: "Vermilion House (Trade)",
         0xC5: "Diglett's Cave",
         0xC6: "Victory Road 3F",
         0xC7: "Rocket Hideout B1",
         0xC8: "Rocket Hideout B2",
         0xC9: "Rocket Hideout B3",
         0xCA: "Rocket Hideout B4",
         0xCB: "Rocket Hideout Elevator",
        #0xCC: "FREEZE",
        #0xCD: "FREEZE",
        #0xCE: "FREEZE",
         0xCF: "Silph Co. 2F",
         0xD0: "Silph Co. 3F",
         0xD1: "Silph Co. 4F",
         0xD2: "Silph Co. 5F",
         0xD3: "Silph Co. 6F",
         0xD4: "Silph Co. 7F",
         0xD5: "Silph Co. 8F",
         0xD6: "Pokémon Mansion 2F",
         0xD7: "Pokémon Mansion 3F",
         0xD8: "Pokémon Mansion 4F",
         0xD9: "Safari Zone East",
         0xDA: "Safari Zone North",
         0xDB: "Safari Zone West",
         0xDC: "Safari Zone Center",
         0xDD: "Safari Zone Center Rest House",
         0xDE: "Safari Zone Secret House",
         0xDF: "Safari Zone West Rest House",
         0xE0: "Safari Zone East Rest House",
         0xE1: "Safari Zone North Rest House",
         0xE2: "Cerulean Cave 2F",
         0xE3: "Cerulean Cave B1",
         0xE4: "Cerulean Cave 1F",
         0xE5: "Lavender Name Rater's House",
         0xE6: "Cerulean House (Badges)",
        #0xE7: "FREEZE",
         0xE8: "Rock Tunnel B1",
         0xE9: "Silph Co. 9F",
         0xEA: "Silph Co. 10F",
         0xEB: "Silph Co. 11F",
         0xEC: "Silph Co. Elevator",
        #0xED: "FREEZE",
        #0xEE: "FREEZE",
         0xEF: "Battle Center",
         0xF0: "Trade Center",
        #0xF1: "FREEZE",
        #0xF2: "FREEZE",
        #0xF3: "FREEZE",
        #0xF4: "FREEZE",
         0xF5: "Indigo Plateau Lorelei's Room",
         0xF6: "Indigo Plateau Bruno's Room",
         0xF7: "Indigo Plateau Agatha's Room"
       }

#################################################################
### source for fishing group data: https://aww.moe/u408xw.asm ###
### SuperRodData: ; e919 (3:6919)                             ###
#################################################################

rb_fish_groups_by_map = {
    0x00: 1, # Pallet Town
    0x01: 1, # Viridian City
    0x03: 3, # Cerulean City
    0x05: 4, # Vermilion City
    0x06: 5, # Celadon City
    0x07: 10, # Fuchsia City
    0x08: 8, # Cinnabar Island
    0x0F: 3, # Route 4
    0x11: 4, # Route 6
    0x15: 5, # Route 10
    0x16: 4, # Route 11
    0x17: 7, # Route 12
    0x18: 7, # Route 13
    0x1C: 7, # Route 17
    0x1D: 7, # Route 18
    0x1E: 8, # Route 19
    0x1F: 8, # Route 20
    0x20: 8, # Route 21
    0x21: 2, # Route 22
    0x22: 9, # Route 23
    0x23: 3, # Route 24
    0x24: 3, # Route 25
    0x41: 3, # Cerulean Gym
    0x5E: 4, # Vermilion Dock
    0xA1: 8, # Seafoam Islands B3
    0xA2: 8, # Seafoam Islands B4
    0xD9: 6, # Safari Zone East
    0xDA: 6, # Safari Zone North
    0xDB: 6, # Safari Zone West
    0xDC: 6, # Safari Zone Center
#   0xE2: 9, # Cerulean Cave 2F - no water to fish in here!
    0xE3: 9, # Cerulean Cave B1
    0xE4: 9 # Cerulean Cave 1F
}


########################################################
### source for following pointer addresses:          ###
### https://github.com/pokemon-speedrunning/symfiles ###
########################################################

# these addresses are the first byte of the game's map header pointer table
# that is, the start of the list of pointers to each map header, ordered by map index
# At 0x1AE and 0x1AF, you'll find the pointer (2 bytes, little endian) to the map header for map 1
# At 0x1B0 and 0x1B1, you'll find the pointer (2 bytes, little endian) to the map header for map 2, etc.
map_header_pointers = {
    'red': 0x01AE,
    'blue': 0x01AE,
    'yellow': 0xFC1F2    
}

# these addresses are the first byte of the games map header bank table
# At byte 0xC23D, you'll find the number of the bank where map 1's map header is stored
# combine with pointer above to get the full address of a map's map header
map_header_bank_pointers = {
    'red': 0xC23D,
    'blue': 0xC23D,
    'yellow': 0xFC3E4
}

# table separate from map headers
# the t to wild encounter data table
wild_data_pointers = {
    'red': 0xCEEB,
    'blue': 0xCEEB,
    'yellow': 0xCB95
}


#########################################################################

grass_map_indices = [
    0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13,
    0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B,
    0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x22, 0x23,
    0x24, # Routes 1 to 25
    
    0xD9, 0xDA, 0xDB, 0xDC # Safari Zone maps
]

indoor_map_indices = [
    0x53, # Power Plant
    0x8E, 0x8F, 0x90, 0x91, 0x92, 0x93, 0x94, # Pokémon Tower 1F-7F
    0xA5, 0xD6, 0xD7, 0xD8, # Pokémon Mansion 1F-4F
]

# cave map indices for human reference
""" 0x3B: "Mt. Moon 1F",
    0x3C: "Mt. Moon B1",
    0x3D: "Mt. Moon B2",
    0x52: "Rock Tunnel 1F",
    0x6C: "Victory Road 1F",
    0x9F: "Seafoam Islands B1",
    0xA0: "Seafoam Islands B2",
    0xA1: "Seafoam Islands B3",
    0xA2: "Seafoam Islands B4",
    0xC0: "Seafoam Islands 1F",
    0xC2: "Victory Road 2F",
    0xC5: "Diglett's Cave",
    0xC6: "Victory Road 3F",
    0xE2: "Cerulean Cave 2F",
    0xE3: "Cerulean Cave B1",
    0xE4: "Cerulean Cave 1F",
    0xE8: "Rock Tunnel B1",
"""

def grass_or_cave(map_id):
    # pass a map id to this function and it will return a string describing the type of land encounter
    # In Gen I there's outside grass encounters, caves with wild Pokémon, and a few indoor locations
    if map_id in grass_map_indices:
        return 'tall grass'
    elif map_id in indoor_map_indices:
        return 'indoors'
    else:
        return 'cave'


#########################################################################

class wild_pkmn(yaml.YAMLObject):
    yaml_tag = '!wild'
    yaml_loader = yaml.SafeLoader # THIS LINE IS VERY IMPORTANT!
    def __init__(self, name, level):
        self.name = str(name)
        self.level = int(level)
    
    # makes it pretty to print these in Python
    def __repr__(self):
        return "%s Lv.%s" % (self.name, self.level)
    
    @classmethod # this fixed that horrible horrible error (with SafeLoader.add_constructor() below)
    def from_yaml(cls, loader, node):
        nodename, nodelevel = node.value.split(' Lv.')
        return wild_pkmn(nodename, nodelevel)
# end class declaration wild_pkmn

pattern = re.compile(r'([\w\d\-.\' ]+) Lv.(\d+)')
yaml.SafeLoader.add_implicit_resolver('!wild', pattern, first=None)
yaml.SafeDumper.add_implicit_resolver('!wild', pattern, first=None)

yaml.SafeLoader.add_constructor('!wild', wild_pkmn.from_yaml)
    
# makes wild_pkmn objects pretty in YAML, when dumping
def wild_pkmn_representer(dumper, data):
    return dumper.represent_scalar('!wild', "%s Lv.%s" % (data.name, data.level))
yaml.SafeDumper.add_representer(wild_pkmn, wild_pkmn_representer)



####################################################################################
####################################################################################
### It was easier to hand-type the YAML from sources I found than write code     ###
### that rips and converts the binary data from each ROM.                        ###
### The YAML depends on the wild_pkmn def and constructors/representers and must ###
### be loaded AFTER those defs/decls                                             ###
####################################################################################
### source: https://aww.moe/u408xw.asm                                           ###
### starting at FishingGroup1: ; e97d (3:697d), 47 bytes                         ###
### ; number of monsters, followed by level/monster pairs                        ###
####################################################################################
### That's from a disassembly of Red, but Blue has the same fishing encounters   ###
### https://sites.google.com/site/pokemonslots/gen-i/blue-green?authuser=0       ###
### That source has a minor error; Bulbapedia has the correct data w/o slot info ###
### in fact it has the same offset for the start of the fishing groups: 0xE97D   ###
####################################################################################

rb_super_rod_data_by_group = yaml.safe_load("""- [] # fish group 0 means no water to fish in
- [Tentacool Lv.15, Poliwag Lv.15] # Fish Group 1; this list is one-indexed
- [Goldeen Lv.15, Poliwag Lv.15]
- [Psyduck Lv.15, Goldeen Lv.15, Krabby Lv.15]
- [Krabby Lv.15, Shellder Lv.15]
- [Poliwhirl Lv.23, Slowpoke Lv.15]
- [Dratini Lv.15, Krabby Lv.15, Psyduck Lv.15, Slowpoke Lv.15]
- [Tentacool Lv.5, Krabby Lv.15, Goldeen Lv.15, Magikarp Lv.15]
- [Staryu Lv.15, Horsea Lv.15, Shellder Lv.15, Goldeen Lv.15]
- [Slowbro Lv.23, Seaking Lv.23, Kingler Lv.23, Seadra Lv.23]
- [Seaking Lv.23, Krabby Lv.15, Goldeen Lv.15, Magikarp Lv.15]
""")

######################################################################################
### source: https://github.com/pret/pokeyellow/blob/master/data/wild/super_rod.asm ###
######################################################################################

y_super_rod_data_by_map = yaml.safe_load("""---
0x00: [Staryu Lv.10, Tentacool Lv.10, Staryu Lv.5, Tentacool Lv.20]       # Pallet Town
0x01: [Poliwag Lv.5, Poliwag Lv.10, Poliwag Lv.15, Poliwag Lv.10]         # Viridian City
0x03: [Goldeen Lv.25, Goldeen Lv.30, Seaking Lv.30, Seaking Lv.40]        # Cerulean City
0x05: [Tentacool Lv.15, Tentacool Lv.20, Tentacool Lv.10, Horsea Lv.5]    # Vermilion City
0x06: [Goldeen Lv.5, Goldeen Lv.10, Goldeen Lv.15, Goldeen Lv.20]         # Celadon City
0x07: [Magikarp Lv.5, Magikarp Lv.10, Magikarp Lv.15, Gyarados Lv.15]     # Fuchsia City
0x08: [Staryu Lv.15, Tentacool Lv.15, Staryu Lv.10, Tentacool Lv.30]      # Cinnabar Island
0x0F: [Goldeen Lv.20, Goldeen Lv.25, Goldeen Lv.30, Seaking Lv.30]        # Route 4
0x11: [Goldeen Lv.5, Goldeen Lv.10, Goldeen Lv.15, Goldeen Lv.20]         # Route 6
0x15: [Krabby Lv.15, Krabby Lv.20, Horsea Lv.10, Kingler Lv.25]           # Route 10
0x16: [Tentacool Lv.15, Tentacool Lv.20, Shellder Lv.25, Shellder Lv.35]  # Route 11
0x17: [Horsea Lv.20, Horsea Lv.25, Seadra Lv.25, Seadra Lv.35]            # Route 12
0x18: [Horsea Lv.15, Horsea Lv.20, Seadra Lv.25, Seadra Lv.25]            # Route 13
0x1C: [Tentacool Lv.5, Tentacool Lv.15, Shellder Lv.25, Shellder Lv.35]   # Route 17
0x1D: [Tentacool Lv.15, Shellder Lv.20, Shellder Lv.30, Shellder Lv.40]   # Route 18
0x1E: [Tentacool Lv.15, Staryu Lv.20, Tentacool Lv.30, Tentacruel Lv.30]  # Route 19
0x1F: [Tentacool Lv.20, Tentacruel Lv.20, Staryu Lv.30, Tentacruel Lv.30] # Route 20
0x20: [Tentacool Lv.15, Staryu Lv.20, Tentacool Lv.30, Tentacruel Lv.30]  # Route 21
0x21: [Poliwag Lv.5, Poliwag Lv.10, Poliwag Lv.15, Poliwhirl Lv.15]       # Route 22
0x22: [Poliwag Lv.25, Poliwag Lv.30, Poliwhril Lv.30, Poliwhirl Lv.40]    # Route 23
0x23: [Goldeen Lv.20, Goldeen Lv.25, Goldeen Lv.30, Seaking Lv.30]        # Route 24
0x24: [Krabby Lv.10, Krabby Lv.15, Kingler Lv.15, Kingler Lv.25]          # Route 25
0x41: [Goldeen Lv.25, Goldeen Lv.30, Seaking Lv.30, Seaking Lv.40]        # Cerulean Gym
0x5E: [Tentacool Lv.10, Tentacool Lv.15, Staryu Lv.15, Shellder Lv.10]    # Vermilion Dock
0xA1: [Krabby Lv.25, Staryu Lv.20, Kingler Lv.35, Staryu Lv.40]           # Seafoam Islands B3
0xA2: [Krabby Lv.25, Staryu Lv.20, Kingler Lv.35, Staryu Lv.40]           # Seaforam Islands B4
0xD9: [Magikarp Lv.5, Magikarp Lv.10, Magikarp Lv.15, Dratini Lv.15]      # Safari Zone East
0xDA: [Magikarp Lv.5, Magikarp Lv.10, Magikarp Lv.15, Dratini Lv.15]      # Safari Zone North
0xDB: [Magikarp Lv.5, Magikarp Lv.10, Magikarp Lv.15, Dratini Lv.15]      # Safari Zone West
0xDC: [Magikarp Lv.5, Magikarp Lv.10, Dratini Lv.10, Dragonair Lv.15]     # Safari Zone Center
0xE3: [Goldeen Lv.30, Seaking Lv.40, Seaking Lv.50, Seaking Lv.60]        # Cerulean Cave B1
0xE4: [Goldeen Lv.25, Seaking Lv.35, Seaking Lv.45, Seaking Lv.55]        # Cerulean Cave 1F

""")

#####################################################################################################


slot_percentages = [20, 20, 15, 10, 10, 10, 5, 5, 4, 1]

class _map(yaml.YAMLObject):
    yaml_tag = '!rby_map'
    yaml_loader = yaml.SafeLoader # THIS LINE IS VERY IMPORTANT!
    yaml_dumper = yaml.SafeDumper
    
    def __init__(self, map_num, current_version, **kwargs):
        self._map_num = map_num
        if not kwargs:
            other_attrs = construct_map_from_id(map_num, current_version)
        else:
            other_attrs = kwargs
            
        self._map_name = other_attrs['map_name']
        self._version = other_attrs['version']
        self.pointer_map_header = other_attrs['pointer_map_header']
        self.pointer_wild_data = other_attrs['pointer_wild_data']
        self.rate_land = other_attrs['rate_land']
        self.pkmn_land = other_attrs['pkmn_land']
        self.rate_surf = other_attrs['rate_surf']
        self.pkmn_surf = other_attrs['pkmn_surf']
        self.fish_group = other_attrs['fish_group']
        if other_attrs['fish_group']:
            self.pkmn_fish_old = other_attrs['pkmn_fish_old']
            self.pkmn_fish_good = other_attrs['pkmn_fish_good']
            self.pkmn_fish_super = other_attrs['pkmn_fish_super']
    
# end class declaration rby._map
    
    
def parse_rby_wild_data(raw_bytes):
    # raw_bytes is a sequence of 20 bytes (ints 0 <= x < 256) straight from the ROM
    # reads the 10 slots of wild Pokémon names+levels and returns a list of wild_pkmn objects
    # I accidentally deleted this function a few minutes ago so this is my second try
    wild_pkmn_list = []
    for current_pkmn in range(0, 10):
        pkmn_level = raw_bytes[2*current_pkmn]
        pkmn_index = raw_bytes[2*current_pkmn+1]
        pkmn_name = pkmn_indices[pkmn_index]
        wild_pkmn_list.append(wild_pkmn(pkmn_name, pkmn_level))
    return wild_pkmn_list
    
# end def parse_rby_wild_data(raw_bytes)
    
def construct_map_from_id(map_id, current_version):
    map_as_dict = {
        'map_name': map_names[map_id],
        'version': current_version
    }
    
    # open file
    rom_file = open("Pokemon %s.gb" % current_version.capitalize(), 'rb')
    rom = rom_file.read()
    rom_file.close()
    
    # calculate where to find this map's header pointer and bank info
    pointer_address = map_header_pointers[current_version] + (map_id * 2)
    bank_pointer_address = map_header_bank_pointers[current_version] + map_id
    # fetch pointer and bank, convert to big endian
    pointer_value = rom[pointer_address] + (rom[pointer_address+1] * 0x100)
    bank_value = rom[bank_pointer_address] + (rom[bank_pointer_address+1] * 0x100)
    # calculate pointer for map header
    map_as_dict['pointer_map_header'] = pointer_value - 0x4000 + (bank_value * 0x4000)
    
    # calculate where to find this map's pointer to its wild Pokémon data
    wild_pointer_address = wild_data_pointers[current_version] + (map_id * 2)
    # convert to big endian
    wild_pointer_value = rom[wild_pointer_address] + (rom[wild_pointer_address+1] * 0x100)        
    map_as_dict['pointer_wild_data'] = wild_pointer_value + 0x8000 # all wild encounter data is in bank 3
    
    # now we finally have the right address for Python!    
    # check for land data
    map_as_dict['rate_land'] = rom[map_as_dict['pointer_wild_data']]
    if map_as_dict['rate_land'] != 0:
        # land data found
        land_bytes = rom[map_as_dict['pointer_wild_data'] + 1:map_as_dict['pointer_wild_data'] + 21]
        map_as_dict['pkmn_land'] = parse_rby_wild_data(land_bytes)
        water_offset = 21
    else:
        map_as_dict['pkmn_land'] = []
        water_offset = 1
        
    #check for water data
    map_as_dict['rate_surf'] = rom[map_as_dict['pointer_wild_data'] + water_offset]
    if map_as_dict['rate_surf'] != 0:
        # water data found
        water_bytes = rom[map_as_dict['pointer_wild_data'] + water_offset + 1:map_as_dict['pointer_wild_data'] + water_offset + 21]
        map_as_dict['pkmn_surf'] = parse_rby_wild_data(water_bytes)
    else:
        # no water data found
        map_as_dict['pkmn_surf'] = []
    
    # set default fish_group to 0
    map_as_dict['fish_group'] = 0
    
    # time for fishing data - works one way in RB and another in Y
    # however, the same maps are fishable
    # I can check RB fish data for all 3 versions to see if the map is fishable
    if map_id in rb_fish_groups_by_map:
        # Let's do Old Rod and Good Rod before I forget
        ###############################################################################
        ### source: https://sites.google.com/site/pokemonslots/gen-i/red?authuser=0 ###
        ###############################################################################
        map_as_dict['pkmn_fish_old'] = [wild_pkmn('Magikarp', 5)]
        map_as_dict['pkmn_fish_good'] = [wild_pkmn('Goldeen', 10), wild_pkmn('Poliwag', 10)]
        # look up fishing group (for RB, but I wanna have it there for all maps I create - anticipating a versions merge)
        # also there will be a variable assignment error in rby_map.__init__() if I only do it for RB maps
        map_as_dict['fish_group'] = rb_fish_groups_by_map[map_id]
        if current_version == 'yellow':
            map_as_dict['pkmn_fish_super'] = y_super_rod_data_by_map[map_id]
        else: # Red or Blue version; need to look up fishing group for the map
            map_as_dict['pkmn_fish_super'] = copy.deepcopy(rb_super_rod_data_by_group[map_as_dict['fish_group']])

    return map_as_dict
# end def construct_map_from_id(map_id)
# Phew!
