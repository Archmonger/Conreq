from functools import update_wrapper
from urllib.parse import unquote

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from ordered_model.admin import (
    BaseOrderedModelAdmin,
    OrderedInlineModelAdminMixin,
    OrderedTabularInline,
)

from conreq._core.app_store import models


class DragDropOrderedModelAdmin(BaseOrderedModelAdmin, admin.ModelAdmin):
    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        return [
            path(
                "<path:object_id>/move-above/<path:other_object_id>/",
                wrap(self.move_above_view),
                name="{app}_{model}_order_above".format(**self._get_model_info()),
            )
        ] + super().get_urls()

    def move_above_view(self, request, object_id, other_object_id):
        obj = get_object_or_404(self.model, pk=unquote(object_id))
        other_obj = get_object_or_404(self.model, pk=unquote(other_object_id))
        obj.above(other_obj)
        # go back 3 levels (to get from /pk/move-above/other-pk back to the changelist)
        return HttpResponseRedirect("../../../")

    def make_draggable(self, obj):
        model_info = self._get_model_info()
        url = reverse(
            "{admin_name}:{app}_{model}_order_above".format(
                admin_name=self.admin_site.name, **model_info
            ),
            args=[-1, 0],  # placeholder pks, will be replaced in js
        )
        return mark_safe(
            r"""
        <div class="pk-holder" data-pk="%s"></div> <!-- render the pk into each row -->
        <style>[draggable=true] { -khtml-user-drag: element; }</style>  <!-- fix for dragging in safari -->
        <script>
            window.__draggedObjPk = null;
            django.jQuery(function () {
                const $ = django.jQuery;
                if (!window.__listSortableSemaphore) {  // make sure this part only runs once
                    window.__move_to_url = '%s'; // this is the url including the placeholder pks
                    $('#result_list > tbody > tr').each(function(idx, tr) {
                        const $tr = $(tr);
                        $tr.attr('draggable', 'true');
                        const pk = $tr.find('.pk-holder').attr('data-pk');
                        $tr.attr('data-pk', pk);
                        $tr.on('dragstart', function (event) {
                            event.originalEvent.dataTransfer.setData('text/plain', null);  // make draggable work in firefox
                            window.__draggedObjPk = $(this).attr('data-pk');
                        });
                        $tr.on('dragover', false); // make it droppable
                        $tr.on('drop', function (event) {
                            event.preventDefault();  // prevent firefox from opening the dataTransfer data
                            const otherPk = $(this).attr('data-pk');
                            console.log(window.__draggedObjPk, 'dropped on', otherPk);
                            const url = window.__move_to_url
                                .replace('\/0\/', '/' + otherPk + '/')
                                .replace('\/-1\/', '/' + window.__draggedObjPk + '/');
                            console.log('redirecting', url);
                            window.location = url;
                        });
                    });
                    window.__listSortableSemaphore = true;
                }
            });
        </script>
        """
            % (obj.pk, url)
        )

    make_draggable.allow_tags = True
    make_draggable.short_description = ""


# Register your models here.
@admin.register(models.Category)
class AppCategories(admin.ModelAdmin):
    pass


@admin.register(models.Subcategory)
class AppSubCategories(admin.ModelAdmin):
    list_display = ("name", "category")


class SpotlightAppTabularInline(OrderedTabularInline):
    model = models.SpotlightApp
    readonly_fields = (
        "order",
        "move_up_down_links",
    )
    ordering = ("order",)
    extra = 1


@admin.register(models.SpotlightCategory)
class SpotlightCategories(OrderedInlineModelAdminMixin, DragDropOrderedModelAdmin):
    model = models.SpotlightCategory
    list_display = ("name", "order", "make_draggable")
    ordering = ("order",)
    inlines = (SpotlightAppTabularInline,)


@admin.register(models.AppPackage)
class Apps(admin.ModelAdmin):
    pass


@admin.register(models.Screenshot)
class Screenshots(admin.ModelAdmin):
    pass


@admin.register(models.NoticeMessage)
class NoticeMessages(admin.ModelAdmin):
    pass
