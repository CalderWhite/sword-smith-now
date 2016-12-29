from PIL import Image
import math, json,requests, random
from bs4 import BeautifulSoup as b
from tqdm import tqdm
class util(object):
    """This is not meant to be constructed. Just use the class's objects"""
    def grab_mineral_index(print_status):
        if print_status:
            print("[GET]ing wiki page...")
        res = requests.request("GET","https://en.wikipedia.org/wiki/List_of_minerals")
        s = b(res.text,"html.parser")
        x = s.findAll("div", { "class" : "div-col columns column-width" })
        # we need to go through each tag, since there is trash beside some of the link tags
        if print_status:
            print("Scraping and indexing...")
        # lazy to the max VVV
        index = {
            "a" : [],
            "b" : [],
            "c" : [],
            "d" : [],
            "e" : [],
            "f" : [],
            "g" : [],
            "h" : [],
            "i" : [],
            "j" : [],
            "k" : [],
            "l" : [],
            "m" : [],
            "n" : [],
            "o" : [],
            "p" : [],
            "q" : [],
            "r" : [],
            "s" : [],
            "t" : [],
            "u" : [],
            "v" : [],
            "w" : [],
            "x" : [],
            "y" : [],
            "z" : [],
        }
        for tag in x:
            for child in tag.findChildren():
                try:
                    y = child.findChildren()[0].text
                    index[y[0].lower()].append(y)
                except IndexError:
                    #print("Skipped! : [%s]" % child.text)
                    pass
                except KeyError:
                    if print_status:
                        print("Skipped! : [%s] (Is a valid name but won't appear in the index)" % child.text)
        return index
    def generate_colors(divisor,only_green=False,img_map=False,print_status=True):
        """NOTE: the number of colors generated will be: [(divisor + 1) ^ 3] and the divisor cannot be zero for OBVIOUS REASONS."""
        if print_status:
            print("Crunching the numbers...")
        diff = math.floor(255 / divisor)
        a = []
        # add one, since we are including zero in the possible numbers
        for i in range(divisor + 1):
            a.append( (i) * diff)
        if print_status:
            print("Creating combos...")
        # go through all combos. Simple stuff.
        combos = []
        for i in a:
            for j in a:
                for k in a:
                    combos.append((int(i),int(j),int(k)))
        if print_status:
            print("Sorting combos...")
        # sorts them so the list is darkest color to lightest
        sortedCombos = []
        x = []
        for i in combos:
            x.append({"index" : combos.index(i), "sum" : (i[0] + i[1] + i[2])})
        x = sorted(x,key=lambda k:k["sum"])
        # inserts them in a new list
        for i in x:
            sortedCombos.append(combos[i["index"]])
        # options
        if img_map:
            # returns all the colors, darkest to lightest in an image
            img = Image.new("RGB",( (divisor + 1) ** 3,1),(255,255,255))
            if only_green:
                # returns only colors where the G value is the greatest
                z = []
                for i in sortedCombos:
                    if i[1] > i[0] and i[1] > i[2]:
                        z.append(i)
                #returns image, going darkest to lightest
                if print_status:
                    print("Writing combos to image...")
                for combo in z:
                    #print((combos.index(combo),0),combo)
                    img.putpixel((z.index(combo),0),combo)
            else:
                if print_status:
                    print("Writing combos to image...")
                for combo in sortedCombos:
                    img.putpixel((sortedCombos.index(combo),0),combo)
            return img
        else:
            if only_green:
                # returns only colors where the G value is the greatest
                z = []
                for i in sortedCombos:
                    if i[1] > i[0] and i[1] > i[2]:
                        z.append(i)
                return z
            else:
                return sortedCombos
    def grab_relic_pages(print_status=False,progress_bar=True):
        if print_status:
            print("[GET]ing wiki page...")
        res = requests.request("GET","https://en.wikipedia.org/wiki/List_of_mythological_objects")
        s = b(res.text,"html.parser")
        x = s.find("div",{"id" : "mw-content-text"})
        z = x.findAll("b")
        # take out the trash
        for i in range(12):
            z.pop(len(z) - 1)
        z.pop(0)
        z.pop(0)
        """
        # for now we're going to generate a giant dict.
        j = {
            "index" : []
        }
        for i in z:
            j["index"].append(i.text)
        j = json.dumps(j, indent=4)
        return j
        """
        index = []
        for i in z:
            index.append(i.text)
        deleted = []
        newIndex = {}
        # All illegal words must be in lower case
        illegal_words = ["weapon"," tree "]
        illegal_names = ["sword","spear"]
        if progress_bar:
            pbar = tqdm(total=len(index))
        for i in index:
            pbar.set_description("Index is %s long" % len(newIndex))
            page = requests.request("GET","https://en.wikipedia.org/wiki/" + str(i))
            if page.status_code == 200:
                ns = b(page.text,"html.parser")
                bad = False
                for wrd in illegal_words:
                    if ns.text.lower().find(wrd) >= 0:
                        deleted.append(i)
                        bad = True
                        if print_status:
                            try:
                                print("[%s] contains the illegal word [%s]" % (index.index(i),wrd))
                            except:
                                print("HIT ERROR PRINTING ITEM NUMBER [%s]" % (str(index.index(i))))
                        break
                if bad == False:
                    newIndex[i] = page.text
            else:
                if print_status:
                    try:
                        print("GOT [%s] for item [%s]." % (page.status_code,index.index(i)))
                    except:
                        print("HIT ERROR PRINTING ITEM NUMBER [%s]" % (str(index.index(i))))
                deleted.append(i)
            if progress_bar:
                pbar.update(1)
        return newIndex
    def generate_relic_buffs(d,print_status=False):
        # just for testing purposes:
        index = json.loads(open("x.json",'r').read())
class mineral_constructor(object):
    def __init__(self,color,name):
        self.color = color
        self.name = name
def generate_minerals(divisor=3,print_status=False):
    color_index = util.generate_colors(divisor,print_status=print_status)
    name_index = util.grab_mineral_index(print_status=print_status)
    minerals = []
    for color in color_index:
        # firstly, delete empty lists
        pops = []
        for i in name_index:
            if len(name_index[i]) == 0:
                pops.append(i)
        for i in pops:
            name_index.pop(i)
        # now generate the first letter of the name
        # The index is seperated by first letter so we get the most equal amount of first letters.
        # If it were just a large list and there were way more A's than other letters, there is a greater chance each name will start with A.
        # However, if we go by picking randomly from any first letter, we achive an equal chance.
        first_letter = list(name_index)[random.randrange(0,len(name_index))]
        nn = len(name_index[first_letter])
        p = random.randrange(0,nn)
        name = name_index[first_letter][p]
        # remove name from index so we have no reoccurances
        name_index[first_letter].pop(p)
        mineral = mineral_constructor(color,name)
        minerals.append(mineral)
    return minerals
def build_minerals(divisor=3,format="JSON",print_status=False):
    index = generate_minerals(divisor=divisor,print_status=print_status)
    formats = ["JSON"]
    if format == "JSON":
        ni = {
            "all" : {}
        }
        for m in index:
            ni["all"][m.name] = m.__dict__
        j = json.dumps(ni, indent=4)
        return j
    else:
        raise Exception("Got [%s] format. Accepted formats : %s" % (format,str(formats)))