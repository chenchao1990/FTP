"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from web_chat.views import chatroom


urlpatterns = [

    url(r'^chat_room/$', chatroom.chatroom, name="web_chat"),
    url(r'^contacts/$', chatroom.contacts, name="load_contacts_list"),
    url(r'^msg/$', chatroom.new_msg, name="send_msg"),
    url(r'^new_msg/$', chatroom.new_msg, name="check_msg"),

]
