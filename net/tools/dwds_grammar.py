"""
分析一个单词的语法
<span class="dwdswb-ft-blocktext"><span>Substantiv
(Maskulinum)</span> · Genitiv Singular: <b>Hund(e)s</b> ·
Nominativ Plural: <b>Hunde</b></span>
"""
def grammar_noun(soup):
    noun = dict()
    content = ""
    noun["type"] = "noun"
    html_text = soup.text
    noun["article"] = ""

    if "(Maskulinum)" in html_text:
        noun["article"] = "der"
        content += "m; "
    elif "(Neutrum)" in html_text:
        noun["article"] = "das"
        content += "n; "
    elif "(Femininum)" in html_text:
        noun["article"] = "die"
        content += "f; "

    sp = soup.find_all("b")
    if "Genitiv Singular:" in html_text:
        noun["genitiv"] = sp[0].text
        content += "genitiv: " + noun["genitiv"] + "; "
    if "Nominativ Plural:" in html_text:
        noun["plural"] = sp[1].text
        content += "pl: " + noun["plural"] + " "
    else:
        noun["plural"] = "nur Sg"
        content += noun["plural"] + " "

    return noun, content

def grammar_verb(soup):
    verb = dict()
    verb["type"] = "verb"
    present = soup.find("span", title = "3. Person Singular Indikativ Präsens Aktiv")
    verb["present"] = present.text
    past_tense = soup.find("span", title="3. Person Singular Indikativ Präteritum Aktiv")
    verb["past_tense"] = past_tense.text

    sp_hilfsverbs = soup.find_all("span", title = "Hilfsverb bei der 3. Person Indikativ Perfekt Aktiv")
    hilfsverbs = ""
    for sp_hv in sp_hilfsverbs:
        #hv = sp_hv.text
        hilfsverbs += sp_hv.text + "/"
    hilfsverbs = hilfsverbs[0:-1]

    participle_2 = soup.find("span", title="Partizip II")
    verb["participle 2"] = hilfsverbs + " " + participle_2.text

    content = "{0}, {1}, {2}".format(verb["present"], verb["present"], verb["participle 2"])
    return verb, content


# Adjektiv · Komparativ: roter/röter · Superlativ: am rotesten/am rötesten
# Adjektiv · indeklinabel
# Adjektiv
# Adjektiv · prädikativ, adverbiell · Komparativ: höher · Superlativ: am höchsten
def grammar_adjektiv(soup):
    adj = dict()
    adj["type"] = "adj"
    items = soup.text.split(" · ")
    content = ""
    for item in items:
        if "Komparativ: " in item:
            adj["comparative"] = item.replace("Komparativ: ", "")
            content += adj["comparative"] + "; "
        if "Superlativ: " in item:
            adj["superlative"] = item.replace("Superlativ: ", "")
            content += adj["superlative"]
        if "indeklinabel" in item:
            adj["indeclinable"] = True
        else:
            adj["indeclinable"] = False

    # print(soup.text)
    return adj, content