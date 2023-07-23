from __future__ import annotations
import re
from functools import singledispatch

import xmltodict as x2d
import MeCab


@singledispatch
def get_txt_by_snt(snt: str) -> str:
    return snt

@get_txt_by_snt.register
def _(snt: list) -> str:
    txts = (p["#text"] for p in snt)
    return "\n".join(txts)
    
    

@singledispatch
def get_txt_by_ps(ps: dict) -> str:
    if "Sentence" in ps:
        return get_txt_by_snt(ps["Sentence"])
    raise Exception("invalid paragraph-sentence")

@get_txt_by_ps.register
def _(ps: list) -> str:
    txts = (get_txt_by_snt(s) for s in ps)
    return "\n".join(txts)    

@singledispatch
def get_txt_by_para(para: dict) -> str:
    if "ParagraphSentence" in para:
        return get_txt_by_ps(para["ParagraphSentence"])

    print(para)
    raise Exception("invalid paragraph")

@get_txt_by_para.register
def _(para: list) -> str:
    txts = (get_txt_by_para(p) for p in para)
    return "\n".join(txts)
    
def get_txt_by_art(art:dict) -> str:
    if "Paragraph" not in art:
        raise Exception("invalid article")
    return get_txt_by_para(art["Paragraph"])

word_type_wl=["名詞", "動詞"]
def count_words(txt: str) -> dict:    
    cnt = {}
    tagger = MeCab.Tagger()
    node = tagger.parseToNode(txt)
    while node:
        word = node.surface
        tp = node.feature.split(",")[0]
        if not tp in word_type_wl:
            node = node.next
            continue
        if not word in cnt:
            cnt[word] = 0
        cnt[word] += 1
        node = node.next
        
    cnt = sorted(cnt.items(), key=lambda x:x[1], reverse=True)
    return cnt


def main():
    FNAME = "./xml/321CONSTITUTION_19470503_000000000000000/321CONSTITUTION_19470503_000000000000000.xml"
    with open(FNAME) as fd:
        txt = fd.read()

    article_pattern = r"<Article\b[^>]*>.*?</Article>"
    article_matches = re.findall(article_pattern, txt, re.DOTALL)

    # Print the matched content inside the <div> tags
    d = {}
    for match in article_matches:
        art = x2d.parse(match)["Article"]
        title = art["ArticleTitle"]
        art_txt = get_txt_by_art(art)
        d[title] = count_words(art_txt)
        # input(match)
    print(d)
        


"""use xmltodict
doc = x2d.parse()
body = doc["Law"]["LawBody"]
print(body["LawTitle"]["#text"])

# Preamble data
for p in body["Preamble"]["Paragraph"]:
    #print(p["@Num"])
    #print(p["ParagraphSentence"]["Sentence"])
    pass


# Main article data
for chapter in body["MainProvision"]["Chapter"]:
    print(chapter["ChapterTitle"])
    for article in chapter["Article"]:
        print(article)
        print(article["ArticleTitle"])
        print(article["Paragraph"])
        print(get_txt_from_paragraph(article["Paragraph"]))
"""

if __name__ == "__main__":
    main()