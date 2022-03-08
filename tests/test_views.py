"""
dj-stripe Views Tests.
"""

import pytest
from django.contrib.admin import helpers
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory
from django.urls import reverse
from pytest_django.asserts import assertContains, assertQuerysetEqual

from djstripe.views import ConfirmCustomAction

from .fields.models import TestCustomActionModel

pytestmark = pytest.mark.django_db


class TestConfirmCustomActionView:
    # to get around Session/MessageMiddleware Deprecation Warnings
    def dummy_get_response(self, request):
        return None

    @pytest.mark.parametrize(
        "action_name", ["_resync_instances", "_sync_all_instances", "_cancel"]
    )
    def test_post(self, action_name, monkeypatch):
        model = TestCustomActionModel

        # create instance to be used in the Django Admin Action
        instance = model.objects.create(id="test")

        data = {
            "action": action_name,
            helpers.ACTION_CHECKBOX_NAME: [instance.pk],
        }

        # monkeypatch instance.api_retrieve, instance.cancel, instance.__class__.sync_from_stripe_data, and app_config.get_model
        def mock_instance_api_retrieve(*args, **keywargs):
            pass

        def mock_subscription_cancel(*args, **keywargs):
            pass

        def mock_instance_sync_from_stripe_data(*args, **kwargs):
            pass

        def mock_get_model(*args, **kwargs):
            return model

        monkeypatch.setattr(model, "api_retrieve", mock_instance_api_retrieve)

        monkeypatch.setattr(model, "cancel", mock_subscription_cancel)

        monkeypatch.setattr(
            model,
            "sync_from_stripe_data",
            mock_instance_sync_from_stripe_data,
        )

        monkeypatch.setattr(ConfirmCustomAction.app_config, "get_model", mock_get_model)

        kwargs = {
            "action_name": action_name,
            "model_name": model.__name__.lower(),
            "model_pks": str(instance.pk),
        }

        if action_name == "_sync_all_instances":
            kwargs["model_pks"] = "all"

        # get the custom action POST url
        change_url = reverse("djstripe:djstripe_custom_action", kwargs=kwargs)

        # add the admin user to the mocked request and disable CSRF checks
        request = RequestFactory().post(change_url, data=data, follow=True)

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        view = ConfirmCustomAction()
        view.setup(request, **kwargs)

        # Invoke the Post method
        response = view.post(request)

        # assert user redirected to the correct url
        assert response.status_code == 302
        assert response.url == reverse(
            f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist"
        )

    @pytest.mark.parametrize(
        "action_name", ["_resync_instances", "_sync_all_instances", "_cancel"]
    )
    def test_get_queryset(self, action_name, monkeypatch):
        model = TestCustomActionModel

        # create instance to be used in the Django Admin Action
        instance = model.objects.create(id="test")

        data = {
            "action": action_name,
            helpers.ACTION_CHECKBOX_NAME: [instance.pk],
        }

        # monkeypatch app_config.get_model

        def mock_get_model(*args, **kwargs):
            return model

        monkeypatch.setattr(ConfirmCustomAction.app_config, "get_model", mock_get_model)

        kwargs = {
            "action_name": action_name,
            "model_name": model.__name__.lower(),
            "model_pks": str(instance.pk),
        }

        if action_name == "_sync_all_instances":
            kwargs["model_pks"] = "all"

        # get the custom action POST url
        change_url = reverse("djstripe:djstripe_custom_action", kwargs=kwargs)

        # add the admin user to the mocked request and disable CSRF checks
        request = RequestFactory().post(change_url, data=data, follow=True)

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        view = ConfirmCustomAction()
        view.setup(request, **kwargs)

        # Invoke the get_queryset method
        qs = view.get_queryset()

        # assert correct queryset gets returned
        if action_name == "_sync_all_instances":
            assertQuerysetEqual(qs, model.objects.all())
            assert qs[0] == instance
        else:
            assertQuerysetEqual(qs, model.objects.filter(pk__in=[instance.pk]))
            assert qs[0] == instance

    @pytest.mark.parametrize(
        "action_name", ["_resync_instances", "_sync_all_instances", "_cancel"]
    )
    def test_get_context_data(self, action_name, monkeypatch):
        model = TestCustomActionModel

        # create instance to be used in the Django Admin Action
        instance = model.objects.create(id="test")

        # monkeypatch app_config.get_model
        def mock_get_model(*args, **kwargs):
            return model

        monkeypatch.setattr(ConfirmCustomAction.app_config, "get_model", mock_get_model)

        kwargs = {
            "action_name": action_name,
            "model_name": model.__name__.lower(),
            "model_pks": str(instance.pk),
        }

        if action_name == "_sync_all_instances":
            kwargs["model_pks"] = "all"

        # get the custom action POST url
        change_url = reverse("djstripe:djstripe_custom_action", kwargs=kwargs)

        request = RequestFactory().get(change_url)

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        view = ConfirmCustomAction()
        view.setup(request, **kwargs)

        # Invoke the get_queryset method
        context = view.get_context_data()

        assert (
            context["info"][0]
            == f'Test custom action model: <a href="/admin/fields/testcustomactionmodel/{instance.pk}/change/">&lt;id=test&gt;</a>'
        )

    @pytest.mark.parametrize(
        "action_name", ["_resync_instances", "_sync_all_instances", "_cancel"]
    )
    def test_get(self, action_name, monkeypatch):
        model = TestCustomActionModel

        # create instance to be used in the Django Admin Action
        instance = model.objects.create(id="test")

        # monkeypatch app_config.get_model
        def mock_get_model(*args, **kwargs):
            return model

        monkeypatch.setattr(ConfirmCustomAction.app_config, "get_model", mock_get_model)

        kwargs = {
            "action_name": action_name,
            "model_name": model.__name__.lower(),
            "model_pks": str(instance.pk),
        }

        if action_name == "_sync_all_instances":
            kwargs["model_pks"] = "all"

        # get the custom action POST url
        change_url = reverse("djstripe:djstripe_custom_action", kwargs=kwargs)

        request = RequestFactory().get(change_url)

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        view = ConfirmCustomAction()
        view.setup(request, **kwargs)

        # Invoke the get method
        response = view.get(request)

        assert response.status_code == 200

        assertContains(response, "Test custom action model: ")

    @pytest.mark.parametrize(
        "action_name", ["_resync_instances", "_sync_all_instances", "_cancel"]
    )
    @pytest.mark.parametrize("is_admin_user", [True, False])
    def test_dispatch(self, is_admin_user, action_name, admin_user, monkeypatch):

        model = TestCustomActionModel

        # create instance to be used in the Django Admin Action
        instance = model.objects.create(id="test")

        # monkeypatch app_config.get_model
        def mock_get_model(*args, **kwargs):
            return model

        monkeypatch.setattr(ConfirmCustomAction.app_config, "get_model", mock_get_model)

        kwargs = {
            "action_name": action_name,
            "model_name": model.__name__.lower(),
            "model_pks": str(instance.pk),
        }

        # get the custom action POST url
        change_url = reverse("djstripe:djstripe_custom_action", kwargs=kwargs)

        request = RequestFactory().get(change_url)

        if is_admin_user:
            # add the admin user to the mocked request
            request.user = admin_user
        else:
            # add the AnonymousUser to the mocked request
            request.user = AnonymousUser()

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        view = ConfirmCustomAction()
        view.setup(request, **kwargs)

        # Invoke the dispatch method
        response = view.dispatch(request)

        if is_admin_user:
            assert response.status_code == 200
        else:
            assert response.status_code == 302
            assert (
                response.url
                == f"/admin/login/?next=/djstripe/action/{action_name}/testcustomactionmodel/{instance.pk}"
            )
