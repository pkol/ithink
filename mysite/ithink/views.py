# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Paweł Kołodziej <p.kolodziej@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.core import serializers
from ithink.models import *
from operator import attrgetter
import time
import json
import os
from event import *
import random

SERVER_NAME = "localhost:8000"

def player(request, play_id):
	play = get_object_or_404(SequencePlay, pk=play_id)
	return render(request, 'ithink/player.html', {'play':play});

def serializeAnswer(a):
	return {'txt':a.answer, 'posx':a.posx, 'posy':a.posy, 'id':a.id, 'attrs' : a.attrs}

def playerGetData(request, play_id):
	play = get_object_or_404(SequencePlay, pk=play_id)
	ret = {}
	ret['state'] = play.state
	if play.state == SequencePlay.STATE_STARTED:
		ret['answers'] = [serializeAnswer(a) for a in  Answer.objects.filter(questionItem = play.current)]
		ret['question'] = play.current.question;
		ret['question_id'] = play.current.id;
	ret['last_event'] = eventGetLastId()
	return HttpResponse(json.dumps(ret), content_type="application/json")
	
def playerStart(request, play_id):
	play = get_object_or_404(SequencePlay, pk=play_id)
	# compute next question 
		
	sequence = get_list_or_404(SequencePlayItem, sp = play.id)
	next = min(sequence, key=attrgetter("order"))
	play.current = next;
	play.state = SequencePlay.STATE_STARTED
	play.save();
	eventAdd({'type':'playStart', 'playId':play.id})
	return HttpResponse(json.dumps({}), content_type="application/json")

def playerNext(request, play_id):
	dir =   request.GET["dir"]; # "next" or "prev"
	play = get_object_or_404(SequencePlay, pk=play_id)
	sequence = get_list_or_404(SequencePlayItem, sp = play.id)
	if dir =="next":
		sequence = [se for se in sequence if se.order > play.current.order]
	elif dir =="prev":
		sequence = [se for se in sequence if se.order < play.current.order]
	else:
		return 0;
	if len(sequence) == 0:
		#play.state = SequencePlay.STATE_ENDED;
		#play.save();
		#eventAdd({'type':'playEnd', 'playId':play.id})
		return HttpResponse(json.dumps({}), content_type="application/json")
	if dir =="next":
		nextq = min(sequence, key=attrgetter("order"))
	elif dir =="prev":
		nextq = max(sequence, key=attrgetter("order"))
	play.state = SequencePlay.STATE_STARTED; # activate answers
	play.current = nextq; ##TODO
	play.save()
	eventAdd({'type':'playQuestion', 'playId':play.id, 'question': play.current.question, 'question_id':play.current.id })
	return HttpResponse(json.dumps({}), content_type="application/json")

def playerAction(request):
	g =  request.GET
	if g['action'] == "setPos":
		a = get_object_or_404(Answer, pk=int(g['answerId']))
		a.posx = float(g['posx']);
		a.posy = float(g['posy']);
		a.save();
	if g['action'] == "pause":
		play = get_object_or_404(SequencePlay, pk=int(g['play_id']))
		play.state = SequencePlay.STATE_PAUSE
		play.save();
		eventAdd({'type':'playPause', 'playId':play.id})
	if g['action'] == "resume":
		play = get_object_or_404(SequencePlay, pk=int(g['play_id']))
		play.state = SequencePlay.STATE_STARTED
		play.save();
		eventAdd({'type':'playResume', 'playId':play.id})
	if g['action'] == "newQuestion":
		play = get_object_or_404(SequencePlay, pk=int(g['play_id']))
		sequence = get_list_or_404(SequencePlayItem, sp = play.id)
		for s in sequence:
			if s.order > play.current.order:
				s.order += 1;
				s.save();
		spi = SequencePlayItem(sp = play, question=g['question'], order=play.current.order+1);
		spi.save();
		play.current = spi;
		play.save();
		eventAdd({'type':'playQuestion', 'playId':play.id, 'question': play.current.question, 'question_id':play.current.id })
	if g['action'] == "newLabel":
		addAnswer(int(g['question_id']), g['labelTxt'], json.dumps({'type':'label'}) ) 


	return HttpResponse(json.dumps({}), content_type="application/json")
	
		



