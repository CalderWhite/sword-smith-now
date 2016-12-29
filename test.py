import GMK, json
x = GMK.items.util.grab_relic_names(print_status=True)
j = json.dumps(x,indent=4)
w = open("x.json",'w')
w.write(j)
w.close()