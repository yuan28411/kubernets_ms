from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from kubernetes import client, config
from dashboard.models import K8sAuth
import os
import random
import yaml
from kubernets_ms import k8s


# Create your views here.


@k8s.self_login_required
def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        """
        token = request.POST.get('token')
        if token:
            configuration = client.Configuration()
            configuration.host = "https://192.168.38.55:6443"  # APISERVER地址
            ca_file = os.path.join(os.getcwd(), "dashboard", "ca.crt")  # K8s集群CA证书（/etc/kubernetes/pki/ca.crt）
            configuration.ssl_ca_cert = ca_file
            configuration.verify_ssl = True  # 启用证书验证
            configuration.api_key = {"authorization": "Bearer " + token}
            client.Configuration.set_default(configuration)
            # apps_api = client.AppsV1Api()
            core_api = client.CoreApi()
            # code = 0
            # msg = ''
            try:
                result = core_api.get_api_versions() #查看K8S接口版本查看验证
                print(result)
                code = 200
                msg = '认证成功'
            except Exception as e:
                e = str(e).split('\n')[3]
                e = eval(e.split(' ')[3])
                code = e['code']
                msg = e['message']
                # code = getattr(e, "code")
                # msg = getattr(e, "message")
            result = {'code': code, 'msg': msg}
            return JsonResponse(result)
            
        else:
            token_random = str(random.random()).split('.')[1]
            file_obj = request.FILES.get('file')
            try:
                content = file_obj.read().decode()
                K8sAuth.objects.create(auth_type="kubeconfig", token=token_random, content=content)
            except Exception:
                code = 402
                msg = '文件类型异常'
                result = {'code': code, 'msg': msg}
                return HttpResponse(result)
            user_obj = K8sAuth.objects.get(token=token_random)
            content_json = yaml.load(user_obj.content, Loader=yaml.FullLoader)
            config.load_kube_config_from_dict(content_json)
            core_api = client.CoreApi()
            try:
                core_api.get_api_versions() #查看K8S接口版本查看验证
                # print(result2)
                code = 200
                msg = '认证成功'
            except Exception as e:
                # e = str(e).split('\n')[3]
                # e = eval(e.split(' ')[3])
                print(e)
                code = 401
                msg = '错误'
                K8sAuth.objects.get(token=token_random).delete()
            result = {'code': code, 'msg': msg}
            return JsonResponse(result)
            #
            #
            # # kubeconfig = os.path.join(os.getcwd(), "kubeconfig")  # 获取当前目录并拼接文件
            # # config.load_kube_config(kubeconfig)  # 指定kubeconfig配置文件（/root/.kube/config）
            #
        pass
        """
        token = request.POST.get('token')
        if token:
            if k8s.auth_check('token', token):
                request.session['is_login'] = True  # 判断是否登陆
                request.session['auth_type'] = 'token'  # 查看登陆类型
                request.session['token'] = token  # 用于查看K8s
                code = 200
                msg = 'Token有效'
            else:
                code = 401
                msg = 'Token无效'
            result = {'code': code, 'msg': msg}
            return JsonResponse(result)

        else:
            token_random = str(random.random()).split('.')[1]
            file_obj = request.FILES.get('file')
            try:
                content = file_obj.read().decode()
                K8sAuth.objects.create(auth_type="kubeconfig", token=token_random, content=content)
            except Exception:
                code = 401
                msg = '文件类型异常'
                result = {'code': code, 'msg': msg}
                return HttpResponse(result)
            if k8s.auth_check('kubeconfig', token_random):
                request.session['is_login'] = True  # 判断是否登陆
                request.session['auth_type'] = 'kubeconfig'  # 查看登陆类型
                request.session['token'] = token_random  # 用于查看K8s
                code = 200
                msg = 'kubeconfig文件有效'
            else:
                code = 401
                msg = '错误'
                K8sAuth.objects.get(token=token_random).delete()
            result = {'code': code, 'msg': msg}
            return JsonResponse(result)
            #
            #
            # # kubeconfig = os.path.join(os.getcwd(), "kubeconfig")  # 获取当前目录并拼接文件
            # # config.load_kube_config(kubeconfig)  # 指定kubeconfig配置文件（/root/.kube/config）
            #
    else:
        pass


def logout(request):
    request.session.flush()
    return redirect('/login')

