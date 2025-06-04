from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from payment.tasks import send_note
from django.utils.html import format_html

class CustomUserAdmin(BaseUserAdmin):

    list_display = BaseUserAdmin.list_display + ('is_new_user', 'send_note_to_user',)

    @admin.display(description='New User?', boolean=True)
    def is_new_user(self, obj):
        seven_days_ago = timezone.now() - timezone.timedelta(days=7)
        return obj.date_joined >= seven_days_ago

    @admin.display(description='Notify user')
    def send_note_to_user(self, obj):
        return format_html(
            '<a class="button" href="?user_id={}">Send Note</a>',
            obj.id
        )

    def changelist_view(self, request, extra_context=None):
        if 'user_id' in request.GET:
            user_id = request.GET['user_id']
            
            send_note.delay(user_id)

        return super().changelist_view(request, extra_context)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)