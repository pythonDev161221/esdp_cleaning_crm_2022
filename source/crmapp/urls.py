from django.urls import path, include

from crmapp.views.excel import (export_manager_report_to_excel, export_expense_excel)
from crmapp.views.client_views import (ClientCreateView,
                                       ClientListView,
                                       ClientUpdateView)

from crmapp.views.service_order_views import (ServiceOrderCreateView,
                                              ServiceOrderUpdateView,
                                              ServiceOrderDeleteView)

from crmapp.views.inventories import (InventoryListView,
                                      InventoryCreateView,
                                      InventoryUpdateView,
                                      InventoryDeleteView,
                                      InventoryOrderCreateView,
                                      InventoryOrderRemoveView)

from crmapp.views.foreman import (ForemanOrderUpdateCreateView,
                                  PhotoBeforeView,
                                  PhotoDetailView,
                                  ServiceForemanOrderCreateView,
                                  ForemanExpenseView)

from crmapp.views.service_views import ServiceListView, ServiceCreateView, ServiceUpdateView, ServiceDeleteView

from crmapp.views.manager_report import ManagerReportCreateView, ManagerReportListView

from crmapp.views.order_staff import OrderStaffCreateView, OrderStaffDeleteView

from crmapp.views.order import OrderListView, OrderDetailView, FirstStepOrderCreateView, \
    SecondStepOrderCreateView, OrderFinishView, OrderDeleteView, OrderDeletedListView

from crmapp.views.income_outcome_report import IncomeOutcomeReportView

from crmapp.views.object_type import ObjectTypeListView, ObjectTypeCreateView, ObjectTypeUpdateView, \
    ObjectTypeDeleteView

from crmapp.views.fine import FineListView, FineCreateView, FineUpdateView, FineDeleteView

from crmapp.views.bonus import BonusListView, BonusCreateView, BonusUpdateView, BonusDeleteView

app_name = 'crmapp'

client_urlpatterns = [
    path('all/', ClientListView.as_view(), name='client_index'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('up/<int:pk>/', ClientUpdateView.as_view(), name='client_update')
]

excel_urlpatterns = [
    path('expense/', export_expense_excel, name='expense-excel'),
    path('manager-report/', export_manager_report_to_excel, name='manager-excel')
]
order_urlpatterns = [
    path('', OrderListView.as_view(), name='order_index'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('deleted_list', OrderDeletedListView.as_view(), name='order_deleted_list'),
    path('create/', FirstStepOrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/add_cleaners/', SecondStepOrderCreateView.as_view(), name='cleaners_add'),
    path('<int:pk>/service/create/', ServiceOrderCreateView.as_view(), name="service_order_create"),
    path('<int:pk>/service/update/', ServiceOrderUpdateView.as_view(), name="service_order_update"),
    path('delete/<int:pk>/', ServiceOrderDeleteView.as_view(), name="service_order_delete"),
    path('<int:pk>/staff/add/', OrderStaffCreateView.as_view(), name='order_staff_add'),
    path('staff/delete/<int:pk>', OrderStaffDeleteView.as_view(), name='order_staff_delete'),
    path("<int:pk>/inventory/add/", InventoryOrderCreateView.as_view(), name="inventory_order_add"),
    path("inventory/<int:pk>/remove/", InventoryOrderRemoveView.as_view(), name="inventory_order_remove"),
    path('<int:pk>/finish/', OrderFinishView.as_view(), name='order_finish'),
]

service_urlpatterns = [
    path('list/', ServiceListView.as_view(), name='service_list'),
    path('create/', ServiceCreateView.as_view(), name='service_create'),
    path('update/<int:pk>/', ServiceUpdateView.as_view(), name='service_update'),
    path('delete/<int:pk>/', ServiceDeleteView.as_view(), name='service_delete'),
]

inventory_urlpatterns = [
    path('inventory/all/', InventoryListView.as_view(), name='inventory_index'),
    path('inventory/create/', InventoryCreateView.as_view(), name='inventory_create'),
    path('inventory/up/<int:pk>/', InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory/delete/<int:pk>/', InventoryDeleteView.as_view(), name='inventory_delete')
]

brigadier_urlpatterns = [
    path('order/<int:pk>/update/', ForemanOrderUpdateCreateView.as_view(), name='foremanorder_create'),
    path('order/<int:pk>/photo/before/', PhotoBeforeView.as_view(), name='foreman_photo_before'),
    path('<int:pk>/photos/', PhotoDetailView.as_view(), name='foreman_photo'),
    path('order/<int:pk>/add/service/', ServiceForemanOrderCreateView.as_view(), name='foreman_create_service'),
    path('order/<int:pk>/add/expense/', ForemanExpenseView.as_view(), name='foreman_create_expense')
]

manager_report_urlpatterns = [
    path('order/<int:pk>/manager_report/create/', ManagerReportCreateView.as_view(), name='manager_report_create'),
    path('manager_report/all/', ManagerReportListView.as_view(), name='manager_report_list'),
]

object_type_urlpatterns = [
    path('all/', ObjectTypeListView.as_view(), name='object_type_list'),
    path('create/', ObjectTypeCreateView.as_view(), name='object_type_create'),
    path('up/<int:pk>/', ObjectTypeUpdateView.as_view(), name='object_type_update'),
    path('delete/<int:pk>/', ObjectTypeDeleteView.as_view(), name='object_type_delete')
]

fine_urlpatterns = [
    path('all/', FineListView.as_view(), name='fine_list'),
    path('create/', FineCreateView.as_view(), name='fine_create'),
    path('up/<int:pk>/', FineUpdateView.as_view(), name='fine_update'),
    path('delete/<int:pk>/', FineDeleteView.as_view(), name='fine_delete')
]

bonus_urlpatterns = [
    path('all/', BonusListView.as_view(), name='bonus_list'),
    path('create/', BonusCreateView.as_view(), name='bonus_create'),
    path('up/<int:pk>/', BonusUpdateView.as_view(), name='bonus_update'),
    path('delete/<int:pk>/', BonusDeleteView.as_view(), name='bonus_delete')
]

urlpatterns = [
    path('client/', include(client_urlpatterns)),
    path('service/', include(service_urlpatterns)),
    path('cleaners/', include(brigadier_urlpatterns)),
    path('inventories/', include(inventory_urlpatterns)),
    path('', include(manager_report_urlpatterns)),
    path('order/', include(order_urlpatterns)),
    path('income_outcome_report', IncomeOutcomeReportView.as_view(), name='income_outcome_report'),
    path('excel/', include(excel_urlpatterns)),
    path('object_type/', include(object_type_urlpatterns)),
    path('fine/', include(fine_urlpatterns)),
    path('bonus/', include(bonus_urlpatterns)),
]
