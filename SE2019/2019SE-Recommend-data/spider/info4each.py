import requests, pickle, time
from bs4 import BeautifulSoup
from bs4 import Tag

# rare = pickle.load(open('1800-tx.pk', 'rb'))
# front = pickle.load(open('1800.pk', 'rb'))
# final = dict(front, **rare)
# pickle.dump(final, open('finaldict1.pk','w+b'))

# brief = pickle.load(open('finaldict1.pk','rb'))
# list_brief = [[a]+list(brief[a]) for a in brief]
# pickle.dump(list_brief, open('list_brief.pk','w+b'))
# url -> name invest_phase field time

# info-tag clearfix: 地区
# info-box：简介
# live 融资 没有就算了
list_brief = pickle.load(open('list_brief.pk','rb'))
i = 0
half = list_brief[int(len(list_brief)/2):]
for e in half:
    try:
        url = e[0]
        # url = 'http://www.cyzone.cn/company/516857.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html5lib")
        ###
        intro = soup.select('div.info-box')[0].get_text().strip()
        ###
        tags = soup.select('div.info-tag.clearfix')[0]
        tags = tags.find_all('li')
        ###
        location = ''
        real_tags = []
        for tag in tags:
            tag_children = list(tag.children)
            if 'i2' in tag.__str__():
                location = tag.get_text().strip()
            elif 'i6' in tag_children[0].__str__():
                for child_str in tag_children[1:]:
                    if type(child_str) == Tag:
                        t = child_str.get_text().strip()
                        if len(t) > 0:
                            real_tags.append(t)
            ###

        ###
        invest_exps = soup.select('div.live')
        invest_info = []
        if len(invest_exps)>0:
            invest_exps = invest_exps[0].find_all('tr')
            for exp in invest_exps[1:]:
                invest_info = list(map(lambda x:x.get_text().strip(),
                                       filter(lambda x:type(x)==Tag, exp.contents)))
        # name invest_phase field project_date + location intro real_tags invest_info
        half[i]+=[location, intro, real_tags, invest_info]
        # print(half[i])
        # print()
        response.close()
        time.sleep(1)
        if i % 100 == 0:
            print(i, 'OK')
    except Exception as e:
        print('error at index', int(len(list_brief)/2)+i)
        print(str(e))

    i+=1
    # print(i, 'OK')

pickle.dump(half, open('half2.pk','w+b'))
