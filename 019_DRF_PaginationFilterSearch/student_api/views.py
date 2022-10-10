from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, mixins, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action

from .models import Student
from .serializers import StudentSerializer


class StudentListView(APIView):

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['success'] = f"Student {student.last_name} updated succesfuly"
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        data = {
            "success": f"Student {student.last_name} deleted succesfuly"
        }
        return Response(data)

############### GenericAPIView ###########################


class StudentView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StudentDetail(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


###################### Generic(Concrete) Views ##########################

class StudetListCreate(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentRUD(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


##################### ModelViewSets ################################

from .pagination import MyPageNumberPagination, MyLimitOffsetPagination, MycursorPagination

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter

class StudentCRUD(ModelViewSet):
    queryset = Student.objects.all().order_by('id') # order_by---- bu kisim default siralama yapmak icin . id degistirilebilir.
    serializer_class = StudentSerializer
    # pagination_class = MyPageNumberPagination
    # pagination_class = MyLimitOffsetPagination
    # pagination_class = MycursorPagination
        # Add filterset_fields:
    filterset_fields = ['first_name', 'last_name', 'number',]
    search_fields = ['first_name','last_name' ]
    ordering_fields = ['first_name', 'last_name', 'number',]
    # ordering_fields = '__all__'

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    @action(detail=False, methods=['GET'], url_path='student_count')
    def count(self, request):
        count = {
            'studen_count': self.queryset.count()
        }
        return Response(count)


    # def get_queryset(self):
    #     queryset = Student.objects.all()
    #     first_name = self.request.query_params.get('first_name')
    #     if first_name is not None:
    #         # This only brings exact names:
    #         # queryset = queryset.filter(first_name=first_name)
    #         # This is more flexible:
    #         queryset = queryset.filter(first_name__contains=first_name)
    #     return queryset