import logging

from rest_framework import viewsets
from helpers.role_permission import RolePermission
from helpers.base_handler.base_crud_handler import BaseCRUDHandler
from helpers.base_handler.base_query_handler import BaseQueryHandler
from utils.action_generator import generate_action_method

logger = logging.getLogger(__name__)


class BaseViewSet(viewsets.ViewSet):
    permission_classes = [RolePermission]

    model = None
    service = None
    data_name = "Data"
    def_list = {}
    params_validation = {}
    actions = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        standard_actions = {"list", "retrieve", "create", "update", "destroy"}
        actions = getattr(cls, "actions", {})
        for name, config in actions.items():
            if name in standard_actions:
                continue

            if hasattr(cls, name):
                continue

            setattr(cls, name, generate_action_method(name, config))

    def get_roles(self, action=None):
        action = action or self.action
        return self.actions.get(action, {}).get("roles", [])

    def handle_request(self, action_type, request=None, pk=None):

        method_name = self.action

        config = self.actions.get(self.action)
        if not config:
            raise NotImplementedError(f"Aksi {self.action} tidak didukung")

        serializer_class = config.get("serializer")

        if action_type == "list":
            return BaseQueryHandler.list(
                method_name,
                request,
                self.model,
                self.service,
                self.data_name,
                self.params_validation,
            )

        elif action_type == "retrieve":
            return BaseQueryHandler.retrieve(
                method_name, request, pk, self.model, self.service, self.data_name
            )

        elif action_type == "create":
            return BaseCRUDHandler.create(
                method_name,
                request,
                serializer_class,
                self.model,
                self.service,
                self.data_name,
            )

        elif action_type == "update":
            return BaseCRUDHandler.update(
                method_name,
                request,
                pk,
                serializer_class,
                self.model,
                self.service,
                self.data_name,
            )

        elif action_type == "destroy":
            return BaseCRUDHandler.destroy(
                method_name, request, pk, self.model, self.service, self.data_name
            )

        raise NotImplementedError(f"Action type '{action_type}' belum didukung.")

    def _handle_custom_action(self, request, pk=None):
        config = self.actions.get(self.action)
        if not config:
            raise NotImplementedError(f"Aksi {self.action} tidak didukung")

        method = config["method"].lower()
        serializer_class = config.get("serializer")

        if method == "get":
            if pk:
                return BaseQueryHandler.retrieve(
                    method_name=self.action,
                    request=request,
                    model=self.model,
                    pk=pk,
                    service=self.service,
                    data_name=self.data_name,
                )
            else:
                return BaseQueryHandler.list(
                    method_name=self.action,
                    request=request,
                    model=self.model,
                    service=self.service,
                    data_name=self.data_name,
                    params_validation=self.params_validation,
                )

        elif method == "put":
            return BaseCRUDHandler.update(
                method_name=self.action,
                request=request,
                pk=pk,
                serializer=serializer_class,
                model=self.model,
                service=self.service,
                data_name=self.data_name,
            )

        elif method == "delete":
            return BaseCRUDHandler.destroy(
                method_name=self.action,
                request=request,
                pk=pk,
                model=self.model,
                service=self.service,
                data_name=self.data_name,
            )

        return BaseCRUDHandler.create(
            method_name=self.action,
            request=request,
            serializer=serializer_class,
            model=self.model,
            service=self.service,
            data_name=self.data_name,
        )

    def list(self, request):
        return self.handle_request("list", request=request)

    def retrieve(self, request, pk=None):
        return self.handle_request("retrieve", request=request, pk=pk)

    def create(self, request):
        return self.handle_request("create", request=request)

    def update(self, request, pk=None):
        return self.handle_request("update", request=request, pk=pk)

    def destroy(self, request, pk=None):
        return self.handle_request("destroy", request=request, pk=pk)
