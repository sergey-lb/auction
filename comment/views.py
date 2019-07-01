from django.http import HttpRequest
from django.shortcuts import render, redirect
from comment.models import Comment
from django.db import IntegrityError


# Create your views here.
def comment_save(request: HttpRequest, auction_id: int):
    request.session['comment_save_called'] = True

    if 'parent_id' not in request.POST:
        return redirect('auction', auction_id=auction_id)

    if 'comment' not in request.POST:
        return redirect('auction', auction_id=auction_id)

    parent_id = int(request.POST['parent_id'])

    message = request.POST['comment'].strip()
    if not message:
        request.session['parent_of_empty_comment'] = parent_id
        return redirect('auction', auction_id=auction_id)

    if parent_id == 0:
        comment = Comment(
            user_id=request.user.id,
            auction_id=auction_id,
            comment=message
        )
    else:
        comment = Comment(
            user_id=request.user.id,
            auction_id=auction_id,
            parent_id=request.POST['parent_id'],
            comment=message
        )

    try:
        comment.save()
    except IntegrityError:
        pass

    return redirect('auction', auction_id=auction_id)
