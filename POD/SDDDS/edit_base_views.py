# Copyright 2021 Fe-Ti

def main(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('sddds:result'))
    return HttpResponseRedirect(reverse('sddds:index'))
