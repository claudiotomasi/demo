#TO DO mergeduplicated code
def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v))
        for k, v in dictionary.items())

def convert(data):
    if isinstance(data, basestring):
        return data.encode('utf-8')
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data
#END TO DO
def adjacents():
    adjacent_list = {
        'q' : ['q', 'w', 'a', 'Q', 'W', 'A'],
        'Q' : ['q', 'w', 'a', 'Q', 'W', 'A'],
        'w' : ['w', 'q', 'a', 's', 'd', 'W', 'Q', 'A', 'S', 'D'],
        'W' : ['w', 'q', 'a', 's', 'd', 'W', 'Q', 'A', 'S', 'D'],
        'e' : ['e','w','r','s','d','f', 'E', 'W','R','S','D','F'],
        'E' : ['e','w','r','s','d','f', 'E', 'W','R','S','D','F'],
        'r' : ['r','e','t','d','f','g', 'R','E','T','D','F','G'],
        'R' : ['r','e','t','d','f','g', 'R','E','T','D','F','G'],
        't' : ['t','r','y','f','g','h','T','R','Y','F','G','H'],
        'T' : ['t','r','y','f','g','h','T','R','Y','F','G','H'],
        'y' : ['y','t','u','g','h','j', 'Y','T','U','G','H','J'],
        'Y' : ['y','t','u','g','h','j', 'Y','T','U','G','H','J'],
        'u' : ['u','y','i','h','j','k','U','Y','I','H','J','K'],
        'U' : ['u','y','i','h','j','k','U','Y','I','H','J','K'],
        'i' : ['i','u','o','j','k','l','I','U','O','J','K','L'],
        'I' : ['i','u','o','j','k','l','I','U','O','J','K','L'],
        'o' : ['o','i','p','k','l', 'O','I','P','K','L'],
        'O' : ['o','i','p','k','l', 'O','I','P','K','L'],
        'p' : ['p','o','l', 'P', 'O', 'L'],
        'P' : ['p','o','l', 'P', 'O', 'L'],
        'a' : ['a','q','s','w','z', 'A','Q','S','W','Z'],
        'A' : ['a','q','s','w','z', 'A','Q','S','W','Z'],
        's' : ['s','a','d','w','x','q','e','z', 'S','A','D','W','X','Q','E','Z'],
        'S' : ['s','a','d','w','x','q','e','z', 'S','A','D','W','X','Q','E','Z'],
        'd' : ['d','s','f','e','c','x','r','D','S','F','E','C','X','R'],
        'D' : ['d','s','f','e','c','x','r','D','S','F','E','C','X','R'],
        'f' : ['f','d','g','r','c','v','t','F','D','G','R','C','V','T'],
        'F' : ['f','d','g','r','c','v','t','F','D','G','R','C','V','T'],
        'g' : ['g','f','h','t','v','b','y','G','F','H','T','V','B','Y'],
        'G' : ['g','f','h','t','v','b','y','G','F','H','T','V','B','Y'],
        'h' : ['h','g','j','y','b','n','u', 'H','G','J','Y','B','N','U'],
        'H' : ['h','g','j','y','b','n','u', 'H','G','J','Y','B','N','U'],
        'j' : ['j','h','k','u','n','m','i', 'J','H','K','U','N','M','I'],
        'J' : ['j','h','k','u','n','m','i', 'J','H','K','U','N','M','I'],
        'k' : ['k','j','l','m','i','o','K','J','L','M','O'],
        'K' : ['k','j','l','m','i','o','K','J','L','M','O'],
        'l' : ['l','k','o','p', 'L','K','O','P'],
        'L' : ['l','k','o','p', 'L','K','O','P'],
        'z' : ['z','x','a','s','Z','X','A','S'],
        'Z' : ['z','x','a','s','Z','X','A','S'],
        'x' : ['x','z','c','s','d','X','Z','C','S','D'],
        'X' : ['x','z','c','s','d','X','Z','C','S','D',' '],
        'c' : ['c','x','v','d','f','C','X','V','D','F',' '],
        'C' : ['c','x','v','d','f','C','X','V','D','F',' '],
        'v' : ['v','c','b','f','g','V','C','B','F','G',' '],
        'V' : ['v','c','b','f','g','V','C','B','F','G',' '],
        'b' : ['b','v','n','g','h','B','V','N','G','H',' '],
        'B' : ['b','v','n','g','h','B','V','N','G','H',' '],
        'n' : ['n','b','m','h','j','N','B','M','H','J',' '],
        'N' : ['n','b','m','h','j','N','B','M','H','J',' '],
        'm' : ['m','n','j','k','M','N','J','K',' '],
        'M' : ['m','n','j','k','M','N','J','K',' '],
        ' ' : [' ', 'c', 'v', 'b', 'n', 'C', 'V', 'B', 'N'],
        '.' : ['.',' ']
            }
    return adjacent_list
