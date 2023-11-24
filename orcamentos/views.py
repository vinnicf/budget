from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Orcamento, OrcamentoItem
from .serializers import OrcamentoSerializer, OrcamentoItemSerializer
from .permissions import IsOwnerOrReadOnly, IsItemOwner

class OrcamentoViewSet(viewsets.ModelViewSet):
    queryset = Orcamento.objects.all()
    serializer_class = OrcamentoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Filter Orcamentos to those owned by the current user
        user = self.request.user
        return Orcamento.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrcamentoItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrcamentoItemSerializer
    queryset = OrcamentoItem.objects.all()
    permission_classes = [IsItemOwner]

    def get_queryset(self):
        queryset = OrcamentoItem.objects.all()
        orcamento_id = self.request.query_params.get('orcamento_id', None)
        if orcamento_id is not None:
            queryset = queryset.filter(orcamento_id=orcamento_id)
        return queryset

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
