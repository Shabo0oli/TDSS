from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from json import JSONEncoder
import tweepy
import json
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.metrics import silhouette_score
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import io
import django.core.files.images as im
from matplotlib import style
from django.db.models import Count


from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from .resources import *






import pandas as pd



from .models import *

from polyglot.downloader import downloader



downloader.download("sentiment2.fa")
downloader.download("sentiment2.uz")
downloader.download("sentiment2.en")
downloader.download("sentiment2.ar")


from polyglot.text import Text, Word

Subject = {}


def calculate_polarity(text):
    polarity_score = 0
    try :
        polytext = Text(text)

        for w in polytext.words:
            polarity_score+= w.polarity

    except :
        pass
    return polarity_score


def outlier_removal_v1(ids, X):
    kmeans = KMeans(n_clusters=4)
    kmeans.fit(preprocessing.scale(X.astype('float64')))
    y = kmeans.labels_



    bincount_y = np.bincount(y)

    no_outlier_ids = []
    no_outlier_X = []

    min_population = +1e9
    less_populated_cluster = 0
    for i in range(0, len(bincount_y)):
        if bincount_y[i] < min_population:
            min_population = bincount_y[i]
            less_populated_cluster = i

    for i in range(len(y)):
        if y[i] != less_populated_cluster:
            no_outlier_ids.append(ids[i])
            no_outlier_X.append(X[i])

    no_outlier_ids = np.asarray(no_outlier_ids)
    no_outlier_X = np.asarray(no_outlier_X)

    return np.asarray(no_outlier_ids), np.asarray(no_outlier_X)

def fetchTweets(word , count , since , until):

    #s_year , s_month , s_day = since.split('-')
    #u_year, u_month, u_day = until.split('-')

    #since = datetime(int(s_year),int(s_month),int(s_day),0,0,0)
    #until = datetime(int(u_year),int(u_month),int(u_day),0,0,0)

    #print(since)
    #print(until)


    auth = tweepy.AppAuthHandler('1Y80BLxUB0nHBncEato2nMBMh', '2E79zBCr8Add0heS668ovgiTGxB9nQQB4mYpsT0GhswWJ6tugx')

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    Subject[word] = 0

    Tweet.objects.filter(Subject=word).delete()
    for tweet in tweepy.Cursor(api.search,
                               q=word,
                               rpp=count,
                               result_type="recent",
                               include_entities=True,
                                since = since,
                                until = until,
                               lang="fa",
                               tweet_mode='extended').items():
        tw = Tweet(Subject=word , Text=tweet.full_text , FavoriteCount=tweet.favorite_count ,
              FollowersCount=tweet.user.followers_count, RetweetCount=tweet.retweet_count, Date=tweet.created_at.date(),
                   Source=tweet.source , Username=tweet.user.screen_name , Location=tweet.user.location)
        tw.save()
        featured = Featured(Tweet=tw,Polarity=calculate_polarity(tweet.full_text) ,
                            Reliability=5*tweet.retweet_count + tweet.favorite_count ,
                            Popularity=tweet.user.followers_count )
        featured.save()

        Subject[word]+=1
        if Subject[word]==count:
            break;




