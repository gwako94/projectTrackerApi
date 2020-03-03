from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated


from .models import Project
from .serializers import ProjectSerializer


class ProjectAPIView(APIView):
    """
   Class for handling projects.
   """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        """
        Method for creating a project
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            data = {
                'status': 'success',
                'message': 'Proeject created successfully',
                'project': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        """
        Method for getting all projects.
        """
        query_set = Project.objects.all()
        serializer = self.serializer_class(query_set, many=True)
        data = {
            'status': 'success',
            'message': 'Projects fetched successfully',
            'Projects': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class ProjectUpdateDeleteApiView(APIView):
    """ Class to handle project update and delete """

    serializer_class = ProjectSerializer

    def get(self, request, id):
        """ Get a single project """
        try:
            project = Project.objects.get(id=id)

        except Project.DoesNotExist:
            raise exceptions.NotFound("Project does not exist")

        serializer = self.serializer_class(project)
        data = {
            'status': 'success',
            'message': 'Project fetched successfully',
            'Projects': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, id):
        """Update a project"""
        try:
            project = Project.objects.get(id=id)

        except Project.DoesNotExist:
            raise exceptions.NotFound("Project does not exist")


        serializer = self.serializer_class(
            project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            "message": "Project updated successfully",
            "Project": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        """Delete a project"""
        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            raise exceptions.NotFound("Project does not exist")

        project.delete()
        data = {
            "message": "Project deleted successfully!"
        }
        return Response(data, status=status.HTTP_200_OK)
