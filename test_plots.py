from extract import get_plot_coordinates as g

codes = {"district": "146", "tehsil": "00766", "village": "124649"}

for p in ["1", "2", "5"]:
    c = g("a", "b", "c", p, True, codes)
    print("PLOT", p, "src=", g.last_meta.get("source"))
    print("  first", c[0])
    print("  third", c[2])
    print("---")