def playerQR(request, play_id):
	qr = os.popen("qrencode http://%s/ithink/%s/audience/ -o - -s 10"%(SERVER_NAME,play_id));
	return HttpResponse(qr.read(), content_type="image/png")
	

def waitForEvent(request, last_event):
	print request.META['HTTP_USER_AGENT']
	return HttpResponse(json.dumps(eventWait(last_event, 50 + random.randint(0,15) )), content_type="application/json");

def addAnswer(questionId, answerTxt, attrs):
	question = get_object_or_404(SequencePlayItem, pk=questionId)
	a = Answer(questionItem = question, answer = answerTxt, attrs = attrs)
	a.save()
	eventAdd({'type':'answer', 'question_id':question.id, 'play_id': question.sp.id,'answer':serializeAnswer(a)});

	

def audience(request, play_id):
	if request.method == 'POST':
		addAnswer(request.POST['question'], request.POST['answer'],"");
#		play = get_object_or_404(SequencePlay, pk=play_id)
#		question = get_object_or_404(SequencePlayItem, pk=request.POST['question'])
#		a = Answer(questionItem = question, answer = request.POST['answer'])
#		a.save()
#		eventAdd({'type':'answer', 'question_id':question.id, 'answer':serializeAnswer(a)});
	play = get_object_or_404(SequencePlay, pk=play_id)
	return render(request, 'ithink/audience.html', {'play':play});
	

def audienceGetData(request, play_id):
	return playerGetData(request, play_id);

def audienceAnswer(request, play_id):
	return audience(request, play_id)
	

def DUPA():
	
	answers = Answer.objects.filter(question = play.current, sequencePlay = play)
	sequence = [se for se in sequence if se.order > play.current.order]
	if len(sequence) == 0:
		next = 'end'
	next = min(sequence, key=attrgetter("order"))

	return render(request, 'ithink/player.html', {'question':play.current, 'answers' : answers, 'play' : play} )

def next(request, play_id):
	play = get_object_or_404(SequencePlay, pk=play_id)
	o = play.current.order
	sequence = get_list_or_404(SequenceDefOrder, sequenceDef = play.sp)
	sequence = [se for se in sequence if se.order > play.current.order]
	if len(sequence) == 0:
		return render(request, 'ithink/end.html')
	play.current = min(sequence, key=attrgetter("order"))
	play.save()
	return player(request, play_id)
		


def answer(request, play_id):
	play = get_object_or_404(SequencePlay, pk=play_id)
	sequence = get_list_or_404(SequenceDefOrder, sequenceDef = play.sp)
		
	return render(request, 'ithink/answer.html', {'question':play.current, 'play' : play} )



def start(request, play_id):
	sequences = get_list_or_404(SequenceDef)
	return render(request, 'ithink/start.html', {'sequences':sequences} )
	
def playNew(request, sequence_id):
	s = get_object_or_404(SequenceDef, id=sequence_id)
	sp = SequencePlay(name = "automatic", seq = s, state = SequencePlay.STATE_NOT_STARTED)
	sp.save()
	for seqDef in SequenceDefOrder.objects.filter(sequenceDef = s):
		spi = SequencePlayItem(sp = sp, question = seqDef.question, order=seqDef.order)
		spi.save()
	return render(request, 'ithink/playNew.html', {'sp' : sp} )
	
	
def foo(request):
	s1= SequenceDef(name = "zwierzaki")
	s1.save()
	SequenceDefOrder(sequenceDef=s1, order=1, question="zyrafa to").save()
	SequenceDefOrder(sequenceDef=s1, order=2, question="malpa to").save()
	SequenceDefOrder(sequenceDef=s1, order=3, question="albators to").save()
	s2= SequenceDef(name = "miasta")
	s2.save()
	SequenceDefOrder(sequenceDef=s2, order=1, question="W Warszawie").save()
	SequenceDefOrder(sequenceDef=s2, order=2, question="W Krakowie").save()
	SequenceDefOrder(sequenceDef=s2, order=3, question="W katowicach").save()
	s3= SequenceDef(name = "alk")
	s3.save()
	SequenceDefOrder(sequenceDef=s3, order=1, question="Gdzie jechać na wakacje?").save()
	SequenceDefOrder(sequenceDef=s3, order=2, question="Elementy, które w tych zajęciach były dobre?").save()
	SequenceDefOrder(sequenceDef=s3, order=3, question="Co należałoby zmienić? Jak?").save()
