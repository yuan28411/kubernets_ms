from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from kubernetes import client, config
from dashboard.models import K8sAuth
import os
import random
import yaml


apiserver = "https://192.168.38.81:6443"

def auth_check(auth_type, token=None):
    if auth_type == 'token':
        configuration = client.Configuration()
        configuration.host = apiserver # APISERVER地址
        ca_file = os.path.join(os.getcwd(), "dashboard", "ca.crt")  # K8s集群CA证书（/etc/kubernetes/pki/ca.crt）
        configuration.ssl_ca_cert = ca_file
        configuration.verify_ssl = True  # 启用证书验证
        configuration.api_key = {"authorization": "Bearer " + token}
        client.Configuration.set_default(configuration)
        core_api = client.CoreApi()
        try:
            core_api.get_api_versions()  # 查看K8S接口版本查看验证
            return True
        except Exception as e:
            return False
    elif auth_type == 'kubeconfig':
        user_obj = K8sAuth.objects.get(token=token)
        try:
            content_json = yaml.load(user_obj.content, Loader=yaml.FullLoader)
        except:
            K8sAuth.objects.get(token=token).delete()
            return False
        config.load_kube_config_from_dict(content_json)
        core_api = client.CoreApi()
        try:
            core_api.get_api_versions()  # 查看K8S接口版本查看验证
            return True
        except Exception as e:
            return False


# 视图登陆认证
def self_login_required(func):
    def inner(request):
        is_login = request.session.get('is_login', False)
        if not is_login:
            return redirect('/login')
        else:
            return func(request)
    return inner


# 加载连接k8s api的认证
def load_auth_config(auth_type, token):
    if auth_type == 'token':
        configuration = client.Configuration()
        configuration.host = apiserver  # APISERVER地址
        ca_file = os.path.join(os.getcwd(), "dashboard", "ca.crt")  # K8s集群CA证书（/etc/kubernetes/pki/ca.crt）
        configuration.ssl_ca_cert = ca_file
        configuration.verify_ssl = True  # 启用证书验证
        configuration.api_key = {"authorization": "Bearer " + token}
        client.Configuration.set_default(configuration)
    elif auth_type == 'kubeconfig':
        user_obj = K8sAuth.objects.get(token=token)
        content_json = yaml.load(user_obj.content, Loader=yaml.FullLoader)
        config.load_kube_config_from_dict(content_json)
    else:
        pass