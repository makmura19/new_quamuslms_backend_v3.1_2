from rest_framework.decorators import action


def generate_action_method(name, config):
    method_type = config.get("method", "get").lower()
    detail = config.get("detail", False)
    methods = [method_type]

    def generated_method(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        return self._handle_custom_action(request, pk=pk)

    generated_method.__name__ = name
    return action(detail=detail, methods=methods, url_path=name)(generated_method)
