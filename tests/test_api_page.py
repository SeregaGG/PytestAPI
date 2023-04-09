import json
import pytest
from pages.main_page import MainPage


@pytest.mark.usefixtures('setup_driver')
class TestApi:
    #может быть лучше вынести method и description в json, а в параметрах передавать сгенерированный список файлов из ресурсов
    @pytest.mark.parametrize('file_name,method,description', ([('list_users.json', 'get', 'List users'), ('single_user.json', 'get', 'Single user'),
                                                   ('single_resource_not_found.json', 'get', 'Single <resource> not found'), ('list_resource.json', 'get', 'List <resource>'),
                                                   ('single_user_not_found.json', 'get', 'Single user not found'), ('delayed_response.json', 'get', 'Delayed response'),
                                                   ('single_resource.json', 'get', 'Single <resource>'), ('create_user.json', 'post', 'Create'),
                                                   ('register_user.json', 'post', 'Register - successful'), ('register_user_400.json', 'post', 'Register - unsuccessful'),
                                                   ('update_user.json', 'put', 'Update'), ('update_user_patch.json', 'patch', 'Update'),
                                                   ('login_user.json', 'post', 'Login - successful'), ('login_user_400.json', 'post', 'Login - unsuccessful')]))
    def test_methods(self, setup_driver, file_name, method, description):
        main_page = MainPage(setup_driver)

        api = main_page.get_resource(file_name)
        main_page.request_ui_click(api.get("request"), method=method, description=description)

        content = main_page.get_ui_response()
        status_code = main_page.get_ui_status_code()

        response = main_page.send_request(api.get("request"), method=method, data=api.get("body"))

        cleaned_response = response.json()
        content.pop("id", None)
        cleaned_response.pop("id", None)
        if content.get("createdAt") is not None and cleaned_response.get("createdAt") is not None:
            content["createdAt"] = content["createdAt"].split('.')[0][:-6]
            cleaned_response["createdAt"] = cleaned_response["createdAt"].split('.')[0][:-6]

        if content.get("updatedAt") is not None and cleaned_response.get("updatedAt") is not None:
            content["updatedAt"] = content["updatedAt"].split('.')[0][:-6]
            cleaned_response["updatedAt"] = cleaned_response["updatedAt"].split('.')[0][:-6]

        assert response.status_code == status_code
        assert json.dumps(content) == json.dumps(cleaned_response)

    @pytest.mark.parametrize('file_name,method,description', ([('single_user.json', 'delete', 'Delete')]))
    def test_delete_method(self, setup_driver, file_name, method, description):
        main_page = MainPage(setup_driver)

        api = main_page.get_resource(file_name)
        main_page.request_ui_click(api.get("request"), method=method, description=description)

        main_page.get_ui_response()
        status_code = main_page.get_ui_status_code()

        response = main_page.send_request(api.get("request"), method=method, data=api.get("body"))

        assert response.status_code == status_code
