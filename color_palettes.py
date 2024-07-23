# color_palettes.py

# Grey palette
GREY = {
    50: '#F6F5F5',
    100: '#ECEDF2',
    200: '#D5D6E2',
    300: '#B1B5C8',
    400: '#868CAA',
    500: '#676E90',
    600: '#525777',
    700: '#434661',
    800: '#3A3D52',
    900: '#252632'
}

# Primary Purple palette
PRIMARY_PURPLE = {
    50: '#EFEFF7',
    100: '#CCCEE6',
    200: '#B4B6D9',
    300: '#9294C8',
    400: '#7D80BD',
    500: '#5C60AD',
    600: '#54579D',
    700: '#41447B',
    800: '#33355F',
    900: '#272849'
}

# Neon Green palette
NEON_GREEN = {
    50: '#FBFDE9',
    100: '#F3F8BB',
    200: '#EEF49B',
    300: '#E6F06D',
    400: '#E1ED51',
    500: '#D9E825',
    600: '#C5D322',
    700: '#9AA51A',
    800: '#778014',
    900: '#5B6110'
}

# Define color combinations for different chart types
USER_GROWTH_COLORS = [PRIMARY_PURPLE[100], PRIMARY_PURPLE[300], PRIMARY_PURPLE[500], PRIMARY_PURPLE[700], PRIMARY_PURPLE[900]]
REVENUE_GROWTH_COLORS = [NEON_GREEN[400], PRIMARY_PURPLE[500], GREY[600], PRIMARY_PURPLE[700], NEON_GREEN[800]]
REVENUE_BREAKDOWN_COLORS = [PRIMARY_PURPLE[300], GREY[400], NEON_GREEN[500]]