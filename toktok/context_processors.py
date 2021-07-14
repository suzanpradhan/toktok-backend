from toktok.apps.storemanagerapp import models as store_manager_app_models

def get_manager_details(request):
    try:
        store_manager_detail = store_manager_app_models.StoreManagerBasicDetail.objects.get(manager=request.user)
        return {
            'store_manager_detail': store_manager_detail
        }
    except Exception as e:
        return {
            'store_manager_detail': None,
        }

    