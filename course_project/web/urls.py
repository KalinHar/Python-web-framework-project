from django.urls import path

# from course_project.web.view import HomeView, LoginFormView, RegisterFormView, \
#     IndicationsListView, AnnounceView, PaymentsView, EditTaxesView, OldDebtsView, \
#     pay_to, client_debts, clear_debt, EditClientView, AddAnnounceView, EditAnnounceView, delete_announce, add_archive, \
#     view_archive, all_archive, reporting_view, ForbiddenPageView, ClientOldDebtsView, DeleteAnnounceView,\
#     EditUnitsView, EditMasterView
from course_project.web.views.announce import AnnounceView, AddAnnounceView, EditAnnounceView, DeleteAnnounceView
from course_project.web.views.archive import view_archive, all_archive
from course_project.web.views.auth import LoginFormView, RegisterFormView
from course_project.web.views.client_info import ClientDetailsView
from course_project.web.views.error_page import ForbiddenPageView
from course_project.web.views.home import HomeView
from course_project.web.views.indications import IndicationsListView
from course_project.web.views.old_debts import OldDebtsView, ClientOldDebtsView, clear_debt
from course_project.web.views.payments import PaymentsView, pay_to, EditTaxesView, EditClientView
from course_project.web.views.reporting import reporting_view, add_archive, EditUnitsView, EditMasterView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),

    path('indications/', IndicationsListView.as_view(), name='indications'),
    path('client-details/<int:pk>/', ClientDetailsView.as_view(), name='client details'),

    path('announce/', AnnounceView.as_view(), name='announce'),
    path('announce/add/', AddAnnounceView.as_view(), name='add announce'),
    path('announce/edit/<int:pk>/', EditAnnounceView.as_view(), name='edit announce'),
    path('announce/delete/<int:pk>/', DeleteAnnounceView.as_view(), name='delete announce'),

    path('payments/', PaymentsView.as_view(), name='payments'),
    path('payments/pay/<int:pk>/', pay_to, name='pay to'),
    path('payments/edit/taxes/', EditTaxesView.as_view(), name='taxes'),
    path('payments/edit/client/<int:pk>/', EditClientView.as_view(), name='edit client'),
    path('payments/olddebts/', OldDebtsView.as_view(), name='old debts'),
    path('payments/client/debts/<int:pk>/', ClientOldDebtsView.as_view(), name='client debts'),
    path('payments/clear/debt/<int:pk>/', clear_debt, name='clear debt'),

    path('reporting/', reporting_view, name='reporting'),
    path('reporting/add/archive/', add_archive, name='add archive'),
    path('reporting/edit/units/', EditUnitsView.as_view(), name='edit units'),
    path('reporting/edit/master/<int:pk>/', EditMasterView.as_view(), name='edit master'),

    path('archive/<int:pk>/', view_archive, name='view archive'),
    path('archive/all/', all_archive, name='all archive'),

    path('auth/login/', LoginFormView.as_view(), name='login'),
    path('auth/register/', RegisterFormView.as_view(), name='register'),

    path('403/', ForbiddenPageView.as_view(), name='403'),

)
