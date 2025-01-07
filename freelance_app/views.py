from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED, \
    HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from django.shortcuts import get_object_or_404


from .models import Job, User
from .permissions import IsClient, IsAdmin
from .serializers import UserSerializer, JobSerializer, UserUpdateSerializer


@api_view(['POST'])
def register(request):
    try:
        # Validate and create new user
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    except Exception as e:
        return Response(
            {'error': 'Failed to register user', 'detail': str(e)},
            status=400
        )

@api_view(['GET', 'PUT'])
@permission_classes([IsAdmin])
@authentication_classes([JWTAuthentication])
def user(request, user_id):
    if request.method == 'GET':
        """Handle GET: Get a user by ID"""
        get_user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(get_user)
        return Response(serializer.data, status=HTTP_200_OK)
    if request.method == 'PUT':
        """Handle PUT: Update a user"""
        # Create and validate the serializer
        get_user = get_object_or_404(User, id=user_id)
        serializer = UserUpdateSerializer(get_user, data=request.data)
        if serializer.is_valid():
            print(serializer.is_valid())
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def jobs(request, job_id=None):
    """Handle GET, POST, PUT, DELETE for jobs"""

    if request.method == 'GET':
        if job_id:
            """Handle GET: Get a job by ID"""
            job = get_object_or_404(Job, id=job_id)
            serializer = JobSerializer(job)
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            """Handle GET: List all jobs"""
            jobs = Job.objects.select_related('created_by').all()  # Optimize by joining created_by
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data, status=HTTP_200_OK)

    elif request.method == 'POST':
        """Handle POST: Create a new job for authenticated client"""
        # Check authentication
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=HTTP_401_UNAUTHORIZED)

        # Check permissions
        if not IsClient().has_permission(request, None):
            return Response({'detail': 'Permission denied.'}, status=HTTP_403_FORBIDDEN)

        serializer = JobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=HTTP_201_CREATED)

    # For PUT and DELETE, a job_id is required
    if job_id is None:
        return Response({'detail': 'Job ID is required for update or delete.'}, status=HTTP_400_BAD_REQUEST)

    job = get_object_or_404(Job, id=job_id)

    # Handle DELETE request
    if request.method == 'DELETE':
        # Allow Admin to delete any job post
        if request.user.role == 'Admin':
            job.delete()
            return Response({'message': 'Job deleted successfully'}, status=HTTP_204_NO_CONTENT)

        # Allow Client/Creator to delete only their own jobs
        if job.created_by != request.user:
            return Response({'error': 'You can only delete your own jobs'}, status=HTTP_403_FORBIDDEN)

        job.delete()
        return Response({'message': 'Job deleted successfully'}, status=HTTP_204_NO_CONTENT)

    # Handle PUT request
    elif request.method == 'PUT':
        if request.user.role == 'Client' and job.created_by != request.user:
            return Response({'error': 'You can only update your own jobs'}, status=HTTP_403_FORBIDDEN)

        serializer = JobSerializer(job, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
