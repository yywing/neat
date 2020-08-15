from rest_framework import viewsets, mixins


class NoUpdateModelViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    """
    A viewset that provides default `list()`, `retrieve()`, `create()` and `delete()` actions.
    """
    pass


class NoCreateModelViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    """
    A viewset that provides default `list()`, `retrieve()`, `update()` and `delete()` actions.
    """
    pass


class NoCreateUpdateModelViewSet(mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet):
    """
    A viewset that provides default `list()`, `retrieve()` and `delete()` actions.
    """
    pass
