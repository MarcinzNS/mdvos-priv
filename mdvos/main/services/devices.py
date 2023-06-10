from ..models.models import Devices, Specification ,Like
from django.db.models import Q
from main.models.models import Comment
from django.shortcuts import get_object_or_404

def getDevicesDataForPage(category: str, sort_by: str, how_many: int, which_page: int, brand_filter: list, ram_filter: list) -> dict:
    start = (which_page-1)*how_many

    devices = Devices.objects.filter(accepted=True)
    if category != "NOT":
        devices = devices.filter(device_type=category)
    if sort_by != "NOT":
        devices = devices.order_by(sort_by)
    devices = devices.values()

    specifications = list(Specification.objects.values('spec_type_id__name', 'value', "devices_id"))

    result = []
    for device in devices:
        device_specifications = [spec for spec in specifications if spec['devices_id'] == device['id_device']]
        device_data = {
            'device': 
                device,
            'specifications': 
                {spec['spec_type_id__name']: spec['value'] for spec in device_specifications}
        }
        if len(brand_filter) + len(ram_filter) > 0:
            if device_data['specifications']["RAM"] in ram_filter or device['brand'] in brand_filter:
                result.append(device_data)
        else:
            result.append(device_data)

    return {"data": result[start:start+how_many], "how_many_results": len(result)}

def getDeviceData(id: int) -> dict:
    return Devices.objects.all().filter(id_device=id).values()[0]

def getSpecificationData(id: int) -> dict:
    specifications = list(Specification.objects.values('spec_type_id__name', 'value', "devices_id"))
    device_specifications = {spec['spec_type_id__name']: spec['value'] for spec in specifications if spec['devices_id'] == id}
    return device_specifications

def getDeviceLike(request,id: int) ->dict:
    devices= get_object_or_404(Devices,pk=id)
    result = []
    user_dislikes_device = False
    user_likes_device = False
    like_count = Like.objects.filter(devices_id=devices, like=True).count()
    dislike_count = Like.objects.filter(devices_id=devices, dislike=True).count()

    if request.user.is_authenticated:
        user_likes_device = Like.objects.filter(user_id=request.user, devices_id=devices, like=True).exists()
        user_dislikes_device = Like.objects.filter(user_id=request.user, devices_id=devices, dislike=True).exists()


    result = {'user_dislikes_device': user_dislikes_device, 'user_likes_device': user_likes_device,
                     'like_count': like_count,'dislike_count': dislike_count}
    return result


def getComments(id: int) -> dict:
    comments = Comment.objects.filter(devices_id=id, main_comment_id='0').values()
    return comments

def getCommentUsername(comment_id: int) -> str:
    comment = Comment.objects.filter(id_comment=comment_id).select_related('user_id').first()
    if comment:
        return comment.user_id.username
    return ""

def getUnderComments(comment_id: int):
    under_comments = Comment.objects.filter(main_comment_id=comment_id).select_related('user_id').values('id_comment', 'text', 'user_id__username')
    return list(under_comments)


def getMCData(id: int) -> dict:
    main_comments = Comment.objects.filter(devices_id=id, main_comment_id=0).select_related('user_id')
    main_comments_data = [{'id_comment': comment.id_comment, 'text': comment.text, 'username': comment.user_id.username} for comment in main_comments]
    return main_comments_data

def getCommentsWithUnderComments(id: int) -> dict:


    main_comments_data = getMCData(id)
    comments = getComments(id)
    comments_username=getCommentUsername(id)
    under_comments = []
    comments_dict = {}

    for comment in comments:
        comment_id = comment['id_comment']
        comments_dict[comment_id] = {
            'id_comment': comment_id,
            'text': comment['text'],
            'username': getCommentUsername(comment_id),
            'under_comments': []
        }

    for main_comment in main_comments_data:
        main_comment_id = main_comment['id_comment']
        if main_comment_id in comments_dict:
            comments_dict[main_comment_id]['under_comments'] = getUnderComments(main_comment_id)


    return list(comments_dict.values())