def getanalysis(word):
    df = pd.DataFrame(
        list(Featured.objects.filter(Tweet__Subject=word).values('Reliability', 'Popularity', 'Polarity')))
    pf = pd.DataFrame(list(Featured.objects.filter(Tweet__Subject=word).values('id')))

    df = df.as_matrix()
    pf = pf.as_matrix()

    for i in range(0, 3):
        pf, df = outlier_removal_v1(pf, df)

    n_clusters = 4
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(preprocessing.scale(df.astype('float64')))
    y = kmeans.labels_

    bincount_y = np.bincount(y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = ['b', 'g', 'r', 'y', 'c', 'm', 'k', 'w']

    context = {}
    context['plots'] = []

    for i in range(1, len(y)):
        ax.scatter(df[i, 2], df[i, 1], df[i, 0], c=colors[y[i]], marker='.', s=50, linewidth=0.3)

    ax.set_xlabel('polarity')
    ax.set_ylabel('popularity')
    ax.set_zlabel('reliability')

    plt.savefig('web/static/' + word + 'plot0.png')
    context['plots'].append('web/static/' + word + 'plot0.png')

    plt.clf()
    style.use('ggplot')

    for i in range(0, len(y)):
        plt.scatter(df[i, 1], df[i, 0], c=colors[y[i]], marker='.', s=50)
    plt.xlabel('reliability')
    plt.ylabel('popularity')

    plt.savefig('web/static/' + word + 'plot1.png')
    context['plots'].append('web/static/' + word + 'plot1.png')

    plt.clf()
    style.use('ggplot')

    for i in range(0, len(y)):
        plt.scatter(df[i, 0], df[i, 2], c=colors[y[i]], marker='.', s=50)

    plt.xlabel('reliability')
    plt.ylabel('polarity')

    plt.savefig('web/static/' + word + 'plot2.png')
    context['plots'].append('web/static/' + word + 'plot1.png')

    plt.clf()
    style.use('ggplot')

    for i in range(0, len(y)):
        plt.scatter(df[i, 0], df[i, 2], c=colors[y[i]], marker='.', s=50)

    plt.xlabel('reliability')
    plt.ylabel('polarity')

    plt.savefig('web/static/' + word + 'plot2.png')
    context['plots'].append('web/static/' + word + 'plot2.png')

    plt.clf()
    style.use('ggplot')

    for i in range(0, len(y)):
        plt.scatter(df[i, 1], df[i, 2], c=colors[y[i]], marker='.', s=50)
    plt.xlabel('popularity')
    plt.ylabel('polarity')

    plt.savefig('web/static/' + word + 'plot3.png')
    context['plots'].append('web/static/' + word + 'plot3.png')

    plt.clf()
    plt.hist(df[:, 0])
    plt.xlabel('distribution of reliability')
    plt.savefig('web/static/' + word + 'plot4.png')
    context['plots'].append('web/static/' + word + 'plot4.png')

    plt.clf()
    plt.hist(df[:, 1])
    plt.xlabel('distribution of popularity')
    plt.savefig('web/static/' + word + 'plot5.png')
    context['plots'].append('web/static/' + word + 'plot5.png')

    plt.clf()
    plt.hist(df[:, 2])
    plt.xlabel('distribution of polarity')
    plt.savefig('web/static/' + word + 'plot6.png')
    context['plots'].append('web/static/' + word + 'plot6.png')
    context['clusters'] = []

    for c in range(0, 4):

        cnt = 0
        sum_rl, min_rl, max_rl = 0.0, +1e9, -1e9
        sum_pp, min_pp, max_pp = 0.0, +1e9, -1e9
        sum_pl, min_pl, max_pl = 0.0, +1e9, -1e9
        # print 'C' + str(c), '==============='
        for i in range(0, len(df)):
            if y[i] == c:
                cnt += 1

                sum_rl += df[i][0]
                min_rl = min(min_rl, df[i][0])
                max_rl = max(max_rl, df[i][0])

                sum_pp += df[i][1]
                min_pp = min(min_pp, df[i][1])
                max_pp = max(max_pp, df[i][1])

                sum_pl += df[i][2]
                min_pl = min(min_pl, df[i][2])
                max_pl = max(max_pl, df[i][2])
        cluster = {}
        cluster['Name'] = 'C' + str(c)
        cluster['sum_rl'] = int(sum_rl)
        cluster['min_rl'] = int(min_rl)
        cluster['max_rl'] = int(max_rl)
        cluster['sum_pp'] = int(sum_pp)
        cluster['min_pp'] = int(min_pp)
        cluster['max_pp'] = int(max_pp)
        cluster['sum_pl'] = int(sum_pl)
        cluster['min_pl'] = int(min_pl)
        cluster['max_pl'] = int(max_pl)
        cluster['count'] = int(cnt)
        context['clusters'].append(cluster)

    return context

def index(request):


    context = {}
    return render(request, 'index.html' , context)


def fetchNumber(request):
    return JsonResponse(Subject, encoder=JSONEncoder)


@csrf_exempt
def analysis(request) :
    word = request.POST['word']
    count = int(request.POST['count'])
    since = request.POST['since']
    until = request.POST['until']
    fetchTweets(word , count , since , until)
    context = {}
    context['analysis'] = getanalysis(word)
    context['word'] = word
    context['count'] = count

    result = Tweet.objects.filter(Subject=word).values('Source').order_by('Source').annotate(count=Count('Source'))
    #print(result)
    context['sources'] = list(result)

    timeline = list(Tweet.objects.filter(Subject=word).values('Date').order_by('Date').annotate(count=Count('Date')))

    timelinetime = []
    timelinecount = []
    for obj in timeline :
        timelinetime.append(str(obj['Date'].strftime("%d-%m-%Y")))
        timelinecount.append(int(obj['count']))

    context['timelinetime'] = timelinetime
    print(timelinetime)
    context['timelinecount'] = timelinecount

    return render(request, 'analysis.html' , context)


@csrf_exempt
def export(request):
    tweets_resource = TweetResource()
    queryset = Tweet.objects.filter(Subject=request.POST['word'])
    dataset = tweets_resource.export(queryset)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tweets.xls"'
    return response