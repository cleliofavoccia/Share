from django.contrib import admin

from .models import Estimation, Decision


class EstimationAdmin(admin.ModelAdmin):
    """Class that manage Estimation objects in Django admin """


class DecisionAdmin(admin.ModelAdmin):
    """Class that manage Decision objects in Django admin """
    pass


# Register the admin class with the associated model
admin.site.register(Estimation, EstimationAdmin)
admin.site.register(Decision, DecisionAdmin)
