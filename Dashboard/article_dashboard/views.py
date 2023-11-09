from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers
from article_dashboard.models import Articles, Summaries
from article_dashboard.forms import SummariesForm, ArticlesList
from datetime import datetime, timedelta


def show(request):
    '''
    Show list of articles with summaries.
    '''
    
    # receive dates from request
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
  
    if not (date_from and date_to):
        # if dates are not found, 
        # calculate dates period for the last 30 days
        date_from = datetime.now().date() - timedelta(days=30)
        date_to = datetime.now().date()

        # prepare data, use filter for dates period
        articles = Articles.objects.all().filter(published_date__range=[date_from, date_to]).order_by('-published_date')
        summaries = Summaries.objects.all()

        return render(request,"articles_list.html",context=
            {'articles':articles, 'summaries':summaries, 'date_from':date_from, 'date_to':date_to})
    
    else:
        # form pass validation to cautch error with non-correct period of dates (start date more then end date)
        form = ArticlesList(request.GET)
        form.is_valid()  

        # prepare data, use filter for dates period
        articles = Articles.objects.all().filter(published_date__range=[date_from, date_to]).order_by('-published_date')
        summaries = Summaries.objects.all()
        
        # pass additional parameter "form" to "context" for validation needs
        return render(request,"articles_list.html",context=
            {'articles':articles, 'summaries':summaries, 'date_from':date_from, 'date_to':date_to, 'form':form})
        

def summary_edit(request, id):  
    summary = Summaries.objects.get(id=id)  
    return render(request,'summary_edit.html', {'summary':summary}) 


def summary_update(request, id): 
    summary= Summaries.objects.get(id=id) 

    if request.method=="POST":
        try: 
            form = SummariesForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                # if form is not valid,
                # prepare values for saving
                is_bad = request.POST.get('is_bad')
                if is_bad == 'on':
                    is_bad = True
                else:
                    is_bad =  False
                summ = request.POST.get('summary').strip()
                article = str(request.POST.get('article'))
                
                # if not found related Article, return 404
                try:
                    toSave = Summaries(id=id, is_bad=is_bad, summary=summ, article=Articles.objects.get(pk=article))
                    toSave.save()
                except ObjectDoesNotExist:
                    return HttpResponse(status=404)

            # if success, redirect to main view
            return redirect("/articles_list")  
        
        except KeyError:
            return HttpResponse(status=400)

    # if not success, turn to "summary_edit" view
    return render(request, 'summary_edit.html', {'summary': summary}) 

