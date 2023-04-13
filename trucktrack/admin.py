from django.contrib import admin
from .models import User,Cities,Orders,Performers,Chat,Chats

admin.site.register(User)
admin.site.register(Cities)
admin.site.register(Orders)
admin.site.register(Performers)
admin.site.register(Chat)
admin.site.register(Chats)
# Register your models here.