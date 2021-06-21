from blog.models import Credit


def site_cred(request):
    try:
        user = request.user
        print(user)
        cred = Credit.objects.filter(author=user)

        point = ""

        for i in cred:
            point += str(i.Credit_Points)
        return {'cred': point}
    except:
        point = "0"
        return {'cred': point}

# name surname
# python/django backend - designation
# email


# Name: Rushabh Gediya
# designation: Python/Django Developer
# email: rushabhgediya38@gmail.com

