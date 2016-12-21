import numpy as np
import jieba
import hashlib
import re
import time

xxx = '''
1993年，南京大学有这样一个男生寝室，四个男生都没有女朋友，
于是搞了个组合叫“名草无主四大天王”。这四大天王坚持每晚举行“卧谈会”，
从各种学术上讨论如何摆脱光棍状态。这一年的11月，校园的梧桐树落叶凋零，令他们分外伤情。
他们在11日这一天晚上卧谈时，符号学的灵感突然登门造访。
11月11日，四个1字排开，不正是好像四根光秃秃的棍子吗？这四根光棍不正是在巧妙地诉说着“名草无名四大天王”的凄凉吗？
'''


class Repeat:
    REX_CH = re.compile(u'[\u4e00-\u9fa5]+')    # 中文
    REX_EN = re.compile('[A-Za-z]+')        # 英文

    cut_func = jieba.cut
    @classmethod
    def hash2bin(cls, hash):
        d = ''
        for i in hash:
            try:
                if int(i) > 7:
                    d = d + '1'
                else:
                    d = d + '0'
            except ValueError:
                d = d + '1'
        return d

    @classmethod
    def hash_bin(cls, s):
        h = hashlib.md5(s.encode()).hexdigest()
        return cls.hash2bin(h)

    @classmethod
    def hist(cls, cut):
        _cut = {x: 0 for x in set(cut)}
        for i in cut:
            _cut[i] += 1
        return {cls.hash_bin(k): v/len(cut) for k, v in _cut.items()}

    @classmethod
    def simhash(cls, s, RE=None, cut_func=None):
        if RE:
            REX = RE
        else:
            REX = re.compile(u'[\u4e00-\u9fa5]+')
        if not cut_func:
            cut_func = cls.cut_func

        cut = [x for x in cut_func(s) if re.match(REX, x)]

        ver = [[v * (int(x) if int(x) > 0 else -1) for x in k] for k, v in cls.hist(cut).items()]
        ver = np.array(ver)
        ver_sum = ver.sum(axis=0)
        sim = ''.join(['1' if x > 0 else '0' for x in ver_sum])
        return sim

yyy = '''
知乎上有个提问，小时候缺爱的女孩子，长大后该怎么办？
或许在我这里，只是希望一直有人陪。
喜宝说，我想要很多很多的爱，要不就是很多很多的钱，实在不行，有健康也是好的。
我有个坏毛病，经常会半夜饿到不行，爬起来找吃的。是真的饿到胃疼，有时候直接饿醒了，每次看到电影里的台词，睡着了就不饿了，我是压根不相信。
为什么会半夜饿？
究其原因，是大学的时候没人陪我吃饭，每次都是一直等到有人陪我的时候，我才会去吃饭，最后把自己饿到胃疼，久而久之，就渐渐习惯了熬到很晚才吃饭。
我不喜欢一个人吃饭，也不喜欢一个人逛街，更不喜欢一个人呆着，可是成长啊，往往是越不喜欢的便越要学会接受它。
（二）
讲讲上一段恋爱吧。
我和他认识的时候，是因为贴吧聚餐，他主动找我要的微信，附带一个如沐春风般的笑容。
我一直以为他是被我的美色打动，后来问他原因。
他说，他第一次看见那么能吃的女孩子，他惊呆了，可是有觉得看我吃饭很意思，仿佛食物都有了灵魂，让人的心情莫名的好了起来。
我们初相识，是因为他看见了我饿死鬼投胎的吃相。
我们在一起，是因为他厨艺很好，好到什么程度呢？就是那种你吃过一顿，就能惦记一辈子的感觉。即便是现在回忆起他来，我的味蕾都会有反应。
他总是给我做很多很多好吃的，午后阳光从窗子洒进来，窗帘是淡绿色的小碎花，空气里弥漫着饭香味，我们两个人坐在桌前，一边吃饭，一边聊天。
我喜欢和他一起手挽着手去菜市场买菜，西红柿土豆黄瓜小白菜，手里拎着的这些果蔬食物，就好像我拥有的全世界。
有一次，我们从菜市场回去的路上，明明是艳阳高照的天气，却突然间下起了冰雹，那是他第一次看见冰雹，被砸了一下之后，便立马丢了手里的菜，双手护住我，我傻了吧唧的去捡菜，被砸了一身。
他立马臭骂了我一顿，说我是他见过，最好吃的女孩子了。
'''

zzz = '''
知乎上有个提问，小时候缺爱的女孩子，长大后该怎么办？
或许在我这里，只是希望一直有人陪。
喜宝说，我想要很多很多的爱，要不就是很多很多的钱，实在不行，
我有个坏毛病，经常会半夜饿到不行，爬起来找吃的。是真的饿到胃疼，有时候直接饿醒了，每次看到电影里的台词，睡着了就不饿了，我是压根不相信。
究其原因，是大学的时候没人陪我吃饭，每次都是一直等到有人陪我的时候，我才会去吃饭，最后把自己饿到胃疼，久而久之
我不喜欢一个人吃饭，也不喜欢一个人逛街，更不喜欢一个人呆着，可是成长啊，往往是越不喜欢的便越要学会接受它。
我和他认识的时候，是因为贴吧聚餐，他主动找我要的微信，附带一个如沐春风般的笑容。
我一直以为他是被我的美色打动，后来问他原因。
他说，他第一次看见那么能吃的女孩子，他惊呆了，可是有觉得看我吃饭很意思，仿佛食物都有了灵魂，让人的心情莫名的好了起来。
我们初相识，是因为他看见了我饿死鬼投胎的吃相。
我们在一起，是因为他厨艺很好，好到什么程度呢？就是那种你吃过一顿，就能惦记一辈子的感觉。即便是现在回忆起他来，我的味蕾都会有反应。
他总是给我做很多很多好吃的，午后阳光从窗子洒进来，窗帘是淡绿色的小碎花，空气里弥漫着饭香味，我们两个人坐在桌前，一边吃饭，一边聊天。
我喜欢和他一起手挽着手去菜市场买菜，西红柿土豆黄瓜小白菜，手里拎着的这些果蔬食物，
有一次，我们从菜市场回去的路上，明明是艳阳高照的天气，却突然间下起了冰雹，那是他第一次看见冰雹，被砸了一下之后，便立马丢了手里的菜，双手护住我，我傻了吧唧的去捡菜，被砸了一身。
他立马臭骂了我一顿，说我是他见过，最好吃的女孩子了。
'''
ccc = zzz * 10

print(Repeat.simhash(yyy))
print(Repeat.simhash(zzz))
print(Repeat.simhash(ccc))