from __future__ import annotations
import re
from functools import singledispatch, reduce

import xmltodict as x2d
import MeCab
from neo4j import GraphDatabase, basic_auth

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
        
    return cnt

def make_cypher_query(tx, d: dict) -> None:
    tx.run("CREATE (n:Test)")
    # for art in d:
    #     query = "CREATE (n:Article)"
    #     # input(query)
    #     tx.run(query, name=art)
    # terms = list(set(reduce(lambda a,b: a+list(b.keys()), d.values(), [])))
    # for term in terms:
    #     query = "CREATE (n:Term)" 
    #     # input(term)
    #     tx.run(query, name=term)
    # for art, cnt in d.items():
    #     for term in cnt.keys():
    #         query = f"MATCH(a:Article),(t:Term) WHERE a.name = '{art}' AND t.name = '{term}' CREATE (a)-[r:USES]->(t)"
    #         # input(query)
    #         tx.run(query)
    
            
        
        
    
    

def main():
    FNAME = "./xml/321CONSTITUTION_19470503_000000000000000/321CONSTITUTION_19470503_000000000000000.xml"
    with open(FNAME,encoding="utf-8") as fd:
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

    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password'))
    print(driver)
    driver.execute_query("CREATE (n:Test)")
    # with driver.session() as session:
    #     input(routing_)
    #     session.execute_write(make_cypher_query,d)
    
    
        


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