from django.urls import path

from course_project.web.views import HomeView, LoginFormView, RegisterFormView, \
    IndicationsListView, AnnounceView, PaymentsView, EditTaxesView, OldDebtsView, \
    pay_to, client_debts, clear_debt, EditClientView, AddAnnounceView, EditAnnounceView, delete_announce, add_archive, \
    view_archive, all_archive, reporting_view, ForbiddenPageView, ClientOldDebtsView, DeleteAnnounce, announce_confirm, \
    EditUnitsView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('indications/', IndicationsListView.as_view(), name='indications'),

    path('announce/', AnnounceView.as_view(), name='announce'),
    path('announce/add/', AddAnnounceView.as_view(), name='add announce'),
    path('announce/edit/<int:pk>/', EditAnnounceView.as_view(), name='edit announce'),
    path('announce/delete/<int:pk>/', delete_announce, name='delete announce'),

    path('announce/confirm/', announce_confirm, name='confirm'),

    path('olddebts/', OldDebtsView.as_view(), name='old debts'),
    path('client/debts/<int:pk>/', ClientOldDebtsView.as_view(), name='client debts'),
    path('clear/debt/<int:pk>/', clear_debt, name='clear debt'),

    path('payments/', PaymentsView.as_view(), name='payments'),
    path('pay/<int:pk>/', pay_to, name='pay to'),
    path('edit/taxes/<int:pk>/', EditTaxesView.as_view(), name='taxes'),
    path('edit/client/<int:pk>/', EditClientView.as_view(), name='edit client'),

    path('reporting/', reporting_view, name='reporting'),
    path('edit/units/', EditUnitsView.as_view(), name='edit units'),

    path('add/archive/', add_archive, name='add archive'),
    path('view/archive/<int:pk>/', view_archive, name='view archive'),
    path('all/archive/', all_archive, name='all archive'),

    path('auth/login/', LoginFormView.as_view(), name='login'),
    path('auth/register/', RegisterFormView.as_view(), name='register'),

    path('403/', ForbiddenPageView.as_view(), name='403'),

)

