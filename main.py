import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

# pip install tweepy
# pip install textblob
# developer.twitter.com/en/portal/dashboard



def istenmeyen_karakter_temizle(text):
    istenmeyen_karakterler = [':',';','!','*','$','½','&']
    for karakter in istenmeyen_karakterler:
        text = text.replace(karakter,'')
    return text

def duygu_analizi(tweet,counter):
    #print(counter, tweet.text)
    blob1 = TextBlob(tweet.full_text)
    blob1_clean = istenmeyen_karakter_temizle(blob1)
    blob1_lang = blob1_clean.detect_language() # HTTP Error 429: Too Many Requests
    #print("lang", blob1_lang)
    if blob1_lang != 'en':
        blob1_ing = blob1_clean.translate(to='en')
    else:
        blob1_ing = blob1_clean
    #print("blob1_ing", blob1_ing)
    #print(blob1_ing.sentiment)
    #print("--------------------------------------------------------------")
    print("Translate ile yapıldı.!")
    return blob1_clean, blob1_ing.polarity

def duygu_analizi_cevirisiz(tweet,counter):
    #print(counter, tweet.text)
    blob1 = TextBlob(tweet.full_text)
    blob1_clean = istenmeyen_karakter_temizle(blob1)
    print("Translatesiz yapıldı.!", blob1_clean.polarity)
    return blob1_clean, blob1_clean.polarity

# Yetkilendirme işlemleri
consumerKey = "qwe"
consumerSecret = "asd"
accessToken = "qweewq"
accessTokenSecret = "asddsa"
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)
#Yetkilendirmeden sorna tweepy ile yazıları alıp textblob ile duygu analizi yapıcaz.
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []
counter = 1
keyword = str(input("Keyword giriniz..\n")) #BritishBasketball #ArmenianGenocide
noOfTweet = int(input("Kaç adet twit kontrol edilsin\n"))
print(noOfTweet, "adet tweet api ile alınıyor...")
# tweets = tweepy.Cursor(api.user_timeline, id = 'elonmusk',tweet_mode='extended').items(noOfTweet) # özel bir kullanıcının twitlerini alır
tweets = tweepy.Cursor(api.search, q=keyword,tweet_mode='extended').items(noOfTweet) # kelime üzerinden twit arıyorsun

print("Tweetlerde duygu analizi yapılıyor... Tweet sayısı fazlaysa bu işlem birkaç dakika sürebilir")
for tweet in tweets:
    try:
        text, polarity = duygu_analizi(tweet,counter)
        tweet_list.append(text)
    except:
        text, polarity = duygu_analizi_cevirisiz(tweet,counter)
        tweet_list.append(text)
    #print("Polarity Tipi:",type(polarity))
    if polarity > 0:
        positive_list.append(text)
    elif polarity < 0:
        negative_list.append(text)
    else:
        neutral_list.append(text)
    counter += 1
new_counter = 1
print("<<<<>>>> Pozitif Twit Sayısı",len(positive_list))
if len(positive_list) != 0:
    print("-----------------Pozitif Twitler-----------------")
    for eleman in positive_list:
        eleman = eleman.strip()
        print(str(new_counter)+".)", eleman)
        new_counter += 1
new_counter = 1
print("<<<<>>>> Negatif Twit Sayısı",len(negative_list))
if len(negative_list) != 0:
    print("-----------------Negatif Twitler-----------------")
    for eleman in negative_list:
        eleman = eleman.strip()
        print(str(new_counter)+".)", eleman)
        new_counter += 1
new_counter = 1
print("<<<<>>>> Nötr Twit Sayısı",len(neutral_list))
if len(neutral_list) != 0:
    print("-----------------Nötr Twitler-----------------")
    for eleman in neutral_list:
        eleman = eleman.strip()
        print(str(new_counter)+".)", eleman)
        new_counter += 1
