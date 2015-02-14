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

from django.conf.urls import patterns, url

from ithink import views

urlpatterns = patterns('',
    url(r'^(?P<play_id>\d+)$', views.answer, name='answer'),
    url(r'^(?P<play_id>\d+)/player/$', views.player, name='player'),
    url(r'^(?P<play_id>\d+)/playerGetData/$', views.playerGetData, name='playerGetData'),
    url(r'^(?P<play_id>\d+)/playerStart/$', views.playerStart, name='playerStart'),
    url(r'^(?P<play_id>\d+)/playerNext/$', views.playerNext, name='playerNext'),
    url(r'^(?P<play_id>\d+)/playerQR/$', views.playerQR, name='playerQR'),
    url(r'^playerAction/$', views.playerAction, name='playerAction'),

    url(r'^(?P<play_id>\d+)/audience/$', views.audience, name='audience'),
    url(r'^(?P<play_id>\d+)/audienceGetData/$', views.audienceGetData, name='audienceGetData'),

    url(r'^(?P<play_id>\d+)/next/$', views.next, name='next'),
    url(r'^(?P<play_id>\d+)/start/$', views.start, name='start'),
    url(r'^playNew/(?P<sequence_id>\d+)/$', views.playNew, name='playNew'),
    url(r'^waitForEvent/(?P<last_event>\d+)/$', views.waitForEvent, name='waitForEvent'),
    url(r'^foo/$', views.foo, name='foo'),
)
