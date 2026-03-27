from django.contrib import admin
from .models import Package, Booking, Review, Profile, PackageImage, Highlight, ItineraryDay, Inclusion, Exclusion

# Other models
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(PackageImage)
admin.site.register(Highlight)
admin.site.register(ItineraryDay)
admin.site.register(Inclusion)
admin.site.register(Exclusion)


class HighlightInline(admin.TabularInline):
    model = Highlight
    extra = 5


class PackageAdmin(admin.ModelAdmin):
    inlines = [HighlightInline]

admin.site.register(Package, PackageAdmin)

class ItineraryInline(admin.TabularInline):
    model = ItineraryDay
    extra = 5

class PackageAdmin(admin.ModelAdmin):
    inlines = [ItineraryInline]


class InclusionInline(admin.TabularInline):
    model = Inclusion
    extra = 5


class ExclusionInline(admin.TabularInline):
    model = Exclusion
    extra = 5


class PackageAdmin(admin.ModelAdmin):
    inlines = [InclusionInline, ExclusionInline]
