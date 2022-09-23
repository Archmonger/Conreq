from django_idom.components import view_to_component
from django_idom.decorators import auth_required
from idom import component, html

from conreq import config
from conreq._core.components import tabbed_viewport
from conreq._core.user_management import views

# TODO: Create SimpleTable and SimpleForm that use Conreq templates
# TODO: Figure out some way to integrate user invites into this


@component
@auth_required(auth_attribute="is_staff")
def edit_user(state, set_state):
    return html._(view_to_component(views.EditUserView, compatibility=True))


@component
@auth_required(auth_attribute="is_staff")
def delete_user(state, set_state):
    return html._(view_to_component(views.DeleteUserView, compatibility=True))


@component
@auth_required(auth_attribute="is_staff")
def manage_users(state, set_state):
    return html._(view_to_component(views.manage_users, compatibility=True))


@component
@auth_required(auth_attribute="is_staff")
def manage_invites(state, set_state):
    return html._(view_to_component(views.manage_invites, compatibility=True))


@component
@auth_required(auth_attribute="is_staff")
def create_invite(state, set_state):
    return html.div("Under Construction")


# pylint: disable=protected-access
@component
@auth_required(auth_attribute="is_staff")
def user_management(state, set_state):
    return html._(
        tabbed_viewport(
            state,
            set_state,
            tabs=config.tabs.user_management.installed,
            top_tabs=config._internal_tabs.user_management,
        )
    )
