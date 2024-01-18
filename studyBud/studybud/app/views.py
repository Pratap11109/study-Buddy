from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q
from django.http import Http404
from .models import Room, Topic, Message
from .forms import RoomForm


# Create your views here.
def home(request):
    q = request.GET.get("q") if request.GET.get("q") else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(Name__icontains=q)
        | Q(
            Description__icontains=q
        )  # used Q pipe for filter based on multiple parameter using Q we can use and or operation on quey parameter based on our need
    )  # want to go for parent field used "__" and  __icontains is a case-insensitive containment
    topics = Topic.objects.all()
    room_count = rooms.count()
    return render(
        request,
        "app/home.html",
        {"rooms": rooms, "topics": topics, "room_count": room_count},
    )


def room(request, pk):
    room_item = get_object_or_404(Room, id=pk)
    messages = None
    try:
        messages = get_list_or_404(Message, room=room_item)
    except Http404:
        pass
    return render(request, "app/room.html", {"room": room_item, "messages": messages})


def room_add(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("room_add")
    return render(request, "app/room_form.html", {"form": form})


def update_room(request, pk):
    room = get_object_or_404(Room, id=pk)
    form = RoomForm(instance=room)  # here we are getting the value of that room
    if request.method == "POST":
        form = RoomForm(
            request.POST, instance=room
        )  # here we define the second parameter which told that we have to modify that specific field
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "app/room_form.html", {"form": form})


def delete_room(request, pk):
    room_obj = get_object_or_404(Room, id=pk)
    if request.method == "POST":
        room_obj.delete()
        return redirect("home")
    return render(request, "app/delete.html", {"obj": room_obj})
