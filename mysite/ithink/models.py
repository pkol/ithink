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


from django.db import models

# Create your models here.

class SequenceDef(models.Model):
	name = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class SequenceDefOrder(models.Model):
	sequenceDef = models.ForeignKey(SequenceDef)
	question = models.CharField(max_length=200)
	order = models.IntegerField()
	def __unicode__(self):
		return "%s ::: %s" % (self.sequenceDef.name, self.question)
	

class SequencePlay(models.Model):
	STATE_NOT_STARTED = 1 
	STATE_STARTED = 2
	STATE_PAUSE = 3

	name = models.CharField(max_length=200)
	seq = models.ForeignKey(SequenceDef)
	current = models.ForeignKey('SequencePlayItem', null=True)
	state = models.IntegerField()
	def __unicode__(self):
		return self.name

class SequencePlayItem(models.Model):
	sp = models.ForeignKey(SequencePlay)
	question = models.CharField(max_length=200)
	order = models.IntegerField()




class Answer(models.Model):
	questionItem = models.ForeignKey(SequencePlayItem)
	answer = models.CharField(max_length=200)
	posx = models.IntegerField(default = -1)
	posy = models.IntegerField(default = -1);
	attrs = models.TextField(default="");

class Event(models.Model):
	data = models.TextField()
