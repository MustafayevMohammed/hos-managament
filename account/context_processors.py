from . models import CustomUserModel


def get_admin_email(request):

    user = request.user
    return {"user":user}
    # if request.user.is_superuser == True:
    #     user = request.user
    # else:
    #     return {"doctor":user}
    # return {"admin":user}
