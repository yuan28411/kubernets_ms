from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, QueryDict
from kubernets_ms import k8s
from kubernetes import client
# Create your views here.


@k8s.self_login_required
def node(request):
    return render(request, 'k8s/node.html')


@k8s.self_login_required
def namespace(request):
    return render(request, 'k8s/namespace.html')


def namespace_api(request):
    # 调用api获取命名空间
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    k8s.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == 'GET':
        data = []
        search_key = request.GET.get('search_key')
        try:
            for ns in core_api.list_namespace().items:
                name = ns.metadata.name
                labels = ns.metadata.labels
                create_time = ns.metadata.creation_timestamp
                d = {'name': name, 'labels': labels, 'create_time': create_time}
                if search_key:
                    if search_key in name:
                        data.append(d)
                else:
                    data.append(d)
            code = 0
            msg = "查询成功"
        except Exception as e:
            status = getattr(e, "status")
            code = 1
            if status == 400:  # 400 格式错误，409 资源存在，403 没权限。
                msg = "格式错误"
            elif status == 409:
                msg = "资源存在"
            elif status == 403:
                msg = "没权限"
        count = len(data)
        if request.GET.get('page'):
            page = int(request.GET.get('page'))
            limit = int(request.GET.get('limit'))
            start = (page - 1) * limit
            end = page * limit
            data = data[start:end]

        result = {'code': code, 'msg': msg, 'count': count, 'data': data}
        print("GET DATA")
        return JsonResponse(result)

    elif request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        for ns in core_api.list_namespace().items:
            if name == ns.metadata.name:
                result = {'code': 1, 'msg': "命名空间已经存在！"}
                return JsonResponse(result)

        body = client.V1Namespace(
            api_version="v1",
            kind="Namespace",
            metadata=client.V1ObjectMeta(
                name=name
            )
        )
        try:
            core_api.create_namespace(body=body)
            code = 0
            msg = '创建成功'
        except Exception as e:
            status = getattr(e, "status")
            code = 1
            if status == 403:
                msg = "没权限"
            else:
                msg = "创建失败"
        result = {'code': code, 'msg': msg}
        return JsonResponse(result)

    elif request.method == 'DELETE':
        data = QueryDict(request.body)
        name = data.get('name')
        try:
            core_api.delete_namespace(name=name)
            code = 0
            msg = '删除成功'
        except Exception as e:
            status = getattr(e, "status")
            code = 1
            if status == 400:  # 400 格式错误，409 资源存在，403 没权限。
                msg = "格式错误"
            elif status == 409:
                msg = "资源存在"
            elif status == 403:
                msg = "没权限"
            else:
                msg = "邪门"
        result = {'code': code, 'msg': msg}
        print(result)
        return JsonResponse(result)

    elif request.method == 'PUT':
        pass

    else:
        pass


def node_api(request):
    # 调用api获取命名空间
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    k8s.load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == 'GET':
        data = []
        search_key = request.GET.get('search_key')
        try:
            for node in core_api.list_node_with_http_info()[0].items:
                name = node.metadata.name
                labels = node.metadata.labels
                status = node.status.conditions[-1].status
                scheduler = ("是" if node.spec.unschedulable is None else "否")
                cpu = node.status.capacity['cpu']
                memory = node.status.capacity['memory']
                kebelet_version = node.status.node_info.kubelet_version
                cri_version = node.status.node_info.container_runtime_version
                create_time = node.metadata.creation_timestamp
                d = {"name": name, "labels": labels, "status": status,
                        "scheduler": scheduler, "cpu": cpu, "memory": memory,
                        "kebelet_version": kebelet_version, "cri_version": cri_version,
                        "create_time": create_time}
                if search_key:
                    if search_key in name:
                        data.append(d)
                else:
                    data.append(d)
            code = 0
            msg = "查询成功"
        except Exception as e:
            status = getattr(e, "status")
            code = 1
            if status == 400:  # 400 格式错误，409 资源存在，403 没权限。
                msg = "格式错误"
            elif status == 409:
                msg = "资源存在"
            elif status == 403:
                msg = "没权限"
        count = len(data)
        if request.GET.get('page'):
            page = int(request.GET.get('page'))
            limit = int(request.GET.get('limit'))
            start = (page - 1) * limit
            end = page * limit
            data = data[start:end]

        result = {'code': code, 'msg': msg, 'count': count, 'data': data}
        print("GET DATA")
        return JsonResponse(result)

    elif request.method == 'POST':
        pass

    elif request.method == 'DELETE':
        pass

    elif request.method == 'PUT':
        pass

    else:
        pass

