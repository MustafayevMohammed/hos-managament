from . models import CustomUserModel


def custom_context_processor(request):
    user = request.user
    unaccepted_users = CustomUserModel.objects.filter(is_accepted = False)
    return {
        "user":user,
        "unaccepted_users":unaccepted_users,
    }